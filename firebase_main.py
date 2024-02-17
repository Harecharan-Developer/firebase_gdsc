import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("pyfirebasesdk.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

market=db.collection("Buyers").get()
print(market)
for doc in market:
    print(doc.to_dict())