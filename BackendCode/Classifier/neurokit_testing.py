import matplotlib.pyplot as plt
import neurokit2 as nk
from neurokit2.epochs import epochs_to_df
import pandas as pd
import numpy as np

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
input_data_np = np.asarray(input_data)
# input_data_np = input_data_np / 4095      # Convert voltages to 0-1 units
print(input_data_np)

# Process ecg
ecg_signals, info = nk.ecg_process(input_data_np, sampling_rate=1000)
print(ecg_signals)
# print(ecg_signals.columns)
# ecg_signals['ECG_P_Offsets'].to_csv('hello.csv')
# print(ecg_signals['ECG_P_Offsets'])
print(info)

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
col = [c for c in ["Signal", "ECG_Raw", "ECG_Clean"] if c in df.columns][-1]
print(col)

# Calculate average heartbeat
mean_heartbeat = df.groupby("Time")[[col]].mean()
print("=================================")
print("mean_heartbeat")
print("=================================")
print(mean_heartbeat)
print()

mean_heartbeat.plot()

plt.show()