import pandas as pd
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
import math
from sklearn.preprocessing import LabelEncoder

# Load data from compiled csv
file_content = pd.read_csv('target/compiled_dataset.csv')

# CONSTANTS
# ROWS = file_content.shape[0]    # 5232
ROWS = 10

# Extract ecg readings as training data
training_data_df = file_content.iloc[:ROWS, 32:10033]   # Extract ekg data

# Convert training data to numpy array
training_data_np = training_data_df.to_numpy()
# print(training_data_np)

# Process training data
def process_data(np_2d_matrix):

    # Build Columns
    avg_r_peak_col = []
    avg_pr_interval_col = []
    # ...

    for i in range(ROWS):

        signals, info = nk.ecg_process(np_2d_matrix[i,:], sampling_rate=1000)

        # Find important characteritics from each row (10 sec reading)
        avg_r_peak_col.append(avg_r_peak_reading(signals, info))
        avg_pr_interval_col.append(avg_pr_interval_reading(signals, info))
        # ...

    # Build dataframe of important columns
    processed_dataframe = pd.DataFrame(
        {
            'AVG_R_PEAK': avg_r_peak_col,
            'AVG_PR_INTERVAL': avg_pr_interval_col,
            # ...
        }
    )

    return processed_dataframe

# Process sample for average r peak
def avg_r_peak_reading(signals, info):

    # Find values of r_peaks indexes
    # print(info['ECG_R_Peaks']) # Give index of r_peaks
    r_peak_values = []
    for r_index in info['ECG_R_Peaks']:
        r_value = signals['ECG_Clean'][r_index]     # Retrieve value of cleaned ecg signal from index
        r_peak_values.append(r_value)
    # print(r_peak_values)

    # Calculate and save average
    total = round(sum(r_peak_values), 6)
    avg_r_peak = round(total/len(r_peak_values), 6)

    return avg_r_peak

# Process sample for average pr interval
def avg_pr_interval_reading(signals, info):

    # Find values of all pr_intervals in reading
    pr_interval_values = []
    for beat in range(len(info['ECG_P_Onsets'])):
        p_onset = info['ECG_P_Onsets'][beat]
        r_onset = info['ECG_R_Onsets'][beat]
        if not math.isnan(p_onset) and not math.isnan(r_onset):
            pr_interval_values.append(r_onset - p_onset)
    # print(pr_interval_values)
        
    # Calculate and save average
    total = sum(pr_interval_values)
    avg_pr_interval = round(total/len(pr_interval_values))       

    return avg_pr_interval

# Create the columns or characteristics you want to track
condition_col = file_content['EXTRT'][:ROWS]
sex_col = file_content['SEX'][:ROWS]
age_col = file_content['AGE'][:ROWS]
height_col = file_content['HGHT'][:ROWS]
width_col = file_content['WGHT'][:ROWS]
ethnicity_col = file_content['RACE'][:ROWS]

# Encode any columns that are not numeric
# condition_col = LabelEncoder().fit_transform(condition_col)
# sex_col = LabelEncoder().fit_transform(sex_col)
# ethnicity_col = LabelEncoder().fit_transform(ethnicity_col)

# Save encoders
# ... 

# Get important features from ecg signals
processed_dataset_ecg = process_data(training_data_np)

# Build dataframe to hold and organize entire training data
processed_dataset = pd.DataFrame(
    {
        'CONDITION': condition_col,
        'SEX': sex_col,
        'AGE': age_col,
        'HEIGHT': height_col,
        'WEIGHT': width_col,
        'ETHNICITY': ethnicity_col,
        'AVG_R_PEAK': processed_dataset_ecg['AVG_R_PEAK'],
        'AVG_PR_INTERVAL': processed_dataset_ecg['AVG_PR_INTERVAL'],
    }
)

print(processed_dataset)
# processed_dataset.to_csv('target/processed_dataset.csv')




