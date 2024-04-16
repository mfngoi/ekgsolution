import matplotlib.pyplot as plt
import neurokit2 as nk
from neurokit2.epochs import epochs_to_df
import pandas as pd
import numpy as np
import math

# Process sample for average pr interval
def avg_pr_interval_reading(signals, info):

    # Find values of all pr_intervals in reading
    pr_interval_values = []
    print(f"{info['ECG_P_Onsets']=}")
    print(f"{info['ECG_R_Onsets']=}")
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


# Get 10,000 reading sample from file
input_data = []
with open("target/heartsample_5v_01.log", 'r') as file:
    while len(input_data) < 10000:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break

# Standardize data
print(f"{input_data=}")
input_data_np = np.asarray(input_data, dtype=np.float64)       # convert to type float64
# input_data_np = input_data_np / 4095      # Convert voltages to 0-1 units
# print(input_data_np)

# Process ecg
ecg_signals, info = nk.ecg_process(input_data_np, sampling_rate=1000)
print(f"{ecg_signals=}")
# print(ecg_signals.columns)
# ecg_signals['ECG_P_Offsets'].to_csv('hello.csv')
# print(ecg_signals['ECG_P_Offsets'])
print(f"{info=}")
print(f"{info['ECG_P_Onsets']=}")
print(f"{len(info['ECG_P_Onsets'])=}")
print(f"{info['ECG_R_Peaks']=}")
print(f"{len(info['ECG_R_Peaks'])=}")

rr_list = []
for i in range(len(info['ECG_R_Peaks'])-1):
    curr_rr = info['ECG_R_Peaks'][i+1] - info['ECG_R_Peaks'][i]
    rr_list.append(curr_rr)

print(f"{rr_list=}")
print(f"{len(rr_list)=}")
avg_rr = sum(rr_list) / len(rr_list)
print(f"{avg_rr=}")


# avg_pr = avg_pr_interval_reading(ecg_signals, info)
avg_qt = avg_qt_interval_reading(ecg_signals, info)
# print(f"{avg_pr=}")
print(f"{avg_qt=}")

avg_qtc = avg_qt / avg_rr
print(f"{avg_qtc=}")

# # Examine plot (Displays ecg analysis overview)s
# nk.ecg_plot(ecg_signals, info)
# plt.show()

# # Segments each heart beat from our ecg_signals
# # 1 heartbeat segment per R-Peaks
# heartbeats = nk.ecg_segment(ecg_signals, rpeaks=info["ECG_R_Peaks"], sampling_rate=info["sampling_rate"], show=True)
# # print(heartbeats)


# # Convert each segment to its own data frame
# df = epochs_to_df(heartbeats)

# # Get main signal column name
# # Selects either "Signal", "ECG_Raw", or "ECG_Clean" column to average
# # col = [c for c in ["Signal", "ECG_Raw", "ECG_Clean"] if c in df.columns][-1]
# col = "ECG_Clean"
# print(col)

# # Calculate average heartbeat
# mean_heartbeat = df.groupby("Time")[[col]].mean()
# # print(f"{mean_heartbeat=}")
# mean_hb = mean_heartbeat["ECG_Clean"].tolist()
# print(f"{mean_hb=}")
# # mean_heartbeat.to_csv("target/mean_heartbeat.csv", columns=["ECG_Clean"], index=False)
# mean_heartbeat.plot()

# np_mean_heartbeat = mean_heartbeat["ECG_Clean"].to_numpy()
# np_mean_heartbeat = np.hstack((np_mean_heartbeat, np.zeros(1000)))
# waves, signals = nk.ecg_delineate(np_mean_heartbeat)
# print(waves)
# print(signals)


# print(np_mean_heartbeat.shape)
# instant_peaks, info = nk.ecg_peaks(ecg_cleaned=np_mean_heartbeat, sampling_rate=1000)
# print(instant_peaks)
# print(info)
# instant_peaks.to_csv('target/instant_peaks.csv')

plt.show()