from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle
import os

# Load data from compiled csv
file_content = pd.read_csv('Classifier/compiled_dataset.csv', index_col=[0])
print(file_content)

# Extract ecg readings as training data
training_data_df = file_content.iloc[:, 31:10032]   # Extract ekg data
print(training_data_df)

# Convert training data to numpy array
training_data = training_data_df.to_numpy()
print(training_data)

# Extract training label or the conditions of each subject
training_label_df = file_content.iloc[:, 11]
print(training_label_df)

# Encode the training label - converts inputs to numerical values
encoder = LabelEncoder()
training_label_encoded = encoder.fit_transform(training_label_df)
print(training_label_encoded)

# Save encoder to disk
with open('encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)
print("Saved encoder to disk... ")

# Select algorithm and load data for training
model = svm.SVC()
model.fit(training_data, training_label_encoded) # Training
print("Training Completed... ")

# Save trained model to disk
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Saved model to disk... ")