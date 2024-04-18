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

@db_fn.on_value_created(reference="/particle/{pushId}") # Change to database
def addsignals(event: db_fn.Event[db_fn.Change]) -> None:

    # Access data
    data = event.data
    # print("Access dictionary attempt")
    # print(f"{data=}")

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
    reportID = str(date)

    # Connect to database
    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Submit signals and user info to ecg server (classifier)
    url_post = "http://18.223.255.251:5000/classifier"

    head = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Gather user info (userID)
    doc = firestore_client.collection("Users").document(userID).get()
    profile = doc.to_dict()
    profile = json.dumps(profile)

    new_data = {
        "profile": profile,
        "signals": data["json"]["signals"], #slidjflwijdfliwdjflijw
    }

    # Send data to amazon server
    response = requests.post(url_post, headers=head, data=new_data)
    results = json.loads(response.text)

    # Push document to database
    entry = {
        "signals": results["decoded_signals"],
        "prediction": results["prediction"],
        "avg_heartbeat": results["avg_heartbeat"],
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
        # Check if warnings needs to be increased
        if (results["prediction"] != "Placebo" and float(results["avg_p_wave"]) > 135) or (results["prediction"] != "Placebo" and float(results["avg_qt_interval"]) > 435):
            firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).set({"warnings": 1})
        else:
            firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).set({"warnings": 0})
    else:
        warnings = int(doc.to_dict()["warnings"]) # Get current value of warnings in doc if exists
        # Check if warnings need to be increased
        if (results["prediction"] != "Placebo" and float(results["avg_p_wave"]) > 135) or (results["prediction"] != "Placebo" and float(results["avg_qt_interval"]) > 435):
            firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).update({"warnings": (warnings+1)})

    # Add entry to database
    firestore_client.collection("Users").document(userID).collection("weekly_reports").document(weekID).collection("reports").document(reportID).set(entry) 
    

# https://us-central1-test-auth-eaf78.cloudfunctions.net/addmessage?text=uppercasemetoo
# https://us-central1-eureka-44973.cloudfunctions.net/addmessage?text=uppercasemetoo
    