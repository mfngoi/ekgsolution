import matplotlib.pyplot as plt
import neurokit2 as nk
from ecgclassifier import ecgClassify
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime



# Load model
with open('target/ecgClassifier.pkl', 'rb') as f:
    ecgClassifier = pickle.load(f)

# Load label encoders
with open('target/condition_encoder.pkl', 'rb') as f:
    condition_encoder = pickle.load(f)
with open('target/sex_encoder.pkl', 'rb') as f:
    sex_encoder = pickle.load(f)
with open('target/ethnicity_encoder.pkl', 'rb') as f:
    ethnicity_encoder = pickle.load(f)

# Store encoders
encoders = {
    'condition': condition_encoder,
    'sex': sex_encoder,
    'ethnicity': ethnicity_encoder,
}





# ====== Route =========

# Generate 15 seconds of ECG signal (recorded at 250 samples/second)
ecg = nk.ecg_simulate(duration=10, sampling_rate=40)

# Format signal into numpy array    
input_data_np = np.asarray(ecg, dtype=np.float64)

# Use a service account.
cred = credentials.Certificate('/Users/matthew/Desktop/projects/ekgsolution/eureka_key.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Eureka ID
userID = "gjpwJHIeXgeExmuQAqfy1c4jjtG2"

# Get profile
doc = db.collection("Users").document(userID).get()
profile = doc.to_dict()
print(profile)


# Test ecgClassify on sample data
results = ecgClassify(profile, input_data_np, ecgClassifier, encoders)

entry = {
    "signals": input_data_np.tolist(),
    "prediction": results["condition"], # prediction
    "avg_heartbeat": results["avg_heartbeat"],
    # "heart_rate": results["heart_rate"],
    "avg_p_wave": results["pr_interval"], # avg_p_wave
    "avg_qtc_interval": results["qt_interval"],  # avg_qtc_interval
}

# Get correct week number
date = datetime.now()

weekNum = 0
startDay = datetime(date.year, 1, 1)
daysDiff = (date - startDay).days
if date.weekday == 6:  # Check if it is a sunday
    weekNum = daysDiff // 7 + 1
else: 
    weekNum = daysDiff // 7

# Create week id and report id
weekID = "week" + str(weekNum)
reportID = f"{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}.{date.microsecond}"

# Check if weekly_reports document exists
doc = db.collection("Users").document(userID).collection("weekly_reports").document(weekID).get()
warnings = 0
# Add week if it does not exists
if not doc.exists:
    print(f"{weekID} did not exist, creating document... ")
    db.collection("Users").document(userID).collection("weekly_reports").document(weekID).set({"warnings": warnings})
else: 
    warnings = int(doc.to_dict()["warnings"]) # Get current value of warnings in doc if exists


db.collection("Users").document(userID).collection("weekly_reports").document(weekID).collection("reports").document(reportID).set(entry) 
print("sucessfully uploaded sample")

# ====== Route Ends ======











# # Process it
# signals, info = nk.ecg_process(ecg, sampling_rate=40)

# # Display signals and info
# print(signals)
# print(signals.columns)
# # signals['ECG_P_Offsets'].to_csv('hello.csv')  # view in csv format
# print(signals['ECG_P_Offsets'])
# print(info)

# # Visualise the processing
# nk.ecg_plot(signals, info)

# plt.show()