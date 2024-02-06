import flask
from news_data import news_data

app = flask.Flask(__name__) # Create a flask app (our server)

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

if __name__ == '__main__': # Runs app when the program is started
    app.run(debug=True)