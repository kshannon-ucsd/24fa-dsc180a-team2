# LCA Analysis

## Overview
The R script in this folder executes the LCA analysis that was performed in the original [research paper](https://ccforum.biomedcentral.com/articles/10.1186/s13054-019-2486-6#article-info). The script is intended to be ran in RStudio.

---
## Prerequisites

1. **Download R and RStudio**
   
   R and RStudio can be downloaded [here](https://posit.co/download/rstudio-desktop/).

2. **Run necessary scripts**

    There are two scripts that must be ran before this one. Scripts are listed in the order they should be ran. 
    - `sql/data_subset_query_v1.sql`: Gets `subset.csv`
    - `python/lca_proprocessing.py`: Performs necessary data preprocessing before modeling
---

## Key Files
1. `LCA.r` - Performs the LCA analysis

---

## Running the R Script

1. Open `LCA.r` in RStudio
2. Set working directory to directory that contains `subset.csv`
3. Run the script
    