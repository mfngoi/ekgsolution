# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import db_fn, firestore_fn, https_fn
from firebase_admin import initialize_app, db, firestore
import google.cloud.firestore

app = initialize_app()

@db_fn.on_value_created(reference="/messages/{pushId}/original")
def makeuppercase(event: db_fn.Event[db_fn.Change]) -> None:
    """Listens for new messages added to /messages/{pushId}/original and
    creates an uppercase version of the message to /messages/{pushId}/uppercase
    """

    # Grab the value that was written to the Realtime Database.
    original = event.data
    if not isinstance(original, str):
        print(f"Not a string: {event.reference}")
        return

    # Use the Admin SDK to set an "uppercase" sibling.
    print(f"Uppercasing {event.params['pushId']}: {original}")
    upper = original.upper()
    parent = db.reference(event.reference).parent
    if parent is None:
        print("Message can't be root node.")
        return
    parent.child("uppercase").set(upper)

# initialize_app()
#
#
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")
