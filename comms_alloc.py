import firebase_admin
from firebase_admin import credentials, firestore
import random
''' pudusuuuuuuuuuuu'''
# Initialize Firebase Admin SDK
cred = credentials.Certificate('pyfirebasesdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def comms_alloc(community_name):
    # Query collections
    market_docs = db.collection('market').where('status', '==', 'open').stream()
    storage_docs = db.collection('storage').stream()
    fish_docs = db.collection('fish_data').stream()
    communities_docs = db.collection('communities').where('community_name', '==', community_name).stream()
    schedule_docs = db.collection('schedule').where('community_name', '==', community_name).stream()
    # Initialize an empty list to store price*quantity tuples
    all_price_quantity = []

    # Initialize a dictionary to store fish names and their total products
    fish_total_products = {}

    # Iterate through the documents in the market collection
    for doc in market_docs:
        data = doc.to_dict()
        fish_name = data.get('fishname')
        price = float(data.get('price', 0))
        quantity = float(data.get('quantity', 0))
        product = price * quantity

        if fish_name in fish_total_products:
            fish_total_products[fish_name] += product
        else:
            fish_total_products[fish_name] = product

    # Sort the fish_total_products dictionary based on the total product in descending order
    sorted_fish_total_products = dict(sorted(fish_total_products.items(), key=lambda item: item[1], reverse=True))

    # Print the results
    for fish_name, total_product in sorted_fish_total_products.items():
        print(f"Fish: {fish_name}, Total Product: {total_product}")

    # Get the fish names for the specified community
    skillset_fish_names = []

    # Iterate over the query results in the communities collection
    for doc in communities_docs:
        data = doc.to_dict()
        fish_names_array = data.get('fish_names', [])
        skillset_fish_names.extend(fish_names_array)

    print("Skillset Fish Names:", skillset_fish_names)

    intersection_list=list(set(skillset_fish_names).intersection(skillset_fish_names))
    print("intersection_list",intersection_list)

    # Get the fish names from storage for the all community
    storage_fish_names = []
    for doc in storage_docs:
        data = doc.to_dict()
        fish_name = data.get('fish_name',[])
        storage_fish_names.extend(fish_name)
    print(storage_fish_names)
    #now create a result list from the intersection list  that has all the fish that are not there in any storages
    result_list = list(set(intersection_list).difference(storage_fish_names))
    print("result_list",result_list)
    
    cut_short_list = result_list[:4]
    #now map all the fishes element in cut_short_list to its net_type from the fish_data db 
    net_type_list = {}
    for fish in cut_short_list:
        fish_docs = db.collection('fish_data').where('name', '==', fish).stream()
        for doc in fish_docs:
            data = doc.to_dict()
            net_type = data.get('net_type')
            net_type_list[fish] = net_type
            
    print(net_type_list)


   ######### #finally update thsi schedule in schedule_docs

    #update the data in schedule_docs 
    for doc in schedule_docs:
        doc_ref = db.collection('schedule').document(doc.id)
        doc_ref.set({
            'community_name': community_name,
            'fish_names': cut_short_list,
        }, merge=True)
    if doc not in schedule_docs:
        schedule_ref = db.collection('schedule')
        schedule_ref.document(community_name).set({
            'community_name': community_name,
            'fish_names': cut_short_list,
        })


    print ("Schedule updated successfully")
    return net_type_list

# # Example usage
comms_alloc("Community 6")
