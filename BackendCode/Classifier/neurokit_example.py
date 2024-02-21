import matplotlib.pyplot as plt
import neurokit2 as nk
import pandas as pd
import numpy as np

# Get 10,000 reading sample from file
input_data = []
with open("heart_samples/heartsample_5v_01.log", 'r') as file:
    while len(input_data) < 10000:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break
print(input_data)
print(len(input_data))


# Get data
data = nk.data("bio_resting_5min_100hz")

# Normalize
input_data_np = np.asarray(input_data)
# input_data_np = input_data_np / 4095      # Convert voltages to 0-1 units
print(input_data_np)

input_data_pd = pd.Series(input_data_np, index=range(10000))

print(data["ECG"])
print(input_data_pd)

# Process ecg
ecg_signals, info = nk.ecg_process(input_data_pd, sampling_rate=1000)
print("ecg signals accepted... ")

print(ecg_signals)
print()
print("=================================")
print()
print(info)

nk.ecg_plot(ecg_signals, info)
plt.show()