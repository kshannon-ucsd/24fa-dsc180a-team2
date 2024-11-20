# Python Scripts

## Overview
The notebooks in this folder execute the KMeans, Latent Class, and Network Analysis of the MIMIC-III subset generated from the [SQL folder](https://github.com/kshannon-ucsd/24fa-dsc180a-team2/tree/sql-query)

---
## 1. spf1
`spf1.py` tabulates statistics across demographics in the subset. Groups are first broken down by gender, then age, morbidity count, and finally elective vs. non-elective admission.

---
### Key Files
1. `data_subset_query_v1.sql` - Performs the queries to create the subset

### Running the Python Script

1. Open the repository folder on your Python environment of choice
2. Excute the code
3. Ensure that the final csv `demographics.csv` is outputted to the res directory
---
## 2. kmeans

## 3. latent_class

## 4. network_analysis
`network_analysis.py` creates network graphs between morbidities in the subset based on their cooccurrences and how frequently each disorder appears in the subgroup

---
### Key Files
1. `lca_data.csv` - One-hot encoded table containing data on patient age, gender, type of admission (elective or non-elective), and which morbidities they have. 
2. `subgroups.csv` - Non-OHE data with column containing assigned subgroups (1-6) based on initial 7 group LCA and removal of subgroups comprising under 5% of the total population.

---
### Running the Python Script

1. Open the repository folder on your Python environment of choice
2. Excute the code
3. Ensure that the final network images are outputted to the `../../res/_networks` directory
    
