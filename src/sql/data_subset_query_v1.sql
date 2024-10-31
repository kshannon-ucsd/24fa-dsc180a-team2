-- SQL query to get the subset the original research paper used for their study

-- Calculate ages for people in the ICU
SET SEARCH_PATH =  mimiciii;

WITH icu_age AS (
     SELECT i.subject_id, i.hadm_id, i.icustay_id, i.dbsource, i.first_careunit, i.last_careunit, i.intime, i.outtime, i.los, DATE_PART('YEAR', AGE(i.intime, p.dob)) as age_years, p.gender
     FROM icustays AS i
     JOIN (
		SELECT p.subject_id, p.dob, p.gender
          FROM patients AS p
	 ) AS p ON i.subject_id = p.subject_id
),

-- Calculate the different age groups for people in the ICU
icu_age_groups AS (
    SELECT *,
    CASE
    	WHEN i.age_years >= 16 AND i.age_years <= 24 THEN '16-24'
		WHEN i.age_years >= 25 AND i.age_years <= 44 THEN '25-44'
		WHEN i.age_years >=45 AND i.age_years <= 64 THEN '45-64'
		WHEN i.age_years >= 65 AND i.age_years <= 84 THEN '65-84'
		ELSE '85-95'
	END as age_group
	FROM icu_age AS i
	WHERE i.age_years >= 16 AND i.age_years < 300
),

-- Find the rows that corresponds to a patient's first admission to the ICU
first_admissions AS(
	SELECT i1.subject_id, i1.hadm_id, i1.icustay_id, i1.dbsource, i1.first_careunit, i1.last_careunit, i2.first_admission, i1.outtime, i1.los, i1.age_years, i1.age_group, i1.gender
	FROM icu_age_groups AS i1
	JOIN(
		SELECT ia.subject_id, MIN(ia.intime) AS first_admission
		FROM icu_age_groups AS ia
		GROUP BY ia.subject_id
	) AS i2 ON i1.subject_id = i2.subject_id
	AND i1.intime = i2.first_admission
),

-- Merging with admissions table to get additional information and figure out patient's length of stay in hospital
first_admissions_merge AS (
	SELECT f.subject_id, f.hadm_id, f.icustay_id, f.dbsource, f.first_careunit, f.last_careunit, f.first_admission, f.outtime, f.los AS los_icu, f.age_years, f.age_group, f.gender,
	CASE
		WHEN a.admission_type = 'ELECTIVE' THEN 'Elective'
		ELSE 'Non-elective'
	END AS admission_type,ROUND(extract(epoch FROM a.dischtime - a.admittime) / 86400, 2) AS los_hospital, a.hospital_expire_flag, a.has_chartevents_data
	FROM first_admissions AS f
	JOIN (
		SELECT a.subject_id, a.hadm_id, a.admission_type, a.hospital_expire_flag, a.has_chartevents_data, a.admittime, a.dischtime
		FROM admissions AS a
	) AS a ON a.subject_id = f.subject_id AND
	a.hadm_id = f.hadm_id
),

-- Merge with sofa table to get information on patient's sofa scores
sofa_score AS (
	SELECT f.subject_id, f.hadm_id, f.icustay_id, f.dbsource, f.first_careunit, f.last_careunit, f.first_admission, f.outtime, f.los_icu, f.los_hospital, f.age_years, f.age_group, f.admission_type, f.hospital_expire_flag, f.has_chartevents_data, f.gender, s.sofa
	FROM first_admissions_merge AS f
	JOIN (
	SELECT s.subject_id, s.icustay_id, s.sofa
	FROM sofa AS s
	) AS s on f.icustay_id = s.icustay_id
),

-- Create table that sums up elixhauser index to create comorbidity index
elixhauser_sum AS (
	SELECT *, e.congestive_heart_failure + e.cardiac_arrhythmias + e.valvular_disease + e.pulmonary_circulation + e.peripheral_vascular + e.hypertension + e.paralysis + e.other_neurological + e.chronic_pulmonary + e.diabetes_uncomplicated + e.diabetes_complicated + e.hypothyroidism + e.renal_failure + e.liver_disease + e.peptic_ulcer + e.aids + e.lymphoma + e.metastatic_cancer + e.solid_tumor + e.rheumatoid_arthritis + e.coagulopathy + e.obesity + e.weight_loss + e.fluid_electrolyte + e.blood_loss_anemia + e.deficiency_anemias + e.alcohol_abuse + e.drug_abuse + e.psychoses + e.depression AS score_sum
	FROM elixhauser_quan AS e
),

-- Merge with elixhauser to obtain final subset of the data
subset AS (
	SELECT s.subject_id, s.hadm_id, s.icustay_id, s.dbsource, s.gender, s.age_years, s.age_group, s.admission_type, e.score_sum AS num_disorders, s.first_careunit, s.last_careunit, s.first_admission AS first_admission_icu, s.outtime AS outtime_icu, s.los_icu, s.los_hospital, s.sofa, s.has_chartevents_data, s.hospital_expire_flag, e.congestive_heart_failure, e.cardiac_arrhythmias, e.valvular_disease, e.pulmonary_circulation, e.peripheral_vascular, e.hypertension, e.paralysis, e.other_neurological, e.chronic_pulmonary, e.diabetes_uncomplicated, e.diabetes_complicated, e.hypothyroidism, e.renal_failure, e.liver_disease, e.peptic_ulcer, e.aids, e.lymphoma, e.metastatic_cancer, e.solid_tumor, e.rheumatoid_arthritis, e.coagulopathy, e.obesity, e.weight_loss, e.fluid_electrolyte, e.blood_loss_anemia, e.deficiency_anemias, e.alcohol_abuse, e.drug_abuse, e.psychoses, e.depression,
		CASE
			WHEN e.score_sum = 0 THEN '0'
			WHEN e.score_sum = 1 THEN '1'
			WHEN e.score_sum = 2 THEN '2'
			WHEN e.score_sum = 3 THEN '3'
			WHEN e.score_sum = 4 THEN '4'
			WHEN e.score_sum = 5 THEN '5'
			WHEN e.score_sum = 6 THEN '6'
			WHEN e.score_sum = 7 THEN '7'
			ELSE '>8'
		END AS comorbidity_score 
	FROM sofa_score AS s
	JOIN elixhauser_sum AS e ON s.hadm_id = e.hadm_id
	WHERE e.score_sum IS NOT NULL
)

SELECT *
FROM subset AS s;


