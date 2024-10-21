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
	WHERE i.age_years >= 16 
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
	SELECT *
	FROM first_admissions_merge AS f
	JOIN (
	SELECT s.subject_id, s.icustay_id, s.sofa
	FROM sofa AS s
	) AS s on f.icustay_id = s.icustay_id
)

-- Merge with elixhauser_quan to get information on elixhauser index
SELECT *
FROM sofa_score AS s
JOIN elixhauser_quan AS e ON e.hadm_id = s.hadm_id;


