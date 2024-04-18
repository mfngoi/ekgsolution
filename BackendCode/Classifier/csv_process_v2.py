import math
import pandas as pd
import numpy as np
import neurokit2 as nk

# Process sample for average pr interval
def avg_p_wave(signals, info):
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

# Process sample for average Q-Peak to T-Offset interval
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
RANDID = 1001
# ROWS = 500

# Extract ecg readings as training data
training_data_df = csv.iloc[:ROWS, 32:10033]   # Extract ekg data

# Convert training data to numpy array
training_data_np = training_data_df.to_numpy()
# print(training_data_np)

subjects = range(1001, 1023)

for subject in subjects:

    # Create the columns or characteristics you want to track from csv
    randid_col = []
    condition_col = []
    sex_col = []
    age_col = []
    height_col = []
    width_col = []
    ethnicity_col = []

    # Build Columns for ecg signals
    # avg_r_peak_col = []
    avg_p_wave_col = []
    avg_qtc_interval_col = []
    # ...

    for i in range(ROWS):

        if csv['RANDID'][i] == subject:

            print('=' * 30)
            print(f"filename: {csv['EGREFID'][i]}  randid: {csv['RANDID'][i]}")
            signals, info = nk.ecg_process(training_data_np[i,:], sampling_rate=1000)

            # Build processed row from each file
            try:
                # Find important characteritics from each row (10 sec reading)
                # avg_r_peak = avg_r_peak_reading(signals, info)
                avg_p_wave_reading = avg_p_wave(signals, info)
                avg_qt_interval = avg_qt_interval_reading(signals, info)
                avg_rr = avg_rr_reading(signals, info)
                avg_qtc_interval = avg_qt_interval / math.sqrt(avg_rr/1000)
                # ...
                
                # Collect found values
                # avg_r_peak_col.append(avg_r_peak)
                avg_p_wave_col.append(avg_p_wave_reading)
                avg_qtc_interval_col.append(avg_qtc_interval)
                # ...

                # Append characteristics of person
                randid_col.append(csv['RANDID'][i])
                condition_col.append(csv['EXTRT'][i])
                sex_col.append(csv['SEX'][i])
                age_col.append(csv['AGE'][i])
                height_col.append(csv['HGHT'][i])
                width_col.append(csv['WGHT'][i])
                ethnicity_col.append(csv['RACE'][i])

            except Exception as e:
                print(f"Exception Occured: [{e.__class__.__name__}]")
                print(f"[{i} of {ROWS}] skipped... ")

    # Build dataframe out of all the compiled columns
    processed_dataframe = pd.DataFrame(
        {
            'CONDITION': condition_col,
            'SEX': sex_col,
            'AGE': age_col,
            'HEIGHT': height_col,
            'WEIGHT': width_col,
            'ETHNICITY': ethnicity_col,
            # 'AVG_R_PEAK': avg_r_peak_col,
            'AVG_P_WAVE': avg_p_wave_col,
            'AVG_QTC_INTERVAL': avg_qtc_interval_col,
            # ...
        }
    )

    # print(processed_dataframe)
    processed_dataframe.to_csv(f"subjects/processed_dataset_{subject}.csv")
