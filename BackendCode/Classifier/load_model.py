from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle

# Load model
with open('target/ekgClassifier.pkl', 'rb') as f:
    ekgClassifier = pickle.load(f)

# Load label encoder
with open('target/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Gather input data
# Get 10,000 reading sample from file
input_data = []
with open("target/heartsample_5v_01.log", 'r') as file:
    while len(input_data) < 10000:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break
# print(input_data)
# print(len(input_data))
        
answer = ekgClassifier.predict([input_data])

print(answer)
answer_decoded = encoder.inverse_transform(answer)
print(answer_decoded)