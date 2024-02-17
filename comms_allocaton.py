import firebase_admin
from firebase_admin import credentials, firestore
import random

def comms_alloc(community_name):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate(r"C:\Users\DELL\Downloads\firebase_gdsc\pyfirebasesdk.json")
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Query the 'market' collection for documents with 'status' field set to 'open'
    open_market_docs = db.collection('market').where('status', '==', 'open').stream()

    # Initialize a dictionary to store fish names and their sorted price-quantity tuples
    fish_price_quantity = {}

    # Iterate through the documents
    for doc in open_market_docs:
        # Get the data from the document
        data = doc.to_dict()
        fish_name = data.get('fishname')
        price = float(data.get('price', 0))  # Convert price to float, default to 0 if not available
        quantity = float(data.get('quantity', 0))  # Convert quantity to float, default to 0 if not available

        # Calculate the product of price and quantity
        product = price * quantity

        # Add the price-quantity tuple to the list corresponding to the fish name
        if fish_name in fish_price_quantity:
            fish_price_quantity[fish_name].append((price, quantity))
        else:
            fish_price_quantity[fish_name] = [(price, quantity)]

    # Sort the price-quantity tuples for each fish based on the product
    for fish_name, price_quantity_list in fish_price_quantity.items():
        sorted_price_quantity = sorted(price_quantity_list, key=lambda x: x[0] * x[1],reverse=True)
        fish_price_quantity[fish_name] = sorted_price_quantity

    # Print the results
    for fish_name, price_quantity_list in fish_price_quantity.items():
        print(f"Fish: {fish_name}")
        for price, quantity in price_quantity_list:
            print(f"Price: {price}, Quantity: {quantity}")
        print()  # Add a newline for better readability
    
    #create a list of all the fish in the dict 
    order_list = list(fish_price_quantity.keys())
    print(order_list)

    # Query the 'communities' collection for a document where 'community_name' matches the input
    community_docs = db.collection('communities').where('community_name', '==', community_name).stream()
    
    # initiales score
    score=0

    # Initialize a list to store the fish names
    community_fish_list = []

    # Iterate through the documents
    for doc in community_docs:
        # Get the data from the document
        data = doc.to_dict()
        fish_name = data.get('fish_names')  # Get the 'fish_name' field
        score = data.get('score')
        print(score)
        # Add the fish name to the list
        if fish_name is not None:
            community_fish_list.append(fish_name)
    flattened_fish = [fish for sublist in community_fish_list for fish in sublist]
    community_fish_list = flattened_fish


    # Print the list of fish names
    print("Fish in community:", community_fish_list)

    intersection_list =list(set(community_fish_list).intersection(order_list))
    print("Intersection in community:", intersection_list)
    
    subract_amount = 0
    # now update the Schedule db with the list of fish names and the amount to capture for the community
    # Create a reference to the Schedule collection
    schedule_ref = db.collection('Schedule')
    if score >7 :
        # Create a document with the community name as the document ID
        schedule_ref.document(community_name).set({
            'fish_names': intersection_list,
            'amount': 1000
        })
        subract_amount = 1000
    elif score <7 and score > 4 :
        schedule_ref.document(community_name).set({
            'fish_names': community_fish_list,
            'amount': 500
        })
        subract_amount = 500
    else:
        schedule_ref.document(community_name).set({
            'fish_names': community_fish_list,
            'amount': 200
        })
        subract_amount = 200
    
    # now update the market db by reducing the amount of fish available from the original order
    batch = db.batch()
    # Iterate through the documents
    for doc in open_market_docs:
        # Get the data from the document
        data = doc.to_dict()
        fish_name = data.get('fishname')
        price = float(data.get('price', 0))  # Convert price to float, default to 0 if not available
        quantity = float(data.get('quantity', 0))  # Convert quantity to float, default to 0 if not available
        if fish_name in intersection_list:
            # Create a document reference with the document ID
            doc_ref = db.collection('market').document(doc.id)
            # Update the quantity of the fish
            batch.update(doc_ref, {'quantity': quantity - subract_amount})


    print("Schedule updated successfully")

# Call the function
comms_alloc("Community 3")
