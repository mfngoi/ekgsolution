# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn, db_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore, db
import google.cloud.firestore

import base64
# import bitarray

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


@db_fn.on_value_created(reference="/particle/{pushId}")
async def addsignals(event: db_fn.Event[db_fn.Change]) -> None:

    data = event.data
    print("Can you see this in the logs")
    print(f"{data=}")

    print("Access dictionary attempt")
    print(f"{data["coreid"]=}")
    print(f"{data["data"]=}")
    print(f"{data["published_at"]=}")

    try:

        # Connect to firestore database
        firestore_client: google.cloud.firestore.Client = firestore.client()
        # User information for firestore database
        userID = "Hv7dlyqYPhYhIOukasD7Yh8G1Du1"
        weekID = "week11"
        reportID = data["published_at"]
        entry = {
            "signals": data["data"],
        }

        # Check if weekly_reports exists by counting amount of documents in collection
        docs = await firestore_client.collection("Users").doc(userID).collection("weekly_reports").stream()
        length = 0
        async for doc in docs:
            length += 1
        if length == 0:  # If does not exist, initalize it with 0 warnings
            await firestore_client.collection("Users").doc(userID).collection("weekly_reports").doc(weekID).set({"warnings": 0})

        # Set report
        _, doc_ref = await firestore_client.collection("users").doc(userID).collection("weekly_reports").doc(weekID).collection("reports").doc(reportID).set(entry)
    except Exception as error:
        print("Error found:", error)






#     # base64_string = data["data"]

#     # sample_string_bytes = base64.b64decode(base64_string)
#     # print(f"{sample_string_bytes=}")

#     # try:
#     #     # Manipulating bits
#     #     ba = bitarray.bitarray()
#     #     ba.frombytes(sample_string_bytes)
#     #     print(f"{ba=}")
#     #     # print(f"{ba.bitarray(1)=}")
#     # except Exception as error:
#     #     print("An error occurred:", error)


# # https://us-central1-test-auth-eaf78.cloudfunctions.net/addmessage?text=uppercasemetoo
    # https://us-central1-eureka-44973.cloudfunctions.net/addMessage?text=uppercasemetoo

   # https://us-central1-eureka-44973.cloudfunctions.net/addmessage?text=uppercasemetoo
        
# # 100100000111
# # 001010110110

# # ChatGPT
# # Test Case of incoming bit array
# # 100100000111001010110110010101111010001001010001100101111011110101010111011011001100011101100000100011111100010100010111100001010101001110111110011111110110000111001011000110101010010000101001010101001011101100001011110000011110111100011010010100011010000100111010101000001010110001111110111110111011101010001101110100101000011010011000011011100000100001010100111000110011100110110011100111000011000101101001100110100001100000101100100010011000000010100011010110000001010101110011001011010101000101110110100001110001110000000001110110011010010100110011000111011110100001101101011000111110100001011001110010111110110101111101101111010100110011011111100100110101101101010000011111110101110000010110101011101110110011010000010111100110110010000100101011110010101111110110011001000001010101111000100010001000110011000110111