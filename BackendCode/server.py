import flask
import pickle
import json
import numpy as np
from flask import request
from news_data import news_data
from ecgclassifier import ecgClassify

app = flask.Flask(__name__) # Create a flask app (our server)

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

@app.route("/ekgclassify", methods=['POST'])
def ekgClassify():

    # data = json.loads(request.form)
    # print(request.form)

    # Handling profile
    profile = request.form['profile'] # Extract contents of profile key
    profile = json.loads(profile)   # Convert string to python dictionary

    # Handling signals
    ecg_signals = request.form['signals']
    ecg_signals = ecg_signals.split(',')
    ecg_signals.pop() # Clean end of signal (loose string)

    print(f"{ecg_signals=}")

    # Format signal into numpy array    
    input_data_np = np.asarray(ecg_signals, dtype=np.float64)       # convert to type float64
    print(f"{input_data_np=}")

    input_data_np = input_data_np / 4095        # normalize unit

    # Get condition in result
    results = ecgClassify(profile, input_data_np, ecgClassifier, encoders)
    results = json.dumps(results)
    
    return results

if __name__ == '__main__': # Runs app when the program is started
    app.run(host='0.0.0.0', debug=True, port=5000)
