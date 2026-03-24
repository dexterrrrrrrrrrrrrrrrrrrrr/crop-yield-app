import streamlit as st
import pandas as pd
import mlflow.pyfunc
from databricks import sql
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
    ["Karnataka", "Tamil Nadu", "Maharashtra"]
)

district = st.sidebar.selectbox(
    "District",
    ["Bangalore Rural", "Mysore", "Madurai"]
)

season = st.sidebar.selectbox(
    "Season",
    ["Rabi", "Kharif", "Whole Year"]
)

crop = st.sidebar.selectbox(
    "Crop",
    ["Tomato", "Onion", "Wheat"]
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
            # Load MLflow model
            model_uri = "runs:/eb428de9a2b94983bf0c830070f81cea/crop_yield_model"
            loaded_model = mlflow.pyfunc.load_model(model_uri)
            
            # Prepare input DataFrame
            input_df = pd.DataFrame([{
                "state": state,
                "district": district,
                "season": season,
                "crop": crop,
                "area": area
            }])
            
            # One-hot encode
            input_df = pd.get_dummies(input_df)
            
            # Align with training columns
            try:
                model_columns = loaded_model.metadata.get_input_schema().input_names()
            except:
                model_columns = loaded_model._model_impl.python_model._model.feature_names_in_
            
            for col in model_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            input_df = input_df[model_columns]
            
            # Make prediction
            prediction = loaded_model.predict(input_df)[0]
            
            # Display results
            st.success("✅ Prediction Complete!")
            
            # Create results layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Area Cultivated", f"{area} ha")
                st.metric("Crop", crop)
            
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
                    "crop": crop,
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

else:
    # Initial state - show instructions
    st.info("👈 Configure the input parameters in the sidebar and click **Predict Yield** to get started.")
    
    # Show sample data or statistics
    st.markdown("### 📖 About")
    st.markdown("""
    This application uses a machine learning model to predict crop production based on:
    - **State & District**: Geographic location
    - **Season**: Growing season (Rabi, Kharif, or Whole Year)
    - **Crop**: Type of crop being cultivated
    - **Area**: Cultivation area in hectares
    
    The model was trained using historical agricultural data and provides production estimates in tonnes.
    """)

# Footer
st.markdown("---")
st.caption("🌾 Crop Yield Prediction System | Powered by MLflow & Databricks")
