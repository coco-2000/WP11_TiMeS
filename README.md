# TiMeS_WP11
This study is based on the TiMeS dataset, which is a longitudinal evaluation of several domains over 4 time-points : first week, third week, third month and 1 year after the stroke.

The goal is to give longitudinal assessment of behavioral inter-domains interactions in stroke patients from the TiMeS cohort.
The behavioral domains previously evaluated are the following : Motor, Attention, Executive, Memory, Sensory, Language and Neglect. 
Each domain was evaluated with a battery of tests. This project provides a longitudinal analysis of the results obtained following the mentionned goal.

## Installation
To use this program, simply clone the git repository of the project: 
"git@github.com:coco-2000/WP11_TiMeS.git".

## Folder and files

- The folder *Code* is made of 9 files and contains the code of the project as well as some visualizations as it is mainly composed of jupyter notebooks.
    The different files are :
    - *Final_code2.ipynb* contains data normalization, test selection and dimensionality reduction within each domain as well as multi-domains kmeans clustering at each time point.
      This file provides 4 outputs : a transformed and clustered dataset for each one the 4 timepoints, saved in the folder *Data*
    - *without_NMF.ipynb*. Same code as Final_code2.ipynb but with MOCA behavioural tests and Fugi_Meyer test for the motor domain or MOCA_total test for behavioural tests and Fugi_Meyer. (NMF not needed)
      This file also provides 4 outputs : a transformed and clustered dataset for each one the 4 timepoints, saved in the folder *Data*
    - *Global_visualization.ipynb* which allows the longitudinal visualization of the 4 TiMeS datasets preprocessed and clustered in *Final_code2.ipynb*
    - *Longitudinal_clustering.py* contains functions for longitudinal clustering and cluster comparison.
    - *Longitudinal_clustering_motor.ipynb* which allows the identification of motor evolution's subtrends with kmeans longitudinal clustering. Results are saved under the folder *Data/Longitudinal*.
    - *Longitudinal_clustering_attention.ipynb* which allows the identification of attention evolution's subtrends with kmeans longitudinal clustering.
    - *Regression.ipynb* which computes the recovery score as a measure of motor recovery and performs a linear regression with acute (T1) scores as independent variables and recovery scores as dependent variable to study predictors.
      This file takes as input results in *Data/Longitudinal*
    - *Classification.ipynb* which performs a classification with acute (T1) scores as independent variables and results of the longitudinal motor clustering as labels from *Longitudinal_clustering_motor.ipynb*, to study predictors.
    - *Cluster_0_comparison.ipynb*  clustering comparison with/without last score test for language & with merged/seperate executive and memory cognitive domains and clustering comparison with MOCA total only for cognitive vs with every MOCA tests for         cognitive (Fugi Meyer test used for motor performance)
                                                              
    The folder Aitana contains the file *Final_code.ipynb* a previous version of *Final_code2.ipynb*

- The folder *Data* contains the data of the project. 
    - The different files of this folder are the ones first loaded in the file *Code/Final_code2.ipynb* and *Code/Aitana/Final_code.ipynb*
    - The folder *Lisa* which contains the data transformed by *Final_code2.ipynb*
    - The folder *Longitudinal* which contains the data transfornmed and clustered by *Longitudinal_clustering_motor.ipynb*

## Important Note :
Longitudinal clustering of other domains can be perforned as in *Longitudinal_clustering_motor.ipynb* and *Longitudinal_clustering_attention.ipynb* with the functions taken from *Longitudinal_clustering.py*

## Order of files to be compiled
- *Final_code2.ipynb* has to be run before *Global_visualization.ipynb*, *Longitudinal_clustering_motor.ipynb*, and *Longitudinal_clustering_attention.ipynb*
- *Final_code2.ipynb* and *without_NMF.ipynb* have to be run with specific boolean parameters before *Cluster_0_comparison.ipynb*
- *Longitudinal_clustering_motor.ipynb* has to be run before *Regression.ipynb* and *Classification.ipynb* 

## Authors
Lisa Fleury, Aitana Waelbroeck Boix, Constance de Trogoff
