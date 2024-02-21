import wfdb
import numpy as np
import pandas as pd
import os

subject = "1001"
files = os.listdir("ecg_data/raw/" + subject)

# Matrix for one subject
sub_matrix = np.zeros(10000) # Initialize top zero row

# List of filenames in one subject
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
print(sub_matrix) # Each row represents a 10 second reading from the subject

sub_pd = pd.DataFrame(data=sub_matrix, index=filelist)
print(sub_pd)