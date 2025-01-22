# Predictive Analysis for Manufacturing Operations

This project provides a RESTful API to predict machine downtime or production defects using a manufacturing dataset. The application is built with FastAPI and uses a supervised machine learning model to make predictions.

## Features

- **Upload Dataset**: Upload a CSV file containing manufacturing data.
- **Train Model**: Train a Logistic Regression model on the uploaded dataset.
- **Make Predictions**: Predict machine downtime based on input parameters such as production volume and maintenance hours.

---

## Prerequisites

- Python 3.8+
- pip (Python package manager)

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   uvicorn app:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. Upload Dataset

**Endpoint**: `POST /upload`

**Description**: Upload a CSV file containing manufacturing data.

**Request**:

- **Headers**: `Content-Type: multipart/form-data`
- **Body**: A CSV file with columns such as `Machine_ID`, `ProductionVolume`, `MaintenanceHours`, and `DefectStatus`.

**Response**:

```json
{
    "message": "File uploaded successfully",
    "columns": ["Machine_ID", "ProductionVolume", "MaintenanceHours", "DefectStatus"]
}
```

---

### 2. Train Model

**Endpoint**: `POST /train`

**Description**: Train a Logistic Regression model on the uploaded dataset.

**Response**:

```json
{
    "message": "Model trained successfully",
    "metrics": {
        "accuracy": 0.87,
        "classification_report": {
            "0": {
                "precision": 0.89,
                "recall": 0.85,
                "f1-score": 0.87,
                "support": 50
            },
            "1": {
                "precision": 0.86,
                "recall": 0.90,
                "f1-score": 0.88,
                "support": 50
            }
        }
    }
}
```

---

### 3. Make Prediction

**Endpoint**: `POST /predict`

**Description**: Make a prediction based on input parameters.

**Request**:

- **Headers**: `Content-Type: application/json`
- **Body**:

```json
{
    "ProductionVolume": 1200,
    "MaintenanceHours": 5
}
```

**Response**:

```json
{
    "Downtime": "Yes",
    "Confidence": 0.92
}
```

---

## Example Usage

### Using cURL

1. **Upload Dataset**

   ```bash
   curl -X POST "http://127.0.0.1:8000/upload" -F "file=@path_to_your_dataset.csv"
   ```

2. **Train Model**

   ```bash
   curl -X POST "http://127.0.0.1:8000/train"
   ```

3. **Make Prediction**

   ```bash
   curl -X POST "http://127.0.0.1:8000/predict" \
   -H "Content-Type: application/json" \
   -d '{"ProductionVolume": 1200, "MaintenanceHours": 5}'
   ```

---

## Notes

- Ensure the dataset contains the following columns: `Machine_ID`, `ProductionVolume`, `MaintenanceHours`, `DefectStatus`.
- `DefectStatus` should be binary (e.g., `0` for no defect, `1` for defect).
- Use Postman or similar tools to test the API endpoints interactively.

