import streamlit as st
import pandas as pd
import mlflow.pyfunc

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌾",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return mlflow.pyfunc.load_model("./model")

# ---------------- TITLE ----------------
st.title("🌾 Crop Yield Prediction System")
st.markdown("Predict crop production based on location, season, crop type, and cultivation area.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Input Parameters")

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
    ["Rabi", "Kharif", "Whole Year"]
)

crop = st.sidebar.selectbox(
    "Crop",
    ["Rice", "Wheat", "Maize", "Sugarcane", "Cotton"]
)

crop_year = st.sidebar.number_input(
    "Crop Year",
    min_value=1997,
    max_value=2030,
    value=2015
)

area = st.sidebar.number_input(
    "Area (hectares)",
    min_value=0.1,
    max_value=10000.0,
    value=10.0
)

# ---------------- PREDICTION ----------------
if st.sidebar.button("🔮 Predict Yield"):

    with st.spinner("Loading model and predicting..."):
        try:
            model = load_model()

            # Get model columns safely
            try:
                model_columns = model.metadata.signature.inputs.input_names()
            except:
                st.error("❌ Could not read model schema. Please define columns manually.")
                st.stop()

            # Clean column names
            model_columns = [col.strip() for col in model_columns]

            # Initialize all features to 0
            input_data = {col: 0 for col in model_columns}

            # Add numeric inputs
            input_data["Crop_Year"] = crop_year
            input_data["Area"] = area

            # ---------------- ENCODING ----------------

            # State encoding
            state_col = f"State_Name_{state}"
            if state_col in input_data:
                input_data[state_col] = 1

            # District encoding
            district_col = f"District_Name_{district}"
            if district_col in input_data:
                input_data[district_col] = 1

            # Season encoding
            season_col = f"Season_{season}"
            if season_col in input_data:
                input_data[season_col] = 1

            # Crop encoding
            crop_col = f"Crop_{crop}"
            if crop_col in input_data:
                input_data[crop_col] = 1

            # Create dataframe
            input_df = pd.DataFrame([input_data])
            input_df = input_df.reindex(columns=model_columns, fill_value=0)

            # Predict
            prediction = model.predict(input_df)[0]

            # ---------------- OUTPUT ----------------
            st.success("✅ Prediction Complete!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Area", f"{area} ha")
                st.metric("Year", crop_year)

            with col2:
                st.metric("Season", season)
                st.metric("Location", f"{district}, {state}")

            st.markdown("---")
            st.markdown("### 📊 Predicted Production")
            st.markdown(f"# {prediction:.2f} Tonnes")

            yield_per_ha = prediction / area
            st.info(f"Yield per hectare: {yield_per_ha:.2f} Tonnes/ha")

        except Exception as e:
            st.error("❌ Prediction Failed")
            st.exception(e)

            with st.expander("🔍 Debug Info"):
                st.write("Model Columns:", model_columns if 'model_columns' in locals() else "Not loaded")
                st.write("Input Data:", input_data if 'input_data' in locals() else "Not created")

# ---------------- DEFAULT SCREEN ----------------
else:
    st.info("👈 Configure inputs in sidebar and click Predict Yield")

    st.markdown("""
    ### 📖 About
    This ML model predicts crop production using:
    - Location (State & District)
    - Season
    - Crop type
    - Area & Year
    
    Output is in **Tonnes**.
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🌾 Built with Streamlit + MLflow")