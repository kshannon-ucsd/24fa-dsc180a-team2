library(poLCA)

# Set work directory to data folder in repository
setwd("")

set.seed(1)

df <- read.table('subset.csv', sep = ",", header = 1)

lca_data <- read.table('lca_data.csv', sep=",", header = 1) 

# Add 1 to each column in lca_data to allow it to be inputted into model
lca_data <- lca_data + 1

# Define formula for LCA analysis
f <- cbind(gender, admission_type, age_years, congestive_heart_failure, cardiac_arrhythmias, valvular_disease, pulmonary_circulation, peripheral_vascular, hypertension, paralysis, other_neurological, chronic_pulmonary, diabetes_uncomplicated, diabetes_complicated, hypothyroidism, renal_failure, liver_disease, peptic_ulcer, aids, lymphoma, metastatic_cancer, solid_tumor, rheumatoid_arthritis, coagulopathy, obesity, weight_loss, fluid_electrolyte, blood_loss_anemia, deficiency_anemias, alcohol_abuse, drug_abuse, psychoses, depression) ~ 1

# Initialize the model
model_7 <- poLCA(f, lca_data, nclass = 7, nrep = 10)

# Define posterior probabilities generated from model
posterior_prob <- model_7$posterior

# Removes a class and reassigns that class to other classes
reassigned_classes <- apply(posterior_prob, 1, function(class_prob) {
  # Find out which class a patient was originally classified as
  original_class <- which.max(class_prob)
  # Remove class 6 and reassign
  if (original_class == 6) {
    # Define the remaining classes
    remaining_class <- c(1, 2, 3, 4, 5, 7)
    # Define the posterior probabilities for the other classes
    remaining_probs <-  class_prob[remaining_class]
    # Reassign patient to class with highest posterior probability
    reassigned_class <- remaining_class[which.max(remaining_probs)]
    # Maintain other groups
  } else {
    reassigned_class <- original_class
  }
  # Return final group
  return(reassigned_class)
})

# Add new column to data that classifies patients
df$reassigned_classes <- reassigned_classes

# Save result to subgroups.csv in data folder
write.csv(df, "subgroups.csv", row.names = FALSE)
