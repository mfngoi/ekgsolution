import numpy as np
import pandas as pd
import neurokit2 as nk
import pickle
import math

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
            reading = int(line) / 4095          # normalize unit
            input_data.append(reading) 
        if line == "":
            break
print(f"Maximum: {max(input_data)}")
print(f"Minimum: {min(input_data)}")
print(f"Average: {sum(input_data)/len(input_data)}")



# Process input data     
input_data_np = np.asarray(input_data)
print(f"{input_data_np.shape=}")
print(f"{input_data_np.dtype=}")
signals, info = nk.ecg_process(input_data_np, sampling_rate=1000)

# ECG Characteristics
# avg_r_peak = avg_r_peak_reading(signals, info)
avg_p_wave = avg_p_wave_reading(signals, info)
avg_qt_interval = avg_qt_interval_reading(signals, info)
avg_rr = avg_rr_reading(signals, info)

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
        'AVG_P_WAVE': [avg_p_wave],
        'AVG_QTC_INTERVAL': [avg_qt_interval / math.sqrt(avg_rr/1000)],
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
