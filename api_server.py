from fastapi import FastAPI, Form, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
import pickle
import json  # Ensure json is imported correctly

app = FastAPI()

# Load the pkl file
with open('ml_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.post("/predict")
async def predict_fish(
    Temperature: float = Form(...),
    Turbidity: float = Form(...),
    Dissolved_Oxygen: float = Form(...),
    PH: float = Form(...),
    Ammonia: float = Form(...),
    Nitrate: float = Form(...),
    entry_id:int =Form(...),
    population:int = 50
):
    try:
        
        # Perform prediction using the loaded model
        prediction = model.predict([[entry_id, Temperature, Turbidity, Dissolved_Oxygen, PH, Ammonia, Nitrate, population]])
        # Prepare the response as a JSON object directly

        weight= prediction[0][0]  # Assuming model output format
        length= prediction[0][1]
        
        if length >= 20 and length <= 26 and weight >= 150 and weight <= 250:
            fish_type = "Rui"
        elif length >= 15 and length <= 25 and weight >= 180 and weight <= 300:
            fish_type = "Koi"
        elif length >= 18 and length <= 30 and weight >= 200 and weight <= 625:
            fish_type = "Silvercarp"
        elif length >= 10 and  weight >= 120:
            fish_type = "Karpio"
        else:
            fish_type = "Salmon"

        return fish_type  # No need to use json.dumps() here

    except Exception as e:
        return JSONResponse(content={"error": str(e)})
