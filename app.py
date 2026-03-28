import streamlit as st
import pandas as pd
import pickle
import os
import mlflow

from sklearn.dummy import DummyRegressor

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌾",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    try:
        model = mlflow.sklearn.load_model("model/")
        st.success("✅ ML Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f"❌ Model load failed: {str(e)}")
        st.info("Using dummy model as fallback...")
        # Fallback dummy
        X_dummy = pd.DataFrame([{col: 0 for col in model_columns}])
        X_dummy.loc[0, "Crop_Year"] = 2015
        X_dummy.loc[0, "Area"] = 10
        y_dummy = [20]
        dummy_model = DummyRegressor(strategy="mean")
        dummy_model.fit(X_dummy, y_dummy)
        return dummy_model

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

# Feature columns handled dynamically from model.feature_names_in_

# ---------------- PREDICTION ----------------
if st.sidebar.button("🔮 Predict Yield"):

    with st.spinner("Predicting..."):
        model = load_model()
        if model:
            try:
                state_col = f"State_{state}"
                district_col = f"District_{district}"
                season_col = f"Season_{season}"
                crop_col = f"Crop_{crop}"

                feature_names = model.feature_names_in_.tolist()
                input_data = {col: 0.0 for col in feature_names}
                input_data["Crop_Year"] = float(crop_year)
                input_data["Area"] = float(area)

                for col in [state_col, district_col, season_col, crop_col]:
                    if col in feature_names:
                        input_data[col] = 1.0

                input_df = pd.DataFrame([input_data])

                # Prediction
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
st.caption("🌾 Built with Streamlit + Pickle")