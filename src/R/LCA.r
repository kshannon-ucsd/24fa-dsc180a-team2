library(tidyverse)
library(poLCA)

set.seed(1)

df <- read.table('subset.csv', sep = ",", header = 1)

lca_data <- read.table('lca_data.csv', sep=",", header = 1) 

lca_data <- lca_data + 1

f <- cbind(gender, admission_type, age_16_24, age_25_44, age_45_64, age_65_84, age_85_95, congestive_heart_failure, cardiac_arrhythmias, valvular_disease, pulmonary_circulation, peripheral_vascular, hypertension, paralysis, other_neurological, chronic_pulmonary, diabetes_uncomplicated, diabetes_complicated, hypothyroidism, renal_failure, liver_disease, peptic_ulcer, aids, lymphoma, metastatic_cancer, solid_tumor, rheumatoid_arthritis, coagulopathy, obesity, weight_loss, fluid_electrolyte, blood_loss_anemia, deficiency_anemias, alcohol_abuse, drug_abuse, psychoses, depression) ~ 1

model_7 <- poLCA(f, lca_data, nclass = 7, nrep = 10)

model_6 <- poLCA(f, lca_data, nclass = 6, nrep = 10)

posterior_prob <- model_7$posterior

reassigned_classes <- apply(posterior_prob, 1, function(class_prob) {
  original_class <- which.max(class_prob)
  if (original_class == 6) {
    remaining_class <- c(1, 2, 3, 4, 5, 7)
    remaining_probs <-  class_prob[remaining_class]
    reassigned_class <- remaining_class[which.max(remaining_probs)]
  } else {
    reassigned_class <- original_class
  }
  return(reassigned_class)
})

df$reassigned_classes <- reassigned_classes
df$six_classes <- model_6$predclass

write.csv(df, "subgroups.csv")
