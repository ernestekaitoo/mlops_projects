import joblib
import os
import pandas as pd
from fastapi import FastAPI, HTTPException
# We import our data rules from the file we made earlier
from .data_models import PredictionDataset, PredictionResponse

app = FastAPI(title="Student Success API")

# 1. THE GPS: Locate the model file (Go up one level from 'src' to 'models')
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.joblib")

# 2. LOAD THE BRAIN: Try to load the model when the app starts
try:
    model_pipe = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    model_pipe = None
    print("❌ Warning: model.joblib not found. Did you run 'make train'?")

@app.get("/")
def home():
    return {"message": "Student Success Predictor is Online. Go to /docs for the UI."}

@app.post("/predictions", response_model=PredictionResponse)
def predict(data: PredictionDataset):
    """
    Takes student data and returns a prediction.
    """
    if model_pipe is None:
        raise HTTPException(status_code=503, detail="Model is not trained yet.")

    # Convert the incoming JSON data into a Pandas DataFrame (what the model expects)
    # We use data.dict(by_alias=True) to match the CSV column names exactly
    input_df = pd.DataFrame([data.dict(by_alias=True)])

    # Make the prediction
    prediction = model_pipe.predict(input_df)[0]

    # Return the result in the format we defined in data_models.py
    return {"predicted_academic_success_score": str(prediction)}