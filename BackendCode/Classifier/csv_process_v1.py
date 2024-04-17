import pandas as pd
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
import pickle
import math
from sklearn.preprocessing import LabelEncoder

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

def avg_p_wave_reading(signals, info):
    # P WAVE ALGORITHM
    all_p_waves = []
    for index in range(len(info['ECG_P_Onsets'])):
        p_onset = info['ECG_P_Onsets'][index]
        p_offset = info['ECG_P_Offsets'][index]
        if not math.isnan(p_onset) and not math.isnan(p_offset):
            p_wave = p_offset - p_onset
            all_p_waves.append(p_wave)

    average_p_wave = round(sum(all_p_waves)/len(all_p_waves), 6)
    return average_p_wave

def avg_qt_interval_reading(signals, info):

    all_qt_intervals = []
    for index in range(len(info['ECG_Q_Peaks'])):
        q_peak = info['ECG_Q_Peaks'][index]
        t_offset = info['ECG_T_Offsets'][index]
        if not math.isnan(q_peak) and not math.isnan(t_offset):
            qt_intervals = t_offset - q_peak
            all_qt_intervals.append(qt_intervals)
    
    average_qt_interval = round(sum(all_qt_intervals)/len(all_qt_intervals), 6)

    return average_qt_interval

def avg_rr_reading(signals, info):
    rr_readings = []
    for i in range(len(info['ECG_R_Peaks'])-1):
        curr_rr = info['ECG_R_Peaks'][i+1] - info['ECG_R_Peaks'][i]
        rr_readings.append(curr_rr)

    avg_rr = sum(rr_readings) / len(rr_readings)
    return avg_rr

# Load data from compiled csv
csv = pd.read_csv('target/compiled_dataset.csv')

# CONSTANTS
ROWS = csv.shape[0]    # 5232
# ROWS = 500

# # Process training data
# def process_csv(csv, encode=True):

# Extract ecg readings as training data
training_data_df = csv.iloc[:ROWS, 32:10033]   # Extract ekg data

# Convert training data to numpy array
training_data_np = training_data_df.to_numpy()
# print(training_data_np)

# Create the columns or characteristics you want to track from csv
condition_col = []
sex_col = []
age_col = []
height_col = []
width_col = []
ethnicity_col = []

# Build Columns for ecg signals
avg_r_peak_col = []
avg_p_wave_col = []
avg_qtc_interval_col = []
# ...

for i in range(ROWS):

    print('=' * 30)
    print(f"filename: {csv['EGREFID'][i]}")
    signals, info = nk.ecg_process(training_data_np[i,:], sampling_rate=1000)

    # Build processed row from each file
    try:
        # Find important characteritics from each row (10 sec reading)
        avg_r_peak = avg_r_peak_reading(signals, info)
        avg_p_wave = avg_p_wave_reading(signals, info)
        avg_qt_interval = avg_qt_interval_reading(signals, info)
        avg_rr = avg_rr_reading(signals, info)
        # ...
        
        # Collect found values
        avg_r_peak_col.append(avg_r_peak)
        avg_p_wave_col.append(avg_p_wave)
        avg_qtc_interval_col.append(avg_qt_interval / math.sqrt(avg_rr/1000))
        # ...

        # Append characteristics of person
        condition_col.append(csv['EXTRT'][i])
        sex_col.append(csv['SEX'][i])
        age_col.append(csv['AGE'][i])
        height_col.append(csv['HGHT'][i])
        width_col.append(csv['WGHT'][i])
        ethnicity_col.append(csv['RACE'][i])

    except Exception as e:
        print(f"Exception Occured: [{e.__class__.__name__}]")
        print(f"[{i} of {ROWS}] skipped... ")

    print(f"{int(round(i/ROWS, 2)*100)}% completed [{i} out of {ROWS}]... ")

# Numerize columns and save encoder if true
encode = True
if encode:
    # Encode any columns that are not numeric
    condition_encoder = LabelEncoder()
    condition_col = condition_encoder.fit_transform(np.array(condition_col))
    sex_encoder = LabelEncoder()
    sex_col = sex_encoder.fit_transform(sex_col)
    ethnicity_encoder = LabelEncoder()
    ethnicity_col = ethnicity_encoder.fit_transform(ethnicity_col)

    # Save encoders
    with open('target/condition_encoder.pkl', 'wb') as f:
        pickle.dump(condition_encoder, f)
    with open('target/sex_encoder.pkl', 'wb') as f:
        pickle.dump(sex_encoder, f)
    with open('target/ethnicity_encoder.pkl', 'wb') as f:
        pickle.dump(ethnicity_encoder, f)

# Build dataframe out of all the compiled columns
processed_dataframe = pd.DataFrame(
    {
        'CONDITION': condition_col,
        'SEX': sex_col,
        'AGE': age_col,
        'HEIGHT': height_col,
        'WEIGHT': width_col,
        'ETHNICITY': ethnicity_col,
        'AVG_R_PEAK': avg_r_peak_col,
        'AVG_P_WAVE': avg_p_wave_col,
        'AVG_QTC_INTERVAL': avg_qtc_interval_col,
        # ...
    }
)

processed_dataframe.to_csv('target/processed_dataset.csv')

# return processed_dataframe


# if __name__ == "___main___":

#     # Get important features from ecg signals
#     processed_dataset = process_csv(csv)

#     print(processed_dataset)
#     processed_dataset.to_csv('target/processed_dataset.csv')




