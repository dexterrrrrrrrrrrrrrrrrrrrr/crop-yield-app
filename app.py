import streamlit as st
import pandas as pd
import mlflow.pyfunc
import os

# Page configuration
st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌾",
    layout="centered"
)

# Title and description
st.title("🌾 Crop Yield Prediction System")
st.markdown("Predict crop production based on location, season, crop type, and cultivation area.")

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Input widgets
state = st.sidebar.selectbox(
    "State",
    ["Karnataka", "Tamil Nadu", "Maharashtra", "Madhya Pradesh", "Manipur", "Telangana"]
)

district = st.sidebar.selectbox(
    "District",
    ["BANGALORE RURAL", "MYSORE", "MADURAI", "PUNE", "INDORE", "AHMEDNAGAR", 
     "BELGAUM", "COIMBATORE", "NASHIK", "SOLAPUR"]
)

season = st.sidebar.selectbox(
    "Season",
    ["Rabi", "Whole Year", "Kharif"]
)

crop_year = st.sidebar.number_input(
    "Crop Year",
    min_value=1997,
    max_value=2030,
    value=2015,
    step=1
)

area = st.sidebar.number_input(
    "Area (hectares)",
    min_value=0.1,
    max_value=10000.0,
    value=10.0,
    step=0.1
)

# Predict button
if st.sidebar.button("🔮 Predict Yield", type="primary"):
    with st.spinner("Loading model and making prediction..."):
        try:
            # Load MLflow model from Unity Catalog
            model_uri = "models:/workspace.default.crop_yield_model/1"
            loaded_model = mlflow.pyfunc.load_model(model_uri)
            
            # Get the model's expected input schema
            try:
                input_schema = loaded_model.metadata.get_input_schema()
                model_columns = input_schema.input_names()
                st.sidebar.success(f"✓ Model loaded ({len(model_columns)} features)")
            except Exception as schema_error:
                st.error(f"Could not get model schema: {schema_error}")
                raise
            
            # Initialize input with base features
            input_data = {
                "Crop_Year": crop_year,
                "Area": area
            }
            
            # Initialize ALL model features to False/0
            for col in model_columns:
                if col not in input_data:
                    input_data[col] = False
            
            # Set the actual values for selected inputs
            # State encoding (note: "Telangana " has a trailing space in the model)
            state_mapping = {
                "Karnataka": "State_Name_Karnataka",
                "Madhya Pradesh": "State_Name_Madhya Pradesh",
                "Maharashtra": "State_Name_Maharashtra",
                "Manipur": "State_Name_Manipur",
                "Tamil Nadu": "State_Name_Tamil Nadu",
                "Telangana": "State_Name_Telangana "  # Note trailing space
            }
            if state in state_mapping:
                feature_name = state_mapping[state]
                if feature_name in input_data:
                    input_data[feature_name] = True
            
            # District encoding
            district_feature = f"District_Name_{district}"
            if district_feature in input_data:
                input_data[district_feature] = True
            
            # Season encoding (note: trailing spaces in model)
            if season == "Rabi" and "Season_Rabi       " in input_data:
                input_data["Season_Rabi       "] = True
            elif season == "Whole Year" and "Season_Whole Year " in input_data:
                input_data["Season_Whole Year "] = True
            # Kharif is the reference category (all False)
            
            # Create DataFrame with correct column order
            input_df = pd.DataFrame([input_data])
            input_df = input_df[model_columns]  # Ensure correct order
            
            # Make prediction
            prediction = loaded_model.predict(input_df)[0]
            
            # Display results
            st.success("✅ Prediction Complete!")
            
            # Create results layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Area Cultivated", f"{area} ha")
                st.metric("Crop Year", crop_year)
            
            with col2:
                st.metric("Season", season)
                st.metric("Location", f"{district}, {state}")
            
            # Highlight predicted production
            st.markdown("---")
            st.markdown("### 📊 Predicted Production")
            st.markdown(f"# {prediction:.2f} Tonnes")
            
            # Calculate yield per hectare
            yield_per_ha = prediction / area
            st.info(f"**Yield per hectare:** {yield_per_ha:.2f} Tonnes/ha")
            
            # Optional: Log prediction to Delta Table
            try:
                data_to_log = pd.DataFrame([{
                    "state": state,
                    "district": district,
                    "season": season,
                    "crop_year": crop_year,
                    "area": area,
                    "predicted_production": prediction,
                    "timestamp": pd.Timestamp.now()
                }])
                
                # Save to Delta table
                from databricks.sdk.runtime import spark
                spark_df = spark.createDataFrame(data_to_log)
                spark_df.write.format("delta").mode("append").saveAsTable("crop_predictions_log")
                
                st.caption("✓ Prediction logged to Delta table")
            except Exception as log_error:
                st.caption(f"⚠️ Could not log prediction: {str(log_error)}")
                
        except Exception as e:
            st.error(f"❌ Error during prediction: {str(e)}")
            st.exception(e)
            
            # Debug information
            with st.expander("🔍 Debug Information"):
                st.write("**Error Details:**")
                st.code(str(e))
                st.write("**Input Values:**")
                st.json({
                    "state": state,
                    "district": district,
                    "season": season,
                    "crop_year": crop_year,
                    "area": area
                })

else:
    # Initial state - show instructions
    st.info("👈 Configure the input parameters in the sidebar and click **Predict Yield** to get started.")
    
    # Show sample data or statistics
    st.markdown("### 📖 About")
    st.markdown("""
    This application uses a machine learning model to predict crop production based on:
    - **State & District**: Geographic location
    - **Season**: Growing season (Rabi, Kharif, or Whole Year)
    - **Crop Year**: Year of cultivation
    - **Area**: Cultivation area in hectares
    
    The model was trained using historical agricultural data and provides production estimates in tonnes.
    
    **Model Information:**
    - Registry: Unity Catalog
    - Model: `workspace.default.crop_yield_model`
    - Version: 1
    - Algorithm: Random Forest Regressor
    - Features: 172 (including one-hot encoded categorical variables)
    """)
    
    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. Select the **State** and **District** from the dropdown menus
    2. Choose the **Season** for cultivation
    3. Enter the **Crop Year** (historical or future)
    4. Specify the **Area** in hectares
    5. Click **Predict Yield** to get production estimates
    """)

# Footer
st.markdown("---")
st.caption("🌾 Crop Yield Prediction System | Powered by MLflow & Databricks Unity Catalog")
