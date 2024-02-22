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
csvFile = pd.read_csv('ecg_data/SCR-002.Clinical.Data.csv', index_col=[0])
print(csvFile)
nClinicalData = csvFile.to_numpy() # turn csv file to numpy

print()
# Properties of clinical data
# print(nClinicalData)
# print(nClinicalData.shape)
# print(nClinicalData.dtype)

# print(nClinicalData[5,:])
# Retrieve all test labels from clinical data
results = nClinicalData[:, 12]
# print(results)
# print(results.shape)

# get folder list
folders = os.listdir("ecg_data/raw")
# print(folders)

merged_subject_list = []

for subject in folders:
# subject = "1001"

    files = os.listdir("ecg_data/raw/" + subject)
    # print(files)

    # Matrix for one subject
    sub_matrix = np.zeros(10000) # Initialize top zero row
    filelist = []

    # iterate through all files in a single subject
    for i in range(0, len(files), 2):
        # print(files[i])
        # print(files[i].split('.')[0])
        filename = files[i].split('.')[0]
        filelocation = "ecg_data/raw/" + subject + "/" + filename
        sig, fields = wfdb.rdsamp(filelocation) # get reading from sample
        leadII = sig[:,1]   # extract lead II data
        # print(leadII)     # single row of 10,000 readings from LEAD II

        # Accumulate leadII readings into matrix
        sub_matrix = np.vstack((sub_matrix, leadII))
        
        filelist.append(filename)   # Track file names
        
    sub_matrix = sub_matrix[1:,:]   # Remove top zero row
    # print(sub_matrix) # Each row represents a 10 second reading from the subject

    sub_pd = pd.DataFrame(data=sub_matrix, index=filelist)
    # print(sub_pd)

    merged_subject_pd = pd.merge(csvFile, sub_pd, left_index=True, right_index=True)
    # print(merged_subject_pd)
    merged_subject_list.append(merged_subject_pd)

    print(subject + " completed... ")

final_dataset = pd.concat(merged_subject_list)
print(final_dataset)
final_dataset.to_csv("target/compiled_dataset.csv") # Saves the dataframe into a csv file
print("compiled data set completed... ")
