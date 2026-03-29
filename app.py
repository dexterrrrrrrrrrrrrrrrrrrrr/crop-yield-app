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
    model_columns = ['Crop_Year', 'Area', 'State_Name_Karnataka', 'State_Name_Madhya Pradesh', 'State_Name_Maharashtra', 'State_Name_Manipur', 'State_Name_Tamil Nadu', 'State_Name_Telangana ', 'District_Name_AHMEDNAGAR', 'District_Name_AKOLA', 'District_Name_AMRAVATI', 'District_Name_ANANTAPUR', 'District_Name_ANUPPUR', 'District_Name_ASHOKNAGAR', 'District_Name_AURANGABAD', 'District_Name_BAGALKOT', 'District_Name_BALAGHAT', 'District_Name_BANGALORE RURAL', 'District_Name_BARWANI', 'District_Name_BEED', 'District_Name_BELGAUM', 'District_Name_BELLARY', 'District_Name_BENGALURU URBAN', 'District_Name_BETUL', 'District_Name_BHANDARA', 'District_Name_BHIND', 'District_Name_BHOPAL', 'District_Name_BIDAR', 'District_Name_BIJAPUR', 'District_Name_BISHNUPUR', 'District_Name_BULDHANA', 'District_Name_BURHANPUR', 'District_Name_CHAMARAJANAGAR', 'District_Name_CHANDEL', 'District_Name_CHANDRAPUR', 'District_Name_CHHATARPUR', 'District_Name_CHHINDWARA', 'District_Name_CHIKMAGALUR', 'District_Name_CHITRADURGA', 'District_Name_CHITTOOR', 'District_Name_CHURACHANDPUR', 'District_Name_COIMBATORE', 'District_Name_CUDDALORE', 'District_Name_DAMOH', 'District_Name_DATIA', 'District_Name_DAVANGERE', 'District_Name_DEWAS', 'District_Name_DHAR', 'District_Name_DHARMAPURI', 'District_Name_DHARWAD', 'District_Name_DHULE', 'District_Name_DINDIGUL', 'District_Name_DINDORI', 'District_Name_EAST GODAVARI', 'District_Name_ERODE', 'District_Name_GADAG', 'District_Name_GADCHIROLI', 'District_Name_GULBARGA', 'District_Name_GUNA', 'District_Name_GUNTUR', 'District_Name_GWALIOR', 'District_Name_HARDA', 'District_Name_HASSAN', 'District_Name_HAVERI', 'District_Name_HINGOLI', 'District_Name_HOSHANGABAD', 'District_Name_IMPHAL EAST', 'District_Name_IMPHAL WEST', 'District_Name_INDORE', 'District_Name_JABALPUR', 'District_Name_JALGAON', 'District_Name_JALNA', 'District_Name_JHABUA', 'District_Name_KADAPA', 'District_Name_KANCHIPURAM', 'District_Name_KANNIYAKUMARI', 'District_Name_KARIMNAGAR', 'District_Name_KARUR', 'District_Name_KATNI', 'District_Name_KHAMMAM', 'District_Name_KHANDWA', 'District_Name_KHARGONE', 'District_Name_KODAGU', 'District_Name_KOLAR', 'District_Name_KOLHAPUR', 'District_Name_KOPPAL', 'District_Name_KRISHNA', 'District_Name_KRISHNAGIRI', 'District_Name_KURNOOL', 'District_Name_LATUR', 'District_Name_MADURAI', 'District_Name_MAHBUBNAGAR', 'District_Name_MANDLA', 'District_Name_MANDSAUR', 'District_Name_MANDYA', 'District_Name_MEDAK', 'District_Name_MORENA', 'District_Name_MYSORE', 'District_Name_NAGAPATTINAM', 'District_Name_NAGPUR', 'District_Name_NALGONDA', 'District_Name_NAMAKKAL', 'District_Name_NANDED', 'District_Name_NANDURBAR', 'District_Name_NARSINGHPUR', 'District_Name_NASHIK', 'District_Name_NEEMUCH', 'District_Name_NIZAMABAD', 'District_Name_OSMANABAD', 'District_Name_PANNA', 'District_Name_PARBHANI', 'District_Name_PERAMBALUR', 'District_Name_PRAKASAM', 'District_Name_PUDUKKOTTAI', 'District_Name_PUNE', 'District_Name_RAICHUR', 'District_Name_RAIGAD', 'District_Name_RAISEN', 'District_Name_RAJGARH', 'District_Name_RAMANATHAPURAM', 'District_Name_RANGAREDDI', 'District_Name_RATLAM', 'District_Name_REWA', 'District_Name_SAGAR', 'District_Name_SALEM', 'District_Name_SANGLI', 'District_Name_SATARA', 'District_Name_SATNA', 'District_Name_SEHORE', 'District_Name_SENAPATI', 'District_Name_SEONI', 'District_Name_SHAHDOL', 'District_Name_SHAJAPUR', 'District_Name_SHEOPUR', 'District_Name_SHIMOGA', 'District_Name_SHIVPURI', 'District_Name_SIDHI', 'District_Name_SIVAGANGA', 'District_Name_SOLAPUR', 'District_Name_SPSR NELLORE', 'District_Name_SRIKAKULAM', 'District_Name_TAMENGLONG', 'District_Name_THANE', 'District_Name_THANJAVUR', 'District_Name_THE NILGIRIS', 'District_Name_THENI', 'District_Name_THIRUVALLUR', 'District_Name_THIRUVARUR', 'District_Name_THOUBAL', 'District_Name_TIKAMGARH', 'District_Name_TIRUCHIRAPPALLI', 'District_Name_TIRUNELVELI', 'District_Name_TIRUVANNAMALAI', 'District_Name_TUMKUR', 'District_Name_TUTICORIN', 'District_Name_UJJAIN', 'District_Name_UKHRUL', 'District_Name_UMARIA', 'District_Name_UTTAR KANNAD', 'District_Name_VELLORE', 'District_Name_VIDISHA', 'District_Name_VILLUPURAM', 'District_Name_VIRUDHUNAGAR', 'District_Name_VISAKHAPATANAM', 'District_Name_VIZIANAGARAM', 'District_Name_WARANGAL', 'District_Name_WARDHA', 'District_Name_WASHIM', 'District_Name_WEST GODAVARI', 'District_Name_YAVATMAL', 'Season_Rabi       ', 'Season_Whole Year ']
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