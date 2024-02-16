import wfdb
import numpy as np
import pandas as pd
import os

sig, fields = wfdb.rdsamp('ecg_data/raw/1001/0b61746e-c5f4-4b54-8baa-4404c22e09b5')

print(sig)

# Properties
print(sig.ndim)
print(sig.shape)
print(sig.dtype)

leadII = sig[:,1]
print("Leads II")
print(leadII)
print(leadII.shape)

# How to read csv file
csvFile = pd.read_csv('ecg_data/SCR-002.Clinical.Data.csv')
nClinicalData = csvFile.to_numpy() # turn csv file to numpy

print()
# Properties of clinical data
print(nClinicalData)
print(nClinicalData.shape)
print(nClinicalData.dtype)

# print(nClinicalData[5,:])
# Retrieve all test labels from clinical data
results = nClinicalData[:, 12]
print(results)
print(results.shape)

# get folder list
folders = os.listdir("ecg_data/raw")
print(folders)

files = os.listdir("ecg_data/raw/1001")
print(files)

# iterate through all files in a single subject
for i in range(0, len(files), 2):
    # print(files[i])
    print(files[i].split('.')[0])
    filename = files[i].split('.')[0]
    filelocation = "ecg_data/raw/1001/" + filename
    sig, fields = wfdb.rdsamp(filelocation)
    leadII = sig[:,1]
    
    print(leadII)
    print(leadII.ndim)
