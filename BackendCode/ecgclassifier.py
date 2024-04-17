import math
import json
import numpy as np
import neurokit2 as nk

# Process sample for average pr interval
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

# Main function used to classify ecg signals
# will return a type of condition or a normal condition
def ecgClassify(profile, ecg_signals, model, encoders):

    # Process signal / input_data using neurokit2
    signals, info = nk.ecg_process(ecg_signals, sampling_rate=40) # Change sampling rate (min: 500 readings / 10 sec or 100 readings / 5 secs

    # ECG Characteristics
    avg_p_wave = avg_p_wave_reading(signals, info)
    avg_qt_interval = avg_qt_interval_reading(signals, info)
    avg_rr = avg_rr_reading(signals, info)

    avg_qtc_interval = avg_qt_interval / math.sqrt(avg_rr/1000)
    print(f"{avg_qtc_interval=}")

    # Human Characteristics
    # condition = ['Placebo']
    sex = profile['sex']
    age = float(profile['age'])
    height = float(profile['height'])
    weight = float(profile['weight'])
    ethnicity = profile['race']

    # Encode or numerize columns
    # condition = condition_encoder.transform(condition)
    sex = encoders['sex'].transform([sex])[0]
    ethnicity = encoders['ethnicity'].transform([ethnicity])[0]

    # Create numpy array for input
    # my_data = np.asarray([sex, age, height, weight, ethnicity, avg_r_peak, avg_pr_interval, avg_qt_interval])
    my_data = np.asarray([sex, age, height, weight, ethnicity, avg_p_wave, avg_qtc_interval])
    # print(f"{my_data}")
            
    # Get prediction
    condition_encoded = model.predict([my_data])
    condition = encoders['condition'].inverse_transform(condition_encoded)[0]    # Decode and extract from array
    print(f"{condition=}")

    # Get Average Heartbeats
    heartbeats = nk.ecg_segment(signals, rpeaks=info["ECG_R_Peaks"], sampling_rate=info["sampling_rate"], show=False)
    epochs_heartbeats = nk.epochs.epochs_to_df(heartbeats)

    # Calculate average ecg values by time 
    heartbeats = epochs_heartbeats.groupby("Time")[["ECG_Clean"]].mean()
    # print(f"{mean_heartbeat=}")
    avg_heartbeat = heartbeats["ECG_Clean"].tolist()
    # print(f"{avg_heartbeat=}")


    results = {
        "condition": condition,
        "ecg_signals": ecg_signals.tolist(),
        "avg_heartbeat": avg_heartbeat,
        "pr_interval": avg_p_wave,
        "qt_interval": avg_qt_interval,
    }

    return results
