import pandas as pd
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
import math
from sklearn.preprocessing import LabelEncoder

# Load data from compiled csv
file_content = pd.read_csv('target/compiled_dataset.csv')
print(file_content)

# CONSTANTS
# ROWS = file_content.shape[0]    # 5232
ROWS = 5

# Extract ecg readings as training data
training_data_df = file_content.iloc[:ROWS, 32:10033]   # Extract ekg data
print(training_data_df)

# Convert training data to numpy array
training_data_np = training_data_df.to_numpy()
print(training_data_np)

# Process training data for r peaks specifically
def avg_all_pr_interval(np_2d_matrix):
    
    pr_interval_col = []

    for i in range(ROWS):

        # print(np_2d_matrix[i,:].shape)
        signals, info = nk.ecg_process(np_2d_matrix[i,:], sampling_rate=1000)
        # print(signals)    # Raw and cleaned readings
        # print(info)       # Give indexes of peaks, onsets, and offsets of PQRST waves
        # print(info.keys())

        print()
        print('P_Onsets', info['ECG_P_Onsets'])
        print('R_Onsets', info['ECG_R_Onsets'])

        # Find values of all pr_intervals in reading
        pr_interval_values = []
        for beat in range(len(info['ECG_P_Onsets'])):
            p_onset = info['ECG_P_Onsets'][beat]
            r_onset = info['ECG_R_Onsets'][beat]
            if not math.isnan(p_onset) and not math.isnan(r_onset):
                pr_interval_values.append(r_onset - p_onset)
        print(pr_interval_values)
            
        # Calculate and save average
        total = sum(pr_interval_values)
        average = round(total/len(pr_interval_values))
        pr_interval_col.append(average)        

    return pr_interval_col

def average_heartbeat(signal_array):

    signals, info = nk.ecg_process(signal_array, sampling_rate=1000)
    # print(signals)    # Raw and cleaned readings
    # print(info)       # Give indexes of peaks, onsets, and offsets of PQRST waves

    # Get each heartbeat as its own segment
    heartbeats = nk.ecg_segment(signals, rpeaks=info['ECG_R_Peaks'], sampling_rate=info['sampling_rate'])
    heartbeats = nk.epochs.epochs_to_df(heartbeats)

    # Average all the heartbeats together
    mean_heartbeat = heartbeats.groupby('Time')[['ECG_Clean']].mean()
    mean_heartbeat = mean_heartbeat["ECG_Clean"].to_numpy()     # Return as numpy array

    return mean_heartbeat

def pr_interval_avg_hb(np_2d_matrix):

    pr_interval_col = []

    for i in range(ROWS):

        avg_heartbeat = average_heartbeat(np_2d_matrix[i,:])
        # print(avg_heartbeat)
        # pd.Series(avg_heartbeat).plot()
        # plt.show()

        # Tried to use ecg_delineate() but unable to function properly
        pr_interval_col.append(0)

    return pr_interval_col

# Create the columns or characteristics you want to track
condition_col = file_content['EXTRT'][:ROWS]
sex_col = file_content['SEX'][:ROWS]
age_col = file_content['AGE'][:ROWS]
height_col = file_content['HGHT'][:ROWS]
width_col = file_content['WGHT'][:ROWS]
ethnicity_col = file_content['RACE'][:ROWS]
avg_all_r_peaks_col = np.zeros(ROWS)
r_peak_avg_hb_col = np.zeros(ROWS)
avg_all_pr_int_col = avg_all_pr_interval(training_data_np)
pr_int_avg_hb_col = pr_interval_avg_hb(training_data_np)
pr_seg_col = np.zeros(ROWS)


# Encode any columns that are not numeric
condition_col = LabelEncoder().fit_transform(condition_col)
sex_col = LabelEncoder().fit_transform(sex_col)

processed_dataset = pd.DataFrame(
    {
        'CONDITION': condition_col,
        'SEX': sex_col,
        'AGE': age_col,
        'HEIGHT': height_col,
        'WIDTH': width_col,
        'ETHNICITY': ethnicity_col,
        'AVG_ALL_R_PEAK': avg_all_r_peaks_col,               # Should contain the average rpeak of a 10 sec period
        'R_PEAK_OF_AVG_HEART': r_peak_avg_hb_col,
        'AVG_ALL_PR_INTERVAL': avg_all_pr_int_col,
        'PR_INTERVAL_AVG_HEART': pr_int_avg_hb_col,
    }
)

print(processed_dataset)
