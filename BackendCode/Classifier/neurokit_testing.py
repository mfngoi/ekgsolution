import matplotlib.pyplot as plt
import neurokit2 as nk
from neurokit2.epochs import epochs_to_df
from csv_process import avg_pr_interval_reading, avg_qt_interval_reading
import pandas as pd
import numpy as np

# Get 10,000 reading sample from file
input_data = []
with open("target/heartsample_5v_03.log", 'r') as file:
    while len(input_data) < 10000:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break

# Standardize data
print(f"{input_data=}")
input_data_np = np.asarray(input_data)
# input_data_np = input_data_np / 4095      # Convert voltages to 0-1 units
# print(input_data_np)

# Process ecg
ecg_signals, info = nk.ecg_process(input_data_np, sampling_rate=1000)
print(ecg_signals)
# print(ecg_signals.columns)
# ecg_signals['ECG_P_Offsets'].to_csv('hello.csv')
# print(ecg_signals['ECG_P_Offsets'])
print(info)

avg_pr = avg_pr_interval_reading(ecg_signals, info)
avg_qt = avg_qt_interval_reading(ecg_signals, info)
print(f"{avg_pr=}")
print(f"{avg_qt=}")

# Examine plot (Displays ecg analysis overview)s
nk.ecg_plot(ecg_signals, info)

# Segments each heart beat from our ecg_signals
# 1 heartbeat segment per R-Peaks
heartbeats = nk.ecg_segment(ecg_signals, rpeaks=info["ECG_R_Peaks"], sampling_rate=info["sampling_rate"], show=True)
# print(heartbeats)


# Convert each segment to its own data frame
df = epochs_to_df(heartbeats)

# Get main signal column name
# Selects either "Signal", "ECG_Raw", or "ECG_Clean" column to average
# col = [c for c in ["Signal", "ECG_Raw", "ECG_Clean"] if c in df.columns][-1]
col = "ECG_Clean"
print(col)

# Calculate average heartbeat
mean_heartbeat = df.groupby("Time")[[col]].mean()
# print(f"{mean_heartbeat=}")
mean_hb = mean_heartbeat["ECG_Clean"].tolist()
print(f"{mean_hb=}")
# mean_heartbeat.to_csv("target/mean_heartbeat.csv", columns=["ECG_Clean"], index=False)
mean_heartbeat.plot()

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