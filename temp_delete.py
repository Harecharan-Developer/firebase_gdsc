import firebase_admin
from firebase_admin import credentials, firestore
import random
''' pudusuuuuuuuuuuu'''
# Initialize Firebase Admin SDK
cred = credentials.Certificate('pyfirebasesdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
communities_docs = db.collection('communities').where('community_name', '==', 'Community 9').stream()
skillset_fish_names = []

# Iterate over the query results in the communities collection
for doc in communities_docs:
    data = doc.to_dict()
    fish_names_array = data.get('fish_names')
    skillset_fish_names.extend(fish_names_array)

print("Skillset Fish Names:", skillset_fish_names)

