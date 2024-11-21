# Sepsis Patient Subset

## Overview
The R script in this folder is designed to perform the LCA analysis that Zsolt Zador, Alexander Landry, Michael D. Cusimano, and Nophar Geifam did in their [research paper](https://ccforum.biomedcentral.com/articles/10.1186/s13054-019-2486-6#article-info). The script is intended to be ran with in R and in RStudio.

---
## Prerequisites

1. **Download R and RStudio**
   
   You can download R and RStudio here:
   - [R/Rstudio](https://posit.co/download/rstudio-desktop/)

2. **Run the Required Scripts**

   Before running the script in this file, you must run the following scripts in order:
   - `data_subset_query_v1.sql`
   - `lca_preproccessing.py`
---

## Concepts Tables Setup

  1. Open `LCA.r` in RStudio
  2. Set the work directory to be the data file in this repository
  3. Run the R script by clicking the source button
---

## Key Files
1. `LCA.R` - Performs the LCA analysis to separate the patients into 6 different classes and saves output to `data` folder under `subgroups.csv`

---

## Running the SQL Script

  1. Open `LCA.r` in RStudio
  2. Set the work directory to be the data file in this repository
  3. Run the R script by clicking the source button
    