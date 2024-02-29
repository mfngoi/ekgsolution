from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle

# Load data from compiled csv
file_content = pd.read_csv('target/processed_dataset.csv', index_col=0)
file_content = file_content.drop('AVG_R_PEAK', axis='columns')        # Should we consider amplitudes?

# Convert training data to numpy array
training_data = file_content.iloc[:,1:].to_numpy()
print(training_data)

# Extract training label or the conditions of each subject
training_label = file_content.iloc[:,0].to_numpy()
print(training_label)

# Select algorithm and load data for training
ekgClassifier = svm.SVC()
print("Training started... ")
ekgClassifier.fit(training_data, training_label) # Training
print("Training Completed... ")

# Save trained model to disk
with open('target/ekgClassifier.pkl', 'wb') as f:
    pickle.dump(ekgClassifier, f)
print("Saved model to disk... ")