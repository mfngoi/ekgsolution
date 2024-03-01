import flask
import pickle
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
    value = request.body
    print(f"{value}")

    profile = request.body['profile']
    ecg_signals = request.body['signals']

    # Get condition in result
    result = ecgClassify(profile, ecg_signals, ecgClassifier, encoders)
    print(f"{result}")
    
    return "success"

if __name__ == '__main__': # Runs app when the program is started
    app.run(debug=True)