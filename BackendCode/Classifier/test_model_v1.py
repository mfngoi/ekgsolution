from sklearn import svm
import pickle

# Load model
with open('target/ecgClassifier.pkl', 'rb') as f:
    ecgClassifier = pickle.load(f)

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
        
# Ask model to predict our input_data
prediction = ecgClassifier.predict([input_data])
print(prediction)   # Numerical value

# Decode the prediction
decoded_prediction = encoder.inverse_transform(prediction)
print(decoded_prediction)