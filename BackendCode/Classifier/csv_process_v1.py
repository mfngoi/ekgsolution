import pandas as pd
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
import pickle
import math
from sklearn.preprocessing import LabelEncoder


# Load data from compiled csv
csv = pd.read_csv('target/compiled_dataset.csv')

# CONSTANTS
ROWS = csv.shape[0]    # 5232
# ROWS = 500

# Process training data
def process_csv(csv, encode=True):

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
    avg_pr_interval_col = []
    avg_qt_interval_col = []
    # ...

    for i in range(ROWS):

        print('=' * 30)
        print(f"filename: {csv['EGREFID'][i]}")
        signals, info = nk.ecg_process(training_data_np[i,:], sampling_rate=1000)

        # Build processed row from each file
        try:
            # Find important characteritics from each row (10 sec reading)
            avg_r_peak = avg_r_peak_reading(signals, info)
            avg_pr_interval = avg_pr_interval_reading(signals, info)
            avg_qt_interval = avg_qt_interval_reading(signals, info)
            # ...
            
            # Collect found values
            avg_r_peak_col.append(avg_r_peak)
            avg_pr_interval_col.append(avg_pr_interval)
            avg_qt_interval_col.append(avg_qt_interval)
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
            'AVG_PR_INTERVAL': avg_pr_interval_col,
            'AVG_QT_INTERVAL': avg_qt_interval_col,
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
    # print(f"{pr_interval_values=}")
        
    # Calculate and save average
    total = sum(pr_interval_values)
    avg_pr_interval = round(total/len(pr_interval_values))    

    return avg_pr_interval

# Process sample for average Q-Peak to T-Offset interval
def avg_qt_interval_reading(signals, info):

    # Find values of all qt_intervals in reading
    qt_interval_values = []
    for beat in range(len(info['ECG_Q_Peaks'])):
        q_peak = info['ECG_Q_Peaks'][beat]
        t_offset = info['ECG_T_Offsets'][beat]
        if not math.isnan(q_peak) and not math.isnan(t_offset):
            qt_interval_values.append(t_offset - q_peak)
    # print(qt_interval_values)
        
    # Calculate and save average
    total = sum(qt_interval_values)
    avg_qt_interval = round(total/len(qt_interval_values))       

    return avg_qt_interval


if __name__ == "___main___":



    # Get important features from ecg signals
    processed_dataset = process_csv(csv)

    print(processed_dataset)
    processed_dataset.to_csv('target/processed_dataset.csv')




