import flask
import time

app = flask.Flask(__name__) # Create a flask app (our server)

@app.route('/')
def root():
    print("root triggered... ")
    return "root"

@app.route('/service')
def service():
    time.sleep(10)
    print("service triggered... ")
    return "service"

if __name__ == '__main__': # Runs app when the program is started
    app.run(host='0.0.0.0', debug=True)

