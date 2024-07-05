# TiMeS_WP11
The goal is to give longitudinal assessment of behavioral inter-domains interactions in stroke patients from the TiMeS cohort.
The behavioral domains previously evaluated are the following : Motor, Attention, Executive, Memory, Sensory, Language and Neglect. 
Each domain was evaluated with a battery of tests. This project provides a longitudinal analysis of the results obtained following th mentionned goal.

## Installation
To use this program, simply clone the git repository of the project: 
"git@github.com:coco-2000/WP11_TiMeS.git".

## Folder and files

- The folder *Code* is made of 9 files and contains the code of the project as well as some visualizations as it is mainly composed of jupyter notebooks.
    The different files are :
    - *Final_code2.ipynb* contains data normalization, dimensionality reduction within each domain
    - *Global_visualization.ipynb* which allows the longitudinal visualization of the 4 TiMeS datasets preprocessed and clustered in *Final_code2.ipynb*
    - *Longitudinal_clustering.py* contains functions for longitudinal clustering and cluster comparison.
    - *Longitudinal_clustering_motor.ipynb* which allows the identification of motor evolution's subtrends with kmeans longitudinal clustering
    - *Longitudinal_clustering_attention.ipynb* which allows the identification of attention evolution's subtrends with kmeans longitudinal clustering
    - *Regression.ipynb* which computes the recovery score as a measure of motor recovery and performs a linear regression with acute (T1) scores as independent variables and recovery scores as dependent variable
    - *Cluster_0_comparison.ipynb*
    - *Classification.ipynb*                                                                    
    The folder Aitana contains the file *Final_code.ipynb* a previous version of *Final_code2.ipynb*

- The folder *Data* contains the data of the project. 
    - The different files of this folder are the ones first loaded in the file *Code/Final_code2.ipynb* and *Code/Aitana/Final_code.ipynb*
    - The folder Lisa which contains the data transformed by *Final_code2.ipynb*
    - The folder Longitudinal which contains the data transfornmed and clustered by *Longitudinal_clustering_motor.ipynb*
 
  ## Authors
  Lisa Fleury, Aitana Waelbroeck Boix, Constance de Trogoff
