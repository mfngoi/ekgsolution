import flask
import pickle
import json
import base64
import bitarray
import requests
import numpy as np
from flask import request
from news_data import news_data
from ecgclassifier import ecgClassify

app = flask.Flask(__name__) # Create a flask app (our server)

# Load model
with open('target/ecgClassifier.pkl', 'rb') as f:
    ecgClassifier = pickle.load(f)

# Load other models
with open('models/white_male_classifer.pkl', 'rb') as f:
    w_m_classifier = pickle.load(f)

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

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/myhomepage')
def homepage():
    return "This is the homepage"

@app.route('/example/<myvar>')
def example(myvar):
    return "You entered in " + str(myvar)

@app.route('/newsinfo')
def newsInfo():
    return flask.jsonify(news_data)

# @app.route('/diagnose', methods=['GET', 'POST'])
# def diagnose():

#     try:

#         user_uid = request.json['args']
#         date = request.json['created_on']
#         print(f"{user_uid=}")
#         print(f"{date=}")

#         device_url = "https://api.particle.io/v1/devices/e00fce684219e0e249d5bc42/uploadEKGData?access_token=40c9617030f65832904eb99528de3da5e7ebfe66"
        
#         args = user_uid + "," + date
#         print(f"{args=}")
#         data = {"args": args}
#         result = requests.post(url=device_url, data=data)
#         print(result)
#         print(type(result))
#         return "success"
#     except:
#         return "failed"

@app.route("/ekgclassify", methods=['POST'])
def ekgClassify():

    # data = json.loads(request.form)
    # print(request.form)

    # Handling profile
    profile = request.form['profile'] # Extract contents of profile key
    profile = json.loads(profile)   # Convert string to python dictionary

    # Handling signals
    signals = request.form['signals']
    signals = signals.strip()
    # print(f"{signals=}")

    # Decode signals base64 into "signals"
    decoded_bytes = base64.b64decode(signals)   # bytes
    b_array = bitarray.bitarray()
    b_array.frombytes(decoded_bytes) # bit array

    # Turn each 12 bit into a decimal number
    ecg_signals = []
    for i in range(len(b_array)//12):
        start_idx = i * 12
        end_idx = (i+1) * 12
        num = int(b_array[start_idx : end_idx].to01(), 2)
        ecg_signals.append(num)
    # print(f"{ecg_signals=}")

    # Format signal into numpy array    
    input_data_np = np.asarray(ecg_signals, dtype=np.float64)       # convert to type float64
    # print(f"{input_data_np=}")

    # input_data_np = input_data_np / 4095        # normalize unit

    # Get condition in result
    results = ecgClassify(profile, input_data_np, ecgClassifier, encoders)
    results = json.dumps(results)
    
    return results

@app.route("/white_m_classify", methods=['POST'])
def white_male_classify():


    w_m_classifier


if __name__ == '__main__': # Runs app when the program is started
    app.run(host='0.0.0.0', debug=True, port=5000)
