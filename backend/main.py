from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(title="Sydney Housing Price Predictor")

# Allow Svelte frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), "models")

try:
    model = joblib.load(os.path.join(MODELS_DIR, "rf_housing_model.pkl"))
    model_features = joblib.load(os.path.join(MODELS_DIR, "model_features.pkl"))
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading model files: {e}")

class PropertyData(BaseModel):
    suburb: str
    property_type: str
    bedrooms: int
    bathrooms: int
    car_spaces: int
    land_size_sqm: float | None = None

@app.post("/predict")
def predict_price(data: PropertyData):
    try:
        # Handle Missing Land Size Logic
        land_size_missing = 1 if data.land_size_sqm is None or data.land_size_sqm == 0 else 0
        
        # If apartment/unit and land size missing, impute 0. 
        final_land_size = data.land_size_sqm
        if land_size_missing:
            if data.property_type in ["Apartment", "Unit", "Townhouse"]:
                final_land_size = 0.0
            else:
                final_land_size = 600.0 # Fallback median for houses

        bed_to_bath_ratio = data.bedrooms / max(data.bathrooms, 1)

        input_dict = {
            "beds": data.bedrooms,
            "baths": data.bathrooms,
            "car_spaces": data.car_spaces,
            "land_size_sqm": final_land_size,
            "land_size_is_missing": land_size_missing,
            "bed_to_bath_ratio": bed_to_bath_ratio,
            f"suburb_{data.suburb}": 1,
            f"property_type_{data.property_type}": 1
        }

        # Align with expected model features
        df_input = pd.DataFrame(0.0, index=[0], columns=model_features)
        
        # Populate the active features
        for key, value in input_dict.items():
            if key in df_input.columns:
                df_input.at[0, key] = value

        # Predict and inverse the log transformation
        log_prediction = model.predict(df_input)[0]
        actual_price = np.expm1(log_prediction)

        return {"predicted_price": round(actual_price, 2)}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))