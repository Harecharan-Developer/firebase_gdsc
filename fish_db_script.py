import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate(r"C:\Users\DELL\Downloads\firebase_gdsc\pyfirebasesdk.json")
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Define the fish data dictionary with viable seasons and net types
fish_data = {
    'Salmon': {'name': 'Salmon', 'viable_season': 'Spring', 'net_type': 'Gill net'},
    'Tuna': {'name': 'Tuna', 'viable_season': 'Spring', 'net_type': 'Purse seine'},
    'Cod': {'name': 'Cod', 'viable_season': 'Spring', 'net_type': 'Trawl net'},
    'Trout': {'name': 'Trout', 'viable_season': 'Spring', 'net_type': 'Fly fishing net'},
    'Sardines': {'name': 'Sardines', 'viable_season': 'Spring', 'net_type': 'Purse seine'},
    'Haddock': {'name': 'Haddock', 'viable_season': 'Summer', 'net_type': 'Trawl net'},
    'Mackerel': {'name': 'Mackerel', 'viable_season': 'Summer', 'net_type': 'Purse seine'},
    'Halibut': {'name': 'Halibut', 'viable_season': 'Summer', 'net_type': 'Bottom trawl net'},
    'Perch': {'name': 'Perch', 'viable_season': 'Summer', 'net_type': 'Cast net'},
    'Bass': {'name': 'Bass', 'viable_season': 'Summer', 'net_type': 'Gill net'},
    'Catfish': {'name': 'Catfish', 'viable_season': 'Fall', 'net_type': 'Trap net'},
    'Pike': {'name': 'Pike', 'viable_season': 'Fall', 'net_type': 'Spearing net'},
    'Grouper': {'name': 'Grouper', 'viable_season': 'Fall', 'net_type': 'Spearfishing gear'},
    'Snapper': {'name': 'Snapper', 'viable_season': 'Fall', 'net_type': 'Bottom longline'},
    'Mahi Mahi': {'name': 'Mahi Mahi', 'viable_season': 'Fall', 'net_type': 'Trolling gear'},
    'Carp': {'name': 'Carp', 'viable_season': 'Winter', 'net_type': 'Gill net'},
    'Swordfish': {'name': 'Swordfish', 'viable_season': 'Winter', 'net_type': 'Longline'},
    'Yellowtail': {'name': 'Yellowtail', 'viable_season': 'Winter', 'net_type': 'Handline'},
    'Herring': {'name': 'Herring', 'viable_season': 'Winter', 'net_type': 'Purse seine'},
    'Anchovies': {'name': 'Anchovies', 'viable_season': 'Winter', 'net_type': 'Purse seine'}
}

# Create a batch object
batch = db.batch()

# Define the path to the collection in Firestore
collection_ref = db.collection('fish_data')

# Add each fish document to the batch
for fish, data in fish_data.items():
    # Define the document reference
    doc_ref = collection_ref.document(fish)
    # Set the data for the document
    batch.set(doc_ref, {'name': data['name'], 'viable_season': data['viable_season'], 'net_type': data['net_type']})

# Commit the batch to Firestore
batch.commit()

print("Batch upload completed successfully.")
