# Sepsis Patient Subset

## Overview
The SQL script in this folder is designed to generate a similar subset that Zsolt Zador, Alexander Landry, Michael D. Cusimano, and Nophar Geifam got in their [research paper](https://ccforum.biomedcentral.com/articles/10.1186/s13054-019-2486-6#article-info). The script is intended to be ran with postgreSQL in combination with pgAdmin4.

---
## Prerequisites

1. **Download concepts tables from MIT-LCP/mimic-code GitHub**
   
   The script requires some tables from the `mimic-iii/concepts_progres` folder in the GitHub. You can find the scripts here:
   - [MIT-LCP/mimic-code GitHub](https://github.com/MIT-LCP/mimic-code)

2. **Required tables (Install them in the order listed)**
   - `blood_gas_first_day`
   - `blood_gas_first_dat_arterial`
   - `echo_data`
   - `gcs_first_day`
   - `urine_output_first_day`
   - `ventilation_classification`
   - `ventilation_durations`
   - `ventilation_first_day`
   - `vitals_first_day`
   - `elixhauser_quan`
   - `martin`
   - `oasis`
   - `sofa`
---

## Concepts Tables Setup

 1. Clone the mimic-code repository to a directory of your choosing using the following:
     ```bash
     git clone https://github.com/MIT-LCP/mimic-code.git
     ```
  2. In your terminal, navigate through the mimiciii, concepts_postgres, and which ever subdirectory contains the SQL script for the required tables
  3. Connect to the Database:
     ```bash
     psql -U postgres -d mimic
     ALTER DATABASE mimic SET search_path TO mimiciii;
     ```
  4. Run SQL script, below is an example with `blood_gas_first_day.sql`
     ```bash
     \i blood_gas_first_day.sql
     ```
  - For more detailed instruction, refer to the [README.md](https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iii/concepts#readme) file on MIT's GitHub.
---

## Key Files
1. `data_subset_query_v1.sql` - Performs the queries to create the subset

---

## Running the SQL Script

1. In your terminal, navigate to the sql folder in this repository
2. Connect to Database:
    ```bash
     psql -U postgres -d mimic
     ALTER DATABASE mimic SET search_path TO mimiciii;
     ```
3. Run the SQL script:
    ```bash
     \i data_subset_query_v1.sql
     ```
    