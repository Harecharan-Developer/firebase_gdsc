# Python
from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()

# Load the model when the application starts
with open('ml_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.post('/predict')
def predict(data: dict):
    try:
        # Extract the values from the input data
        Temp = data.get('Temp')
        Turbidity = data.get('Turbidity')
        Dissolved_Oxygen = data.get('Dissolved_Oxygen')
        PH = data.get('PH')
        Ammonia = data.get('Ammonia')
        Nitrate = data.get('Nitrate')

        # Convert the input data to a numpy array
        input_data = np.array([Temp, Turbidity, Dissolved_Oxygen, PH, Ammonia, Nitrate])

        # Use the model to make a prediction
        prediction = model.predict(input_data.reshape(1, -1))

        # Return the prediction
        return {"prediction": prediction.tolist()}
    except Exception as e:
        print("problem error in here ml api calll!", e)
        return str(e)