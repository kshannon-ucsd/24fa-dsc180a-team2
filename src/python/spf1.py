#!/usr/bin/env python
# coding: utf-8

# ## Supplementary Figure 1 Recreation

# #### Loading the subset from Postgres local server

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('sqlalchemy')
install('psycopg2')
install('pandas')

from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import os
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/mimic')
os.makedirs('../../res/_demographics', exist_ok=True)

inspector = inspect(engine)
subset_query = open('../sql/data_subset_query_v1.sql', 'r').read()

df = pd.read_sql_query(subset_query, engine)

# Drop extraneous columns
df = df.loc[:,~df.columns.duplicated()]

df['admission_type'].unique()

morbidities = set(['congestive_heart_failure',
       'cardiac_arrhythmias', 'valvular_disease', 'pulmonary_circulation',
       'peripheral_vascular', 'hypertension', 'paralysis',
       'other_neurological', 'chronic_pulmonary', 'diabetes_uncomplicated',
       'diabetes_complicated', 'hypothyroidism', 'renal_failure',
       'liver_disease', 'peptic_ulcer', 'aids', 'lymphoma',
       'metastatic_cancer', 'solid_tumor', 'rheumatoid_arthritis',
       'coagulopathy', 'obesity', 'weight_loss', 'fluid_electrolyte',
       'blood_loss_anemia', 'deficiency_anemias', 'alcohol_abuse',
       'drug_abuse', 'psychoses', 'depression'])

# Creating Morbidity Count Column
def count_morbidities(row, morbidities):
    count = 0
    for morbidity in morbidities:
        if row[morbidity] == 1:
            count += 1
    return count


df['num_morbidity'] = df.apply(count_morbidities, args=(morbidities,), axis=1)

## All patient statistics
num_patients = df.shape[0]

median_morbidities = df['num_morbidity'].median()
morbidities_Q1 = df['num_morbidity'].quantile(0.25)
morbidities_Q3 = df['num_morbidity'].quantile(0.75)

prop_with_multiple_morbidities = (df[df['num_morbidity'] > 1].shape[0] / num_patients)
CI_percent_with_multiple_morbidities = 1.96 * ((prop_with_multiple_morbidities) * (1 - prop_with_multiple_morbidities) / num_patients) ** 0.5

sofa_score = df['sofa'].mean()
CI_sofa_score = 1.96 * df['sofa'].std() / num_patients ** 0.5

LOS_score_icu = df['los_icu'].mean()
CI_LOS_score_icu = 1.96 * df['los_icu'].std() / num_patients ** 0.5

LOS_score_hospital = df['los_hospital'].mean()
CI_LOS_score_hospital = 1.96 * df['los_hospital'].std() / num_patients ** 0.5

prop_mortality = df['hospital_expire_flag'].mean()
CI_mortality = 1.96 * (prop_mortality * (1 - prop_mortality) / num_patients) ** 0.5

print(f'Number of patients: {num_patients}')
print(f'Median number of morbidities: {median_morbidities} (Q1: {morbidities_Q1}, Q3: {morbidities_Q3})')
print(f'Percent of patients with multiple morbidities: {prop_with_multiple_morbidities * 100:.2f}% ± {CI_percent_with_multiple_morbidities * 100:.2f}')
print(f'Mean SOFA score: {sofa_score:.2f} ± {CI_sofa_score:.2f}')
print(f'Mean Length of Stay (ICU): {LOS_score_icu:.2f} ± {CI_LOS_score_icu:.2f}')
print(f'Mean Length of Stay (Hospital): {LOS_score_hospital:.2f} ± {CI_LOS_score_hospital:.2f}')
print(f'Percent Mortality: {prop_mortality * 100:.2f}% ± {CI_mortality * 100:.2f}')

## Creating a function for each statistic

def get_num_patients(df):
    return df.shape[0]

def get_median_morbidities(df):
    return df['num_morbidity'].median()

def get_morbidities_CI(df):
    morbidities = df['num_morbidity']
    morbidities_Q1 = morbidities.quantile(0.25)
    morbidities_Q3 = morbidities.quantile(0.75)
    return morbidities_Q1, morbidities_Q3

def get_prop_with_multiple_morbidities(df):
    num_patients = get_num_patients(df)
    prop_with_multiple_morbidities = (df[df['num_morbidity'] > 1].shape[0] / num_patients)
    CI_percent_with_multiple_morbidities = 1.96 * ((prop_with_multiple_morbidities) * (1 - prop_with_multiple_morbidities) / num_patients) ** 0.5
    return prop_with_multiple_morbidities, CI_percent_with_multiple_morbidities

def get_sofa_score(df):
    return df['sofa'].mean()

def get_sofa_CI(df):
    num_patients = get_num_patients(df)
    CI_sofa_score = 1.96 * df['sofa'].std() / num_patients ** 0.5
    return CI_sofa_score

def get_LOS_icu(df):
    return df['los_icu'].mean()

def get_LOS_icu_CI(df):
    num_patients = get_num_patients(df)
    CI_LOS_score_icu = 1.96 * df['los_icu'].std() / num_patients ** 0.5
    return CI_LOS_score_icu

def get_LOS_hospital(df):
    return df['los_hospital'].mean()

def get_LOS_hospital_CI(df):
    num_patients = get_num_patients(df)
    CI_LOS_score_hospital = 1.96 * df['los_hospital'].std() / num_patients ** 0.5
    return CI_LOS_score_hospital

def get_mortality(df):
    return df['hospital_expire_flag'].mean()

def get_mortality_CI(df):
    num_patients = get_num_patients(df)
    prop_mortality = df['hospital_expire_flag'].mean()
    CI_mortality = 1.96 * (prop_mortality * (1 - prop_mortality) / num_patients) ** 0.5
    return CI_mortality


# In[15]:


# Creating a dictionary of statistics
num_patients = get_num_patients(df)
median_morbidities, morbidities_CI = get_median_morbidities(df), get_morbidities_CI(df)
prop_with_multiple_morbidities, CI_percent_with_multiple_morbidities = get_prop_with_multiple_morbidities(df)
sofa_score, sofa_CI  = get_sofa_score(df), get_sofa_CI(df)
LOS_icu, LOS_icu_CI = get_LOS_icu(df), get_LOS_icu_CI(df)
LOS_hospital, LOS_hospital_CI = get_LOS_hospital(df), get_LOS_hospital_CI(df)
mortality, mortality_CI = get_mortality(df), get_mortality_CI(df)
        
rows = [{'Group': 'All Patients', 
        'Number of Patients (%)': num_patients,
        'Median Morbidity Count (IQR)': f'{median_morbidities} ({morbidities_CI[0]}, {morbidities_CI[1]})',
        'Percent (95% CI) with multimorbidity': f'{prop_with_multiple_morbidities * 100:.2f}% ± {CI_percent_with_multiple_morbidities * 100:.2f}',
        'SOFA Score (95% CI)': f'{sofa_score:.2f} ± {sofa_CI:.2f}',
        'LOS ICU (95% CI)': f'{LOS_icu:.2f} ± {LOS_icu_CI:.2f}',
        'LOS Hospital (95% CI)': f'{LOS_hospital:.2f} ± {LOS_hospital_CI:.2f}',
        'Percent Mortality (95% CI)': f'{mortality * 100:.2f}% ± {mortality_CI * 100:.2f}'}]

gender = ['M', 'F']

age_groups = ['16-24', '25-44', '45-64', '65-84', '85-95']

number_of_disorders = [0, 1, 2, 3, 4, 5, 6, 7, '>8']

admission_type = ['Elective', 'Non-elective']

for grp in gender:
    gender_df = df[df['gender'] == grp]
    
    num_patients = get_num_patients(gender_df)
    median_morbidities, morbidities_CI = get_median_morbidities(gender_df), get_morbidities_CI(gender_df)
    prop_with_multiple_morbidities, CI_percent_with_multiple_morbidities = get_prop_with_multiple_morbidities(gender_df)
    sofa_score, sofa_CI  = get_sofa_score(gender_df), get_sofa_CI(gender_df)
    LOS_icu, LOS_icu_CI = get_LOS_icu(gender_df), get_LOS_icu_CI(gender_df)
    LOS_hospital, LOS_hospital_CI = get_LOS_hospital(gender_df), get_LOS_hospital_CI(gender_df)
    mortality, mortality_CI = get_mortality(gender_df), get_mortality_CI(gender_df)
    
    rows.append({'Group': grp,
                'Number of Patients (%)': num_patients,
                'Median Morbidity Count (IQR)': f'{median_morbidities} ({morbidities_CI[0]}, {morbidities_CI[1]})',
                'Percent (95% CI) with multimorbidity': f'{prop_with_multiple_morbidities * 100:.2f}% ± {CI_percent_with_multiple_morbidities * 100:.2f}',
                'SOFA Score (95% CI)': f'{sofa_score:.2f} ± {sofa_CI:.2f}',
                'LOS ICU (95% CI)': f'{LOS_icu:.2f} ± {LOS_icu_CI:.2f}',
                'LOS Hospital (95% CI)': f'{LOS_hospital:.2f} ± {LOS_hospital_CI:.2f}',
                'Percent Mortality (95% CI)': f'{mortality * 100:.2f}% ± {mortality_CI * 100:.2f}'})

for grp in age_groups:
    age_group_df = df[df['age_group'] == grp]
    
    num_patients = get_num_patients(age_group_df)
    median_morbidities, morbidities_CI = get_median_morbidities(age_group_df), get_morbidities_CI(age_group_df)
    prop_with_multiple_morbidities, CI_percent_with_multiple_morbidities = get_prop_with_multiple_morbidities(age_group_df)
    sofa_score, sofa_CI  = get_sofa_score(age_group_df), get_sofa_CI(age_group_df)
    LOS_icu, LOS_icu_CI = get_LOS_icu(age_group_df), get_LOS_icu_CI(age_group_df)
    LOS_hospital, LOS_hospital_CI = get_LOS_hospital(age_group_df), get_LOS_hospital_CI(age_group_df)
    mortality, mortality_CI = get_mortality(age_group_df), get_mortality_CI(age_group_df)
    
    rows.append({'Group': grp,
                'Number of Patients (%)': num_patients,
                'Median Morbidity Count (IQR)': f'{median_morbidities} ({morbidities_CI[0]}, {morbidities_CI[1]})',
                'Percent (95% CI) with multimorbidity': f'{prop_with_multiple_morbidities * 100:.2f}% ± {CI_percent_with_multiple_morbidities * 100:.2f}',
                'SOFA Score (95% CI)': f'{sofa_score:.2f} ± {sofa_CI:.2f}',
                'LOS ICU (95% CI)': f'{LOS_icu:.2f} ± {LOS_icu_CI:.2f}',
                'LOS Hospital (95% CI)': f'{LOS_hospital:.2f} ± {LOS_hospital_CI:.2f}',
                'Percent Mortality (95% CI)': f'{mortality * 100:.2f}% ± {mortality_CI * 100:.2f}'})
    
for grp in number_of_disorders:
    if grp == '>8':
        disorder_df = df[df['num_morbidity'] > 8]
    else:
        disorder_df = df[df['num_morbidity'] == grp]
    
    num_patients = get_num_patients(disorder_df)
    median_morbidities, morbidities_CI = get_median_morbidities(disorder_df), get_morbidities_CI(disorder_df)
    prop_with_multiple_morbidities, CI_percent_with_multiple_morbidities = get_prop_with_multiple_morbidities(disorder_df)
    sofa_score, sofa_CI  = get_sofa_score(disorder_df), get_sofa_CI(disorder_df)
    LOS_icu, LOS_icu_CI = get_LOS_icu(disorder_df), get_LOS_icu_CI(disorder_df)
    LOS_hospital, LOS_hospital_CI = get_LOS_hospital(disorder_df), get_LOS_hospital_CI(disorder_df)
    mortality, mortality_CI = get_mortality(disorder_df), get_mortality_CI(disorder_df)
    
    rows.append({'Group': grp,
                'Number of Patients (%)': num_patients,
                'Median Morbidity Count (IQR)': f'{median_morbidities} ({morbidities_CI[0]}, {morbidities_CI[1]})',
                'Percent (95% CI) with multimorbidity': f'{prop_with_multiple_morbidities * 100:.2f}% ± {CI_percent_with_multiple_morbidities * 100:.2f}',
                'SOFA Score (95% CI)': f'{sofa_score:.2f} ± {sofa_CI:.2f}',
                'LOS ICU (95% CI)': f'{LOS_icu:.2f} ± {LOS_icu_CI:.2f}',
                'LOS Hospital (95% CI)': f'{LOS_hospital:.2f} ± {LOS_hospital_CI:.2f}',
                'Percent Mortality (95% CI)': f'{mortality * 100:.2f}% ± {mortality_CI * 100:.2f}'})
    
for grp in admission_type:
    admission_type_df = df[df['admission_type'] == grp]
    
    num_patients = get_num_patients(admission_type_df)
    median_morbidities, morbidities_CI = get_median_morbidities(admission_type_df), get_morbidities_CI(admission_type_df)
    prop_with_multiple_morbidities, CI_percent_with_multiple_morbidities = get_prop_with_multiple_morbidities(admission_type_df)
    sofa_score, sofa_CI  = get_sofa_score(admission_type_df), get_sofa_CI(admission_type_df)
    LOS_icu, LOS_icu_CI = get_LOS_icu(admission_type_df), get_LOS_icu_CI(admission_type_df)
    LOS_hospital, LOS_hospital_CI = get_LOS_hospital(admission_type_df), get_LOS_hospital_CI(admission_type_df)
    mortality, mortality_CI = get_mortality(admission_type_df), get_mortality_CI(admission_type_df)
    
    rows.append({'Group': grp,
                'Number of Patients (%)': num_patients,
                'Median Morbidity Count (IQR)': f'{median_morbidities} ({morbidities_CI[0]}, {morbidities_CI[1]})',
                'Percent (95% CI) with multimorbidity': f'{prop_with_multiple_morbidities * 100:.2f}% ± {CI_percent_with_multiple_morbidities * 100:.2f}',
                'SOFA Score (95% CI)': f'{sofa_score:.2f} ± {sofa_CI:.2f}',
                'LOS ICU (95% CI)': f'{LOS_icu:.2f} ± {LOS_icu_CI:.2f}',
                'LOS Hospital (95% CI)': f'{LOS_hospital:.2f} ± {LOS_hospital_CI:.2f}',
                'Percent Mortality (95% CI)': f'{mortality * 100:.2f}% ± {mortality_CI * 100:.2f}'})

res = pd.DataFrame(rows)

res.to_csv('../../res/_demographics/demographics.csv', index=False)

