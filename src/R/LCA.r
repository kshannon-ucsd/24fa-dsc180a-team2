library(tidyverse)
library(poLCA)

set.seed(1)

# Load in subset data
df <- read.table('subset.csv', sep = ",", header = 1)

# Load in data to be used in model
lca_data <- read.table('lca_data.csv', sep=",", header = 1) 

# Adding 1 to the all columns in lca_data to allow for it to be passed into model
lca_data <- lca_data + 1

# Define formula for model
f <- cbind(gender, admission_type, age_years, congestive_heart_failure, cardiac_arrhythmias, valvular_disease, pulmonary_circulation, peripheral_vascular, hypertension, paralysis, other_neurological, chronic_pulmonary, diabetes_uncomplicated, diabetes_complicated, hypothyroidism, renal_failure, liver_disease, peptic_ulcer, aids, lymphoma, metastatic_cancer, solid_tumor, rheumatoid_arthritis, coagulopathy, obesity, weight_loss, fluid_electrolyte, blood_loss_anemia, deficiency_anemias, alcohol_abuse, drug_abuse, psychoses, depression) ~ 1

# Create model for 7 classes with intention to remove one later
model_7 <- poLCA(f, lca_data, nclass = 7, nrep = 10)

# Create model for 6 classes
model_6 <- poLCA(f, lca_data, nclass = 6, nrep = 10)

# Find the class posterior probabilities for model7
posterior_prob <- model_7$posterior

# Removing class below 5% from model7 and reassigning it to other classes
reassigned_classes <- apply(posterior_prob, 1, function(class_prob) {
  # Finding which class had the max posterior probability
  original_class <- which.max(class_prob)
  # Class 6 was the class that contained less than 5% of sample
  if (original_class == 6) {
    # Defining the remaining 6 classes
    remaining_class <- c(1, 2, 3, 4, 5, 7)
    # Finding the posterior probabilities for the remaining classes
    remaining_probs <-  class_prob[remaining_class]
    # Reassigns patient to class with highest posterior probability
    reassigned_class <- remaining_class[which.max(remaining_probs)]
  } else {
    # If not class 6, stay in original class
    reassigned_class <- original_class
  }
  return(reassigned_class)
})

# Assign outputs of both models to new columns in subset data
df$reassigned_classes <- reassigned_classes
df$six_classes <- model_6$predclass

# Write result to new csv
write.csv(df, "subgroups.csv", row.names = FALSE)
