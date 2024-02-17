    for doc in community_docs:
        # Get the data from the document
        data = doc.to_dict()
        score = data.get('score')  # Get the 'score' field