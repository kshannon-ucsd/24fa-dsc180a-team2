import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import matplotlib.pyplot as plt
import os

df = pd.read_csv('../../data/subset.csv')


data = df[df.columns[3:]]
data = data.drop(columns = ['age_years', 'outtime_icu', 'first_admission_icu'])
qual = ['dbsource', 'gender', 'age_group', 'admission_type', 'first_careunit', 'last_careunit']

quant = ['num_disorders', 'los_icu', 'los_hospital', 'sofa']
data= data.dropna()

preprocessor = ColumnTransformer(transformers= [
    ('num', StandardScaler(), quant), 
    ('cat', OneHotEncoder(), qual)
])

kmeans = KMeans(n_clusters = 6)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('kmeans', kmeans)
])

pipeline.fit(data)
labels = pipeline['kmeans'].labels_


#commented code saves figures to data directory

df['subgroup'] = pd.Series(labels)
morbidities = ['congestive_heart_failure',
       'cardiac_arrhythmias', 'valvular_disease', 'pulmonary_circulation',
       'peripheral_vascular', 'hypertension', 'paralysis',
       'other_neurological', 'chronic_pulmonary', 'diabetes_uncomplicated',
       'diabetes_complicated', 'hypothyroidism', 'renal_failure',
       'liver_disease', 'peptic_ulcer', 'aids', 'lymphoma',
       'metastatic_cancer', 'solid_tumor', 'rheumatoid_arthritis',
       'coagulopathy', 'obesity', 'weight_loss', 'fluid_electrolyte',
       'blood_loss_anemia', 'deficiency_anemias', 'alcohol_abuse',
       'drug_abuse', 'psychoses', 'depression']


# os.makedirs(f"../../res/{subdirectory_name}", exist_ok=True)
for i in range(5):
       df.groupby('subgroup')[morbidities].sum().iloc[i].sort_values(ascending = False)[:5].plot(kind = 'bar')
       plt.title(f'Top 5 Morbidities for Subgroup {i}')
       # plt.savefig(f"../../res/{subdirectory_name}/subgroup_{i}_top_morbidities.png")
    
       # Display the plot
       plt.close()

