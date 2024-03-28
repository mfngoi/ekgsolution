# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn, db_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore, db
import google.cloud.firestore

# Other modules
from datetime import datetime
import base64
import bitarray
import struct

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

@db_fn.on_value_created(reference="/particletest/{pushId}")
def addsignals(event: db_fn.Event[db_fn.Change]) -> None:

    # Access data
    data = event.data
    # print("Access dictionary attempt")
    # print(f"{data=}")

    # Decode signals base64 into "signals"
    # base64_string = data["json"]["signals"]
    # sample_string_bytes = base64.b64decode(base64_string)
    # b_array = bitarray.bitarray()
    # b_array = b_array.frombytes(sample_string_bytes)
    # print(f"{b_array}")

    # signals = []    # Array to store decoded values
    # for i in range(len(b_array)//12):
    #     start_idx = i * 12
    #     end_idx = (i+1) * 12
    #     # print(f"{b_array[start_idx:end_idx]=}")
    #     num_bits = bitarray.bitarray(b_array[start_idx : end_idx].to01() + ("0"*20), endian='little')
    #     num = struct.unpack("<L", num_bits)[0]
    #     signals.append(num)

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

    entry = {
        "signals": data["json"]["signals"],
    }

    # Connect to database
    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Check if weekly_reports document exists
    doc = firestore_client.collection("users").document(userID).collection("weekly_reports").document(weekID).get()

    # Add week if it does not exists
    if not doc.exists:
        print(f"{weekID} did not exist, creating document... ")
        firestore_client.collection("users").document(userID).collection("weekly_reports").document(weekID).set({"warnings": 0})

    # Push document to database
    print(f"Added report: {reportID} to user db... ")
    firestore_client.collection("users").document(userID).collection("weekly_reports").document(weekID).collection("reports").document(reportID).set(entry)



# https://us-central1-test-auth-eaf78.cloudfunctions.net/addmessage?text=uppercasemetoo
# https://us-central1-eureka-44973.cloudfunctions.net/addmessage?text=uppercasemetoo
    