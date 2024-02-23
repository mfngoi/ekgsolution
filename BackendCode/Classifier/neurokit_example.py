import matplotlib.pyplot as plt
import neurokit2 as nk

# Generate 15 seconds of ECG signal (recorded at 250 samples/second)
ecg = nk.ecg_simulate(duration=15, sampling_rate=250, heart_rate=70)

# Process it
signals, info = nk.ecg_process(ecg, sampling_rate=250)

# Display signals and info
print(signals)
print(signals.columns)
# signals['ECG_P_Offsets'].to_csv('hello.csv')  # view in csv format
print(signals['ECG_P_Offsets'])
print(info)

# Visualise the processing
nk.ecg_plot(signals, info)

plt.show()