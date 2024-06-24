import pickle
import numpy as np


# Load model
with open('target/ecgClassifier.pkl', 'rb') as f:
    ecgClassifier = pickle.load(f)

# Load label encoders
with open('target/condition_encoder.pkl', 'rb') as f:
    condition_encoder = pickle.load(f)
with open('target/sex_encoder.pkl', 'rb') as f:
    sex_encoder = pickle.load(f)
with open('target/ethnicity_encoder.pkl', 'rb') as f:
    ethnicity_encoder = pickle.load(f)

# ,CONDITION,SEX,AGE,HEIGHT,WEIGHT,ETHNICITY,AVG_R_PEAK,AVG_P_WAVE,AVG_QTC_INTERVAL
# ,4,0,30,167.0,71.3,2,0.825794,99.0,386.90865512520645
data = [245,1,0,20,177.0,80.6,2,0.77369,104.333333,411.28243832587697]

# Data
sex = data[2] # 'M' = 1, 'F' = 0
age = data[3]
height = data[4]
weight = data[5]
ethnicity = data[6] # 'ASIAN' = 1,  'AFRICAN AMERICAN' = 0, 'WHITE' = 2
avg_p_wave = data[8]
avg_qtc_interval = data[9]
real_condition = data[1]
real_condition_decoded = condition_encoder.inverse_transform([real_condition])[0]

# Load data
my_data = np.asarray([sex, age, height, weight, ethnicity, avg_p_wave, avg_qtc_interval])

# Get prediction
condition_encoded = ecgClassifier.predict([my_data])
condition = condition_encoder.inverse_transform(condition_encoded)[0]    # Decode and extract from array

# Decode columns
# condition = condition_encoder.transform(condition)
sex = sex_encoder.inverse_transform([sex])[0]
ethnicity = ethnicity_encoder.inverse_transform([ethnicity])[0]

print(f"Sex: {sex}")
print(f"Age: {age}")
print(f"Height: {height}")
print(f"Weight: {weight}")
print(f"Ethnicity: {ethnicity}")
print(f"AVG P WAVE: {avg_p_wave}")
print(f"AVG QT INTERVAL: {avg_qtc_interval}")
print(f"Expected Condition: [{real_condition}] {real_condition_decoded}")
print(f"Given Condition: {condition_encoded} {condition}")


# Experiment can classifier determine overdose


# What consititues as an overdose experimentally?
# P-wave exceeds normal by 18 ms
# Corrected QT interval exceeds by 37 ms


