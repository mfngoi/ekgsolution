# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn, db_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore, db
import google.cloud.firestore
import requests
import json

# Other modules
from datetime import datetime

app = initialize_app()

@https_fn.on_request()
def addmessage(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    original = req.args.get("text")
    if original is None:
        return https_fn.Response("No text parameter provided", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Push the new message into Cloud Firestore using the Firebase Admin SDK.
    _, doc_ref = firestore_client.collection("messages").add({"original": original})

    # Send back a message that we've successfully written the message
    return https_fn.Response(f"Message with ID {doc_ref.id} added.")


@firestore_fn.on_document_created(document="messages/{pushId}")
def makeuppercase(event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
    """Listens for new documents to be added to /messages. If the document has
    an "original" field, creates an "uppercase" field containg the contents of
    "original" in upper case."""

    # Get the value of "original" if it exists.
    if event.data is None:
        return
    try:
        original = event.data.get("original")
    except KeyError:
        # No "original" field, so do nothing.
        return

    # Set the "uppercase" field.
    print(f"Uppercasing {event.params['pushId']}: {original}")
    upper = original.upper()
    event.data.reference.update({"uppercase": upper})

def demoGroupClassify(route, profile, results, firestore_client, userID, weekID, warnings):
    # url =  AWS SERVER + Route (ie. /white_m_classify)
    server_url = "http://18.223.255.251:5000"
    url = f"{server_url}{route}"
    data = {"age": int(profile["age"]), "bmi": float(profile["weight"])/float(profile["height"])**2}
    subject_p_wave_standard, subject_qtc_wave_standard = requests.post(url=url, data=data)
    def check_p_wave():
        return (float(results["avg_p_wave"]) > subject_p_wave_standard + 18)
    def check_qtc_interval():
        return (float(results["avg_qtc_interval"]) > subject_qtc_wave_standard + 37)
    if check_p_wave() or check_qtc_interval():
        firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).set({"warnings": warnings + 1})

@db_fn.on_value_created(reference="/particle/{pushId}") # Change to database
def addsignals(event: db_fn.Event[db_fn.Change]) -> None:

    # Access data
    data = event.data

    # Get correct week number
    date = datetime.now()

    weekNum = 0
    startDay = datetime(date.year, 1, 1)
    daysDiff = (date - startDay).days
    if date.weekday == 6:  # Check if it is a sunday
        weekNum = daysDiff // 7 + 1
    else: 
        weekNum = daysDiff // 7

    # Create new document
    userID = data["json"]["user"]
    weekID = "week" + str(weekNum)
    reportID = data["json"]["report_id"]

    # Connect to database
    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Submit signals and user info to ecg server (classifier)
    url_post = "http://18.223.255.251:5000/classifier"

    head = {"Content-Type": "application/x-www-form-urlencoded"}

    # Gather user info (userID)
    doc = firestore_client.collection("Users").document(userID).get()
    profile = doc.to_dict()
    profile = json.dumps(profile)

    new_data = {
        "profile": profile,
        "signals": data["json"]["signals"],
    }

    # Send data to amazon server
    response = requests.post(url_post, headers=head, data=new_data)
    results = json.loads(response.text)

    # Push document to database
    entry = {
        "signals": results["decoded_signals"],
        "prediction": results["prediction"],
        "avg_heartbeat": results["avg_heartbeat"],
        "heart_rate": results["heart_rate"],
        "avg_p_wave": results["avg_p_wave"],
        "avg_qtc_interval": results["avg_qtc_interval"],
    }
    print(f"Added report: {reportID} to user db... ")

    # Check if weekly_reports document exists
    doc = firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).get()
    warnings = 0
    # Add week if it does not exists
    if not doc.exists:
        print(f"{weekID} did not exist, creating document... ")
        firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).set({"warnings": warnings})
    else: 
        warnings = int(doc.to_dict()["warnings"]) # Get current value of warnings in doc if exists

    # Check if warnings needs to be updated
    if results["prediction"] != "Placebo":
        # Male
        if profile["sex"] == 'M':

            if profile["race"] == 'ASIAN':
                subject_p_wave_standard, subject_qtc_wave_standard = 106.51,413.56
                def check_p_wave():
                    return (float(results["avg_p_wave"]) > subject_p_wave_standard + 18)
                def check_qtc_interval():
                    return (float(results["avg_qtc_interval"]) > subject_qtc_wave_standard + 37)
                if check_p_wave() or check_qtc_interval():
                    firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).set({"warnings": warnings + 1})
            if profile["race"] == 'AFRICAN AMERICAN':
                # Select a given route in the server to identify closest subject
                route = "/african_american_m_classify"
                demoGroupClassify(route, profile, results, firestore_client, userID, weekID, warnings)

            if profile["race"] == 'WHITE':
                # Select a given route in the server to identify closest subject
                route = "/white_m_classify"
                demoGroupClassify(route, profile, results, firestore_client, userID, weekID, warnings)

        # Female
        if profile["sex"] == 'F':

            if profile["race"] == 'AFRICAN AMERICAN':
                # Select a given route in the server to identify closest subject
                route = "/african_american_f_classify"
                demoGroupClassify(route, profile, results, firestore_client, userID, weekID, warnings)

            if profile["race"] == 'WHITE' or profile["race"] == 'ASIAN': # no existing Asian female subject to compare with
                # Select a given route in the server to identify closest subject
                route = "/white_f_classify"
                demoGroupClassify(route, profile, results, firestore_client, userID, weekID, warnings)
    else:
        print("Prediction is Placebo: No Warnings Issued... ")

    # Add entry to database
    firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).collection("reports").document(reportID).set(entry) 
    
    