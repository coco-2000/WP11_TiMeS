
# -*- coding: utf-8 -*-

""" Functions for longitudinal clustering """
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from matplotlib.colors import ListedColormap


def get_time_series(df, domain):
    """
    reshapes DataFrame from long to wide and returns an np.array
    :param df: pd.DataFrame with data in long format
    :return: data : np.array with reshaped data, df_data : pd.DataFrame with reshaped data
    """
    #display(df.Patient.nunique())
    df_data = (df.groupby('Patient').agg({domain: lambda x: list(x)}))
    data = pd.DataFrame(df_data[domain].values.tolist()).values

    data = np.expand_dims(data, axis=-1)
    return data, df_data

def kmeans_clustering(data, n_clusters, metric):
    """ 
    perforn kmeans clustering on data with "n_cluster" a number of clusters and "metric" the 
    metric used for clustering for example "dtw" or "euclidean".
    Returns the labels and the kmeans model
    """
    km = TimeSeriesKMeans(n_clusters=n_clusters, metric=metric, random_state=np.random.seed(0))
    labels = km.fit_predict(X=data, y=None)
    return labels, km

def plot_clusters(n_clusters, data, labels, km):
    """ 
    Make a plot of each cluster, showing the evolution of every patients in the cluster as well as 
    the cluster center obtained with DBA
    """
    for yi in range(n_clusters):
        plt.figure(figsize=(8, 2.5* n_clusters))
        plt.subplot(n_clusters, 1, 1 + yi)
        for xx in data[labels == yi]:
            plt.plot(xx.ravel(), "k-", alpha=.2)
        plt.plot(km.cluster_centers_[yi].ravel(), "r-", label="cluster center")
        plt.ylim(0,1)
        plt.title("Cluster %d" % (yi))
        plt.tight_layout()
        plt.legend()
        plt.show()

def choose_n_clusters(data, max_clusters, metric, plot_cluster=False):
    """ 
    Perform kmeans clustering for a range of number of clusters from 2 to max_clusters 
    and plot the silhouette score in order to be able to choose the best number of clusters
    """
    silhouette_scores = []

    for n_clusters in range(2, max_clusters):
        labels, km = kmeans_clustering(data, n_clusters, metric)
        silhouette_scores.append(silhouette_score(data, labels, metric=metric))

        if plot_cluster:
            plot_clusters(n_clusters, data, labels, km)

    plt.plot(range(2, max_clusters), silhouette_scores, marker='o')
    plt.title("Silhouette score for different number of clusters with " + metric)
    plt.show()

def order_clusters(data,labels):
    """ 
    To ease visualization of cluster comparison, we order the clusters by number of patients
    This was also done in the file Final_code_2 for acute multi-domain clustering
    """
    print(labels)
    cluster_info = []
    labels_name = np.unique(labels)

    for i in labels_name:
        # Identifying indices of points belonging to the current cluster
        cluster_points_indices = np.where(labels == i)[0]
        # Selecting the actual points belonging to the current cluster
        cluster_points = data[cluster_points_indices]

        # Adding information about the current cluster to the list
        cluster_info.append({
            'cluster_index': i,
            'cluster_points': cluster_points, 
            'cluster_indices_in_data': cluster_points_indices.tolist()
        })

    # Sorting the clusters based on the number of points they contain
    sorted_cluster_info = sorted(cluster_info, key=lambda x: len(x['cluster_points']), reverse=True)
    #map label to ordered labels
    ordered_labels = {sorted_cluster_info[i]['cluster_index'] : i for i in range(len(sorted_cluster_info))}
    # transform labels list into list with ordered labels
    ordered_labels_list = np.array([ordered_labels[label] for label in labels])
    print(ordered_labels_list)

    return ordered_labels_list


def add_labels_to_NMF(df, NMF, labels, domain):
    """ 
    Add labels to the NMF dataframe
    """
    df["longitudinal_" + domain + "_labels"] = labels
    NMF = NMF.drop(columns=["longitudinal_" + domain + "_labels"], errors='ignore')
    NMF = NMF.merge(df["longitudinal_" + domain + "_labels"], on='Patient')
    return NMF

def clusters_info(NMF, domain):
    """
    Give general information about the clusters, such as :
    - global trend with median and interquartile range evolution per cluster
    - number of patients per cluster,
    - separate lineplot for patients present twice, thrice and for all patients
    """
    NMF["longitudinal_" + domain + "_labels"] = NMF["longitudinal_" + domain + "_labels"].astype(str)

    # Generate a colormap with unique colors for each label
    color_labels = NMF["longitudinal_" + domain + "_labels"].unique()
    col_values = sns.color_palette('Set2')
    colormap = dict(zip(color_labels, col_values))

    #Show the global trend of each cluster
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=NMF, x="time_in_weeks", y=domain, estimator = "median", errorbar=("pi", 50), 
                 hue="longitudinal_" + domain + "_labels", palette=colormap)
    plt.xlabel("Time (in weeks)")
    plt.title(domain + " recovery per cluster with median and interquartile range")
    plt.show();

    #Show the number of patients per cluster per time point
    fig, ax = plt.subplots(2, 2, figsize=(12,12))  
    cluster_stats = NMF.groupby(["longitudinal_" + domain + "_labels", "time"]).agg({'Patient': 'count'}).reset_index()
    sns.barplot(data=cluster_stats, x="time", y="Patient", hue="longitudinal_" + domain + "_labels", palette=colormap, ax=ax[0,0])
    for container in ax[0,0].containers:
        ax[0,0].bar_label(container, fmt='%d', label_type='edge', fontsize=10)
    ax[0,0].set(xlabel='Time Point', ylabel='number of patients')
    ax[0,0].set_title("Number of patients per cluster per time point")

    #Show lineplot for patients present twice, thrice and for all patients
    twice_patients = NMF.groupby('Patient').filter(lambda x: len(x) == 2)
    sns.lineplot(data=twice_patients, x="time_in_weeks", y=domain, hue="longitudinal_" + domain + "_labels", 
                 palette=colormap, estimator =None, units="Patient", ax=ax[0,1]) 
    ax[0,1].set(xlabel='Time (in weeks)', ylabel=domain + " score")
    ax[0,1].set_title(domain + " score per cluster per patient only present twice")

    thrice_patients = NMF.groupby('Patient').filter(lambda x: len(x) == 3)
    sns.lineplot(data=thrice_patients, x="time_in_weeks", y=domain, hue="longitudinal_" + domain + "_labels", 
                 palette=colormap, estimator =None, units="Patient", ax=ax[1,0])
    ax[1,0].set(xlabel='Time (in weeks)', ylabel=domain +' score')
    ax[1,0].set_title(domain + " score per cluster per patient only present thrice")

    sns.lineplot(data=NMF, x="time_in_weeks", y=domain, hue="longitudinal_" + domain + "_labels", 
                 palette=colormap, estimator =None, units="Patient", ax=ax[1,1]) 
    ax[1,1].set(xlabel='Time (in weeks)', ylabel= domain +' score')
    ax[1,1].set_title(domain + " score per cluster for every patients")
    plt.show();

def comparison2(NMF, label0, label1, title):
    """ 
    Show the number of common patients between clusters of the 2 different clustering, as well as the percentage of common 
    patients through heatmaps
    """
    
    # Display the matrix of the number of common patients between clusters of the 2 different clustering
    info_long_domain = NMF[NMF["time"] == "1"].groupby([label0, label1]).size().unstack(fill_value=0)
    #display(info_long_domain)

    # Create a custom colormap to highlight 0 values
    colors = sns.color_palette("YlGnBu", 256)
    colors[0] = (1, 1, 1)  # Set color for value 0 to white
    custom_cmap = ListedColormap(colors)

    # Create a figure with 3 heatmaps
    fig, ax = plt.subplots(1, 3, figsize=(21,5))

    # First heatmap : number of common patients between clusters of the 2 different clustering
    sns.heatmap(info_long_domain, annot=True, fmt='d', cmap=custom_cmap, ax=ax[0], cbar_kws={'label': 'Number of patients'}, vmin=0)
    ax[0].set_title('Number of common patients between clusters of the 2 different clustering', fontsize=9)

    #Compute percentage
    total = info_long_domain.sum(axis=1)
    percentage_info = info_long_domain.div(total, axis=0)

    # Second heatmap : percentage of common patients between clusters of the 2 different clustering
    sns.heatmap(percentage_info, annot=True, fmt='.0%', cmap=custom_cmap, ax=ax[1], cbar_kws={'label': '% patients with ' + label0 + ' in ' + label1})
    ax[1].set_title('Percentage of common patients between clusters of the 2 different clustering', fontsize=9)

    total = info_long_domain.sum(axis=0)
    percentage_info = info_long_domain.div(total, axis=1) 

    # Third heatmap : percentage of common patients between clusters of the 2 different clustering (transposed)
    sns.heatmap(percentage_info, annot=True, fmt='.0%', cmap=custom_cmap, ax=ax[2], cbar_kws={'label':'% of patients with ' + label1 + ' in ' + label0})
    ax[2].set_title('Percentage of common patients between clusters of the 2 different clustering', fontsize=9)
    
    plt.suptitle(title, fontsize=12)
    plt.show()

def lineplot_comparison(NMF, label0, label1, palette, domain):
    """
    Compare the domain recovery per cluster per time point for two different clustering
    :param palette: color palette to use for coloring label0 (label1 will be differentiated by style)
    """
    plt.figure(figsize=(15, 8))
    sns.lineplot(data=NMF, x="time_in_weeks", y=domain, hue=label0, style=label1, palette=palette, estimator =None, units="Patient") 
    plt.xlabel("Time (in weeks)")
    plt.title(domain + " recovery per cluster per time point")
    plt.show();