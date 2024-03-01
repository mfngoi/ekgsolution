import numpy as np
import pandas as pd
import neurokit2 as nk
import pickle
from csv_process import avg_r_peak_reading, avg_pr_interval_reading, avg_qt_interval_reading

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

# Gather input data
# Get 10,000 reading sample from file
input_data = []
with open("target/heartsample_5v_01.log", 'r') as file:
    while len(input_data) < 10000:
        line = file.readline().strip()
        if line.isdigit():
            reading = int(line)
            # reading = int(line) / 4095          # normalize unit
            input_data.append(reading) 
        if line == "":
            break
print(f"Maximum: {max(input_data)}")
print(f"Minimum: {min(input_data)}")
print(f"Average: {sum(input_data)/len(input_data)}")


# Process input data     
input_data_np = np.asarray(input_data)
signals, info = nk.ecg_process(input_data_np, sampling_rate=1000)

# ECG Characteristics
# avg_r_peak = avg_r_peak_reading(signals, info)
avg_pr_interval = avg_pr_interval_reading(signals, info)
avg_qt_interval = avg_qt_interval_reading(signals, info)

# Human Characteristics
# condition = ['Placebo']
sex = ['M']
age = [23]
height = [180.5]
weight = [67.8]
ethnicity = ['ASIAN']

# Encode or numerize columns
# condition = condition_encoder.transform(condition)
sex = sex_encoder.transform(sex)
ethnicity = ethnicity_encoder.transform(ethnicity)

# Create dataframe of input test
my_dataframe = pd.DataFrame(
    {
        # 'CONDITION': condition,
        'SEX': sex,
        'AGE': age,
        'HEIGHT': height,
        'WEIGHT': weight,
        'ETHNICITY': ethnicity,
        # 'AVG_R_PEAK': [avg_r_peak],
        'AVG_PR_INTERVAL': [avg_pr_interval],
        'AVG_QT_INTERVAL': [avg_qt_interval],
    }
)
print(my_dataframe)
        
# Ask model to predict our input_data
my_data = my_dataframe.to_numpy()
condition_encoded = ecgClassifier.predict(my_data)
print(f"{condition_encoded}")   # Numerical value

# Decode the prediction
condition = condition_encoder.inverse_transform(condition_encoded)
print(f"{condition}")
