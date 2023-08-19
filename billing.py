from firebase_admin import firestore

db = firestore.client()


def pushUsage(usage):
    try:
        # Add a new document with a random document ID
        write_time, doc_ref = db.collection("Billing").add(usage)
        if doc_ref.id:
            print(
                f"Document with ID {doc_ref.id} was successfully added at {write_time}."
            )
            return 200
        else:
            print("Failed to add the document.")
            return 500
    except Exception as e:
        print(f"Error occurred: {e}")
        return 500
