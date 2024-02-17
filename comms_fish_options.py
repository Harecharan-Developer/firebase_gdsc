import firebase_admin
from firebase_admin import credentials, firestore
import random

# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate(r"C:\Users\DELL\Downloads\firebase_gdsc\pyfirebasesdk.json")
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Define the list of fishes
fishes = [
    "Salmon",
    "Tuna",
    "Cod",
    "Trout",
    "Sardines",
    "Haddock",
    "Mackerel",
    "Halibut",
    "Perch",
    "Catfish",
    "Grouper",
    "Snapper",
    "Mahi Mahi",
    "Carp",
    "Swordfish",
    "Yellowtail",
    "Herring",
    "Anchovies"
]

# Define the list of community names
community_names = [
    "Community 1",
    "Community 2",
    "Community 3",
    "Community 4",
    "Community 5",
    "Community 6",
    "Community 7",
    "Community 8",
    "Community 9",
    "Community 10",
    "Community 11",
    "Community 12",
    "Community 13",
    "Community 14",
    "Community 15",
    "Community 16",
    "Community 17",
    "Community 18",
    "Community 19",
    "Community 20"
]

# Create a dictionary to store community names and associated fish names
community_fish = {}

# Assign random fish names to each community
for community_name in community_names:
    # Randomly select 3 to 5 fish names for each community
    num_fish = random.randint(10, 15)
    fish_names = random.sample(fishes, num_fish)
    community_fish[community_name] = fish_names

# Initialize a batched write
batch = db.batch()

# Add documents to the Firestore collection within the batch
for community_name, fish_names in community_fish.items():
    # Create a document reference without specifying the document ID (Firestore will auto-generate one)
    doc_ref = db.collection("communities").document()

    # Set the data for the document
    doc_data = {
        "community_name": community_name,
        "fish_names": fish_names,
        "score": 5  # Add 'score' field with a default value of 5
    }
    batch.set(doc_ref, doc_data)

# Commit the batched write operation
try:
    batch.commit()
    print("Batched write operation successful")
except Exception as e:
    print(f"Error committing batched write operation: {e}")
