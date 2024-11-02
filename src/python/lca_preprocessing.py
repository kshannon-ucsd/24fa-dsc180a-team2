import pandas as pd

def age_buckets(df):
    """
    Takes in a DataFrame and returns columns that one hot encode which age group a patient 
    is in.

    Args:
        df (DataFrame): DataFrame.

    Returns:
        A DataFrame that has additional columns that indicate which age bucket a patient is in.
        1 implies membership and 0 non-membership.
    """
    age_one_hot_encoded = pd.get_dummies(df["age_group"], dtype = "int", prefix = "age")
    age_one_hot_encoded.columns = [col.replace("-", "_") for col in age_one_hot_encoded]
    return pd.concat([df.drop(columns = "age_group"), age_one_hot_encoded], axis = 1)

def adjust_gender(gender):
    """
    Takes in whether a person is male or female and encodes them as 0 and 1 respectively.

    Args:
        gender (str): String that represents if a patient is male or female.

    Returns:
        Integer that indicates whether a patient is male or female. If the patient is male, 0.  
        If the patient is female, 1.
    ---
    """
    if gender == "M":
        return 0
    elif gender == "F":
        return 1
    
def adjust_admission(admission):
    """
    Takes in whether a person was admitted non-electively or electively and encodes them as 0 and 1 
    respectively

    Args:
        admission (str): String that represents if a patient was admitted electively or 
                         non-electively.

    Returns:
        Integer that indicates how the patient was admitted. If the patient was admitted 
        non-electively, 0. If the patient was admitted electively, 1.
    ---
    """
    if admission == "Non-elective":
        return 0
    elif admission == "Elective":
        return 1

def necessary_columns(df):
    """
    Takes in a DataFrame and drops columns that aren't necessary for the LCA.
    
    Args:
        df (DataFrame): DataFrame.
    
    Returns:
        DataFrame with only the necessary columns needed for LCA.
    """
    return df.drop(columns = ["subject_id", "hadm_id", "icustay_id", "dbsource", "age_years", 
                              "num_disorders", "first_careunit", "last_careunit", 
                              "first_admission_icu", "outtime_icu", "los_icu", "los_hospital", 
                              "sofa", "has_chartevents_data", "hospital_expire_flag", 
                              "comorbidity_score"])

def main():
    """
    This script does the following:
    1. Reads data from the CSV file
    2. Preprocesses the data to make it suitable for LCA
    3. Saves the result into a new CSV file
    """
    subset = pd.read_csv("subset.csv")
    age_transform = age_buckets(subset)
    gender_transform = age_transform.assign(gender = age_transform["gender"].apply(adjust_gender))
    admission_transform = gender_transform.assign(
        admission_type = gender_transform["admission_type"].apply(adjust_admission)
    )
    lca_data = necessary_columns(admission_transform)
    lca_data.to_csv("lca_data.csv")

if __name__ == "__main__":
    main()