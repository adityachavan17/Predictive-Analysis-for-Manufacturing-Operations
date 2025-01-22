import logging
import joblib
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report


app = FastAPI()


logging.basicConfig(level=logging.INFO)


model_path = "model.pkl"
scaler_path = "scaler.pkl"

uploaded_data = None
model = None
scaler = None


try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    logging.info("Model and scaler loaded successfully.")
except Exception as e:
    logging.warning(f"Failed to load model or scaler: {e}")
    model = None
    scaler = None

class PredictionRequest(BaseModel):
    ProductionVolume: float
    MaintenanceHours: float


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global uploaded_data
    try:
        
        if file is None:
            raise HTTPException(status_code=400, detail="No file uploaded.")
        
        
        uploaded_data = pd.read_csv(file.file)
        logging.info(f"Uploaded data columns: {uploaded_data.columns.tolist()}")
        return {"message": "File uploaded successfully", "columns": uploaded_data.columns.tolist()}
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=400, detail="Failed to upload file")


@app.post("/train")
def train_model():
    global model, scaler, uploaded_data
    try:
        if uploaded_data is None:
            logging.error("No data uploaded.")
            raise HTTPException(status_code=400, detail="No data uploaded. Please upload a dataset first.")

       
        X = uploaded_data[['ProductionVolume', 'MaintenanceHours']]
        y = uploaded_data['DefectStatus']
        logging.info(f"Training model with {len(X)} samples.")

    
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

  
        model = LogisticRegression(random_state=42)
        model.fit(X_train_scaled, y_train)


        y_pred = model.predict(X_test_scaled)
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "classification_report": classification_report(y_test, y_pred, output_dict=True),
        }

        
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)

        logging.info("Model trained and saved successfully.")
        return {"message": "Model trained successfully", "metrics": metrics}
    except Exception as e:
        logging.error(f"Error training model: {e}")
        raise HTTPException(status_code=500, detail="Failed to train model")


@app.post("/predict")
def predict(request: PredictionRequest):
    global model, scaler
    try:
        if model is None or scaler is None:
            logging.error("Model or scaler not initialized.")
            raise HTTPException(status_code=400, detail="Model not trained. Please train the model first.")

        
        input_data = pd.DataFrame([request.dict()])
        input_scaled = scaler.transform(input_data)

        
        prediction = model.predict(input_scaled)
        confidence = model.predict_proba(input_scaled).max()

        logging.info(f"Prediction: {prediction[0]}, Confidence: {confidence}")
        return {"Downtime": "Yes" if prediction[0] == 1 else "No", "Confidence": round(confidence, 2)}
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")


# Run the server using: uvicorn app:app --reload
