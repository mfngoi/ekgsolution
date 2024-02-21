import pandas as pd # used to read a csv file
import numpy as np
import wfdb
import os

# Reading a csv file
csv_file = pd.read_csv("ecg_data/SCR-002.Clinical.Data.csv")
print(csv_file)
clinical_data = csv_file.to_numpy() # convert dataframe from panda to numpy array from numpy

print()
print(clinical_data)

label = clinical_data[:,12]  # Training Label
print(label)
print(label.shape)

# How to get a list of folders and files in a specific directory
dir = os.listdir("ecg_data/raw/1001")
print(dir)

# Get the dataset for one test subject
filename = dir[0].split('.')[0]
sig, fields = wfdb.rdsamp('ecg_data/raw/1001/' + filename)
data_1 = sig[:,1]

for i in range(2,len(dir),2):
    filename = dir[i].split('.')[0]
    sig, fields = wfdb.rdsamp('ecg_data/raw/1001/' + filename)
    leadII = sig[:,1]
    data_1 = np.vstack((data_1, leadII))

print(data_1)
print(data_1.ndim)
print(data_1.shape)




