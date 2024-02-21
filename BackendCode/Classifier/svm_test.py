from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle
import os

model = None

if os.path.exists("model.pkl"):
    print("Found existing model... ")
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
else:
    file_content = pd.read_csv('Classifier/compiled_dataset.csv', index_col=[0])
    print(file_content)

    training_data_df = file_content.iloc[:, 31:10032]   # Extract ekg data
    print(training_data_df)

    training_data = training_data_df.to_numpy()
    print(training_data)

    training_label_df = file_content.iloc[:, 11]
    print(training_label_df)

    encoder = LabelEncoder()
    training_label_encoded = encoder.fit_transform(training_label_df)
    print(training_label_encoded)

    # Save encoder to disk
    with open('encoder.pkl', 'wb') as f:
        pickle.dump(encoder, f)
    print("Saved encoder to disk... ")

    model = svm.SVC()
    model.fit(training_data, training_label_encoded) # Training
    print("Training Completed... ")

    # Save trained model to disk
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Saved model to disk... ")

# Get 10,000 reading sample from file
input_data = []
with open("heart_samples/heartsample_5v_01.log", 'r') as file:
    while len(input_data) < 10000:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break
# print(input_data)
# print(len(input_data))
        
if os.path.exists("encoder.pkl"):
    print("Found existing encoder... ")
    with open('encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
else:
    print("Missing encoder... ")

answer = model.predict([input_data])

print(answer)
answer_decoded = encoder.inverse_transform(answer)
print(answer_decoded)
