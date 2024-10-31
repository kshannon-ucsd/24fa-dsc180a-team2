# 24fa-dsc180a-team2

# Sepsis - Using Clinical Healthcare Data Science to Identify and Combat an Infectious Killer

## Data Science Capstone Project - DSC 180AB  

### Project Overview

This project aims to explore severe infection management and detection in inpatient ICU care, with a focus on sepsis, using the MIMIC-III dataset. In this phase, we focus on reproducing the results of the paper:
*Zador, Z., Landry, A., Cusimano, M.D., et al. Multimorbidity states associated with higher mortality rates in organ dysfunction and sepsis: a data-driven analysis in critical care.* (2019). Available at: [https://doi.org/10.1186/s13054-019-2486-6](https://doi.org/10.1186/s13054-019-2486-6)
Our goal is to affirm the original conclusions and methodologies around critical care patient subgroups, particularly those at higher risk of mortality due to organ dysfunction and sepsis. 

---

## Accessing the MIMIC Dataset

The MIMIC-III database is a freely accessible, de-identified dataset containing detailed clinical data for ICU patients. To access the data, follow these steps:

1. **Create a PhysioNet account** at [https://physionet.org](https://physionet.org) using your UCSD email.
2. Complete the required **CITI training course** for human research protection.
3. Upload your training certificate to PhysioNet.
4. **Apply for credentialing** on PhysioNet, listing Kyle Shannon (kshannon@ucsd.edu) as your supervisor.
5. Once approved, sign the **Data Use Agreement** for both MIMIC-III and MIMIC-IV datasets.
6. Download the zipped MIMIC-III tables to a preferred directory. 

For more detailed instructions, see the official MIMIC-III documentation at [https://mimic.physionet.org](https://mimic.physionet.org).

---
## Prerequisites

1. **A Code Editor/IDE That Supports Jupyter Notebooks**
   
   We opted to use VS Code for this project. You can download it here:
   - [VS Code Download](https://code.visualstudio.com/)
     
   Note: Editing notebooks with VSCode requires the <ins>Jupyter Notebook extension</ins> to be installed
3. **A Code Editor/IDE For R**
   
   We opted to use RStudio for this project. You can download it here:
   - [RStudio Download](https://posit.co/download/rstudio-desktop/)
5. **PostgreSQL Client**
   
   If you want to connect to the PostgreSQL database from your local machine, make sure to install a PostgreSQL client:
   - For macOS:  
     ```bash
     brew install postgresql
     ```
   - For Windows: Install via [PostgreSQL Windows Installer](https://www.postgresql.org/download/windows/).
7. **PhysioNet Account**  
   You need a PhysioNet account to access the MIMIC dataset. Complete the credentialing process on [PhysioNet](https://physionet.org) and the required CITI training.
---

## Development Environment Setup

### 1. PostgreSQL Database Setup

- **Create the MIMIC Database**:
  1. Clone the mimic-code repository to a directory of your choosing using the following:
     ```bash
     git clone https://github.com/MIT-LCP/mimic-code.git
     ```
  2. In your terminal, navigate through the mimiciii, buildmimic, and postgres subdirectories
     
  4. To create MIMIC-III from a set of zipped/unzipped CSV files in the "/path/to/data/" directory, run the following command:
     ```bash
     $ make create-user mimic datadir="/path/to/data/"
     ```
  
      Alternatively, if you would like to create the database with non-default parameters, run the following:
  
      ```bash
      $ make create-user mimic datadir="/path/to/data/" DBNAME="my_db" DBPASS="my_pass" DBHOST="192.168.0.1"
      ```
  4. The Makefile's default parameters creates a postgres database with the following setup:

      Database name: mimic
     
      User name: postgres
     
      Password: postgres
     
      Schema: mimiciii
     
      Host: none (defaults to localhost)
     
      Port: none (defaults to 5432)

      For more detailed instructions on setting up the MIMIC-III database in Postgres, refer to [the mimic-code README.](https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iii/buildmimic/postgres)
  

- **Connect to the Database**:  
  ```bash
  psql -U postgres -d mimic
  ALTER DATABASE mimic SET search_path TO mimiciii;
  ```
---

## pgAdmin 4 Database Access

You can also manage the PostgreSQL database using pgAdmin. Here’s how to connect:

1. Open pgAdmin and create a new PostgreSQL connection.
2. Use the following settings:
   - Host: `localhost`
   - Port: `5432`
   - Database: `mimic`
   - Username: `postgres`
   - Password: `postgres`
     
---

### Team Members:
- Ojas Vashishtha 
- Raine Hoang
- Rohan Duvur
