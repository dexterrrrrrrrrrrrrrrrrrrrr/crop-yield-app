# 🌾 Crop Yield Prediction App

A Streamlit-based Databricks App for predicting crop production using machine learning.

## Features

- Interactive UI for inputting agricultural parameters
- Real-time crop yield predictions using MLflow model
- Automatic logging of predictions to Delta table
- Support for multiple states, districts, seasons, and crops

## Files

- `app.yaml` - Databricks App configuration
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies

## Deployment Instructions

### Option 1: Using Databricks CLI

1. Install Databricks CLI:
   ```bash
   pip install databricks-cli
   ```

2. Configure authentication:
   ```bash
   databricks configure --token
   ```

3. Deploy the app:
   ```bash
   databricks apps create crop-yield-app
   databricks apps deploy crop-yield-app --source-code-path /Workspace/Users/<your-email>/crop-yield-app
   ```

### Option 2: Using Databricks UI

1. Navigate to **App** in the Databricks workspace
2. Click **Create App**
3. Select **From files**
4. Choose the `crop-yield-app` folder
5. Click **Deploy**

### Option 3: Using Databricks SDK (Python)

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Create app
app = w.apps.create(
    name="crop-yield-app",
    description="Crop yield prediction system"
)

# Deploy app
w.apps.deploy(
    app_name="crop-yield-app",
    source_code_path="/Workspace/Users/<your-email>/crop-yield-app"
)
```

## Model Requirements

The app expects an MLflow model with run ID: `eb428de9a2b94983bf0c830070f81cea`

Ensure this model is registered and accessible in your Databricks workspace.

## Usage

1. Select state, district, season, and crop from the dropdowns
2. Enter the cultivation area in hectares
3. Click "Predict Yield" button
4. View the predicted production in tonnes

## Data Logging

Predictions are automatically logged to the `crop_predictions_log` Delta table for tracking and analysis.
