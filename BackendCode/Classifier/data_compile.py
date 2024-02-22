import wfdb
import numpy as np
import pandas as pd
import os

# Read CSV file for subject information (meta data)
csv_file = pd.read_csv('ecg_data/SCR-002.Clinical.Data.csv', index_col=[0])

# Get folders in raw (list of subjects)
folders = os.listdir("ecg_data/raw")

# Store dataframes of each compiled subject
merged_subject_list = []

# Iterate through subjects
for subject in folders:
# subject = "1001"

    files = os.listdir("ecg_data/raw/" + subject)

    # Matrix for one subject
    sub_matrix = np.zeros(10000) # Initialize top zero row
    filelist = []

    # Iterate through all files in a single subject
    for i in range(len(files)):
        if files[i].split('.')[1] == "dat":
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

    merged_subject_pd = pd.merge(csv_file, sub_pd, left_index=True, right_index=True)
    merged_subject_list.append(merged_subject_pd)
    print(subject + " completed... ")

# Combine all subject dataframes into one
final_dataset = pd.concat(merged_subject_list)
final_dataset.to_csv("target/compiled_dataset.csv") # Saves the dataframe into a csv file
print("compiled data set completed... ")
