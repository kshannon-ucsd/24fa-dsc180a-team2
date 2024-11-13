import pandas as pd

def adjust_age(age):
    """
    Takes in an age and subtracts 1 from it.

    Subtraction is done to ensure that data is ready for LCA. The value 1 needs to be added across 
    all columns for it to be a valid input so this offsets that addition.

    Args:
        age (int): Integer that represents someone's age in years.

    Returns:
        Integer that represents someone's age subtracted by 1.
    """
    return age - 1

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
    return df.drop(columns = ["subject_id", "hadm_id", "icustay_id", "dbsource", "age_group", 
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
    subset = pd.read_csv("/Users/ojasvashishtha/subset.csv")
    age_transform = subset.assign(age_years = subset["age_years"].apply(adjust_age))
    gender_transform = age_transform.assign(gender = age_transform["gender"].apply(adjust_gender))
    admission_transform = gender_transform.assign(
        admission_type = gender_transform["admission_type"].apply(adjust_admission)
    )
    lca_data = necessary_columns(admission_transform)
    lca_data.to_csv("lca_data.csv")

if __name__ == "__main__":
    main()