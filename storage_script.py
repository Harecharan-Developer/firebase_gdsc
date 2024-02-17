import firebase_admin
from firebase_admin import credentials, firestore
import random

# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate("pyfirebasesdk.json")
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Define data for 20 communities
community_data = []

for i in range(1, 21):
    community_name = f"Community {i}"
    fish_name = []
    fish_amount = []
    # Append empty lists for fish_name and fish_amount
    community_data.append({
        'community_name': community_name,
        'fish_name': fish_name,
        'fish_amount': fish_amount
    })

# Create a batch object
batch = db.batch()

# Define the path to the collection in Firestore
collection_ref = db.collection('storage')

# Add each community document to the batch
for community in community_data:
    # Define the document reference
    doc_ref = collection_ref.document()
    # Set the data for the document
    batch.set(doc_ref, community)

# Commit the batch to Firestore
batch.commit()

print("Batch upload completed successfully.")
