import math
import numpy as np
import neurokit2 as nk

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

# Main function used to classify ecg signals
# will return a type of condition or a normal condition
def ecgClassify(profile, ecg_signals, model, encoders):

    # Format signal into numpy array    
    input_data_np = np.asarray(ecg_signals, dtype=np.float64)       # convert to type float64
    # print(f"{input_data_np=}")

    # input_data_np = input_data_np / 4095        # normalize unit

    # Process signal / input_data using neurokit2
    signals, info = nk.ecg_process(input_data_np, sampling_rate=1000) # Change sampling rate

    # ECG Characteristics
    # avg_r_peak = avg_r_peak_reading(signals, info)
    avg_pr_interval = avg_pr_interval_reading(signals, info)
    avg_qt_interval = avg_qt_interval_reading(signals, info)

    # Human Characteristics
    # condition = ['Placebo']
    sex = profile['sex']
    age = profile['age']
    height = profile['height']
    weight = profile['weight']
    ethnicity = profile['ethnicity']

    # Encode or numerize columns
    # condition = condition_encoder.transform(condition)
    sex = encoders['sex'].transform([sex])[0]
    ethnicity = encoders['ethnicity'].transform([ethnicity])[0]

    # Create numpy array for input
    # my_data = np.asarray([sex, age, height, weight, ethnicity, avg_r_peak, avg_pr_interval, avg_qt_interval])
    my_data = np.asarray([sex, age, height, weight, ethnicity, avg_pr_interval, avg_qt_interval])
    # print(f"{my_data}")
            
    # Get prediction
    condition_encoded = model.predict([my_data])
    condition = encoders['condition'].inverse_transform(condition_encoded)[0]    # Decode and extract from array
    
    return condition
