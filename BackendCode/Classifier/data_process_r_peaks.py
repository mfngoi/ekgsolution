import pandas as pd
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Load data from compiled csv
file_content = pd.read_csv('target/compiled_dataset.csv')
print(file_content)

# CONSTANTS
# ROWS = file_content.shape[0]    # 5232
ROWS = 10

# Extract ecg readings as training data
training_data_df = file_content.iloc[:ROWS, 32:10033]   # Extract ekg data
print(training_data_df)

# Convert training data to numpy array
training_data_np = training_data_df.to_numpy()
print(training_data_np)

# Process training data for r peaks specifically
def avg_all_r_peaks(np_2d_matrix):
    
    r_peak_col = []

    for i in range(ROWS):

        # print(np_2d_matrix[i,:].shape)
        signals, info = nk.ecg_process(np_2d_matrix[i,:], sampling_rate=1000)
        # print(signals)    # Raw and cleaned readings
        # print(info)       # Give indexes of peaks, onsets, and offsets of PQRST waves

        # Find values of r_peaks indexes
        # print(info['ECG_R_Peaks']) # Give index of r_peaks
        r_peak_values = []
        for r_index in info['ECG_R_Peaks']:
            r_value = signals['ECG_Clean'][r_index]     # Retrieve value of cleaned ecg signal from index
            r_peak_values.append(r_value)
        # print(r_peak_values)

        # Calculate and save average
        total = round(sum(r_peak_values), 6)
        average = round(total/len(r_peak_values), 6)
        r_peak_col.append(average)

    return r_peak_col

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


def r_peak_avg_hb(np_2d_matrix):

    r_peak_col = []

    for i in range(ROWS):

        avg_heartbeat = average_heartbeat(np_2d_matrix[i,:])
        # print(avg_heartbeat)
        # pd.Series(avg_heartbeat).plot()
        # plt.show()

        r_peak_col.append(max(avg_heartbeat))

    return r_peak_col



# Create the columns or characteristics you want to track
condition_col = file_content['EXTRT'][:ROWS]
sex_col = file_content['SEX'][:ROWS]
age_col = file_content['AGE'][:ROWS]
height_col = file_content['HGHT'][:ROWS]
width_col = file_content['WGHT'][:ROWS]
ethnicity_col = file_content['RACE'][:ROWS]
avg_all_r_peaks_col = avg_all_r_peaks(training_data_np)
r_peak_avg_hb_col = r_peak_avg_hb(training_data_np)
pr_int_col = np.zeros(ROWS)
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
        'WEIGHT': width_col,
        'ETHNICITY': ethnicity_col,
        'AVG_ALL_R_PEAK': avg_all_r_peaks_col,               # Should contain the average rpeak of a 10 sec period
        'R_PEAK_OF_AVG_HEART': r_peak_avg_hb_col,
        'PR_INT': pr_int_col,
        'PR_SEGMENT': pr_seg_col,
    }
)

print(processed_dataset)
