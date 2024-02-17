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
    "Salmon", "Tuna", "Cod", "Trout", "Sardines", "Haddock", "Mackerel",
    "Halibut", "Perch", "Catfish", "Grouper", "Snapper", "Mahi Mahi", 
    "Carp", "Swordfish", "Yellowtail", "Herring", "Anchovies"
]

# Initialize a batched write
batch = db.batch()

# Update 20 subcollections in a single batch
for _ in range(20):
    # Generate random data for the document
    buyer_id = "PpleV39pJRUyVxrXLxloGZGiWSl1"
    buyer_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8)).upper()
    fish_name = random.choice(fishes)
    price = random.randint(100, 1000)
    quantity = random.randint(100, 1000)
    status = "open"

    # Create a document reference without specifying the document ID (Firestore will auto-generate one)
    doc_ref = db.collection("market").document()

    # Set the data for the document
    doc_data = {
        "buyerid": buyer_id,
        "buyername": buyer_name,
        "fishname": fish_name,
        "price": price,
        "quantity": quantity,
        "status": status
    }

    # Add the set operation to the batch
    batch.set(doc_ref, doc_data)

# Commit the batched write operation
batch.commit()

print("Data uploaded successfully as a single batch.")
