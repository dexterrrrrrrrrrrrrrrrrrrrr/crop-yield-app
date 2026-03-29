# 🌾 Crop Yield Prediction App

A **Streamlit web application** for predicting crop yield using machine learning models. Input state, district, season, crop type, area, and year to get real-time yield predictions. Includes a fallback dummy model for testing and smooth functionality without full model access.  

**Live Demo:** [Open the app](https://crop-yield-app-bgvwzbzylwskquhwjgwric.streamlit.app/)  

---

## 🚀 Quick Local Run
```bash
# Add Python bin to PATH
export PATH=$PATH:/Users/anuragpaul/Library/Python/3.9/bin

# Run the Streamlit app
streamlit run app.py
```
## ☁️ Deploy to Streamlit Cloud (Recommended)
	1.	Make your GitHub repo public
	•	GitHub → Settings → Danger Zone → Make public
	2.	Go to Streamlit Cloud￼
	3.	Click New app → Select your GitHub repo (crop-yield-app) → Branch main → app.py → Deploy

Your live app will be available at https://crop-yield-app-bgvwzbzylwskquhwjgwric.streamlit.app/

⸻

## 🌟 Features
	•	Predict crop yield from State, District, Season, Crop, Area, Year
	•	MLflow model integration (./model/)
	•	Fallback dummy model ensures full functionality
	•	Quick, interactive Streamlit interface

⸻

## 🛠 Built With
	•	Streamlit￼ – Web application framework
	•	MLflow￼ – Model management and deployment
	•	Python 3.9 – Core language
	•	pandas / scikit-learn – Data preprocessing & ML model support

⸻

## ⚡ Usage
	1.	Select State, District, Season, Crop, Area, Year
	2.	Submit to receive predicted yield
	3.	Use predictions for planning and analysis

## 📄 Files
- `app.py` – Main Streamlit app  
- `requirements.txt` – Python dependencies  
- `model/` – MLflow model files  
- `TODO.md` – Future improvements and notes  

---

## 🔄 Workflow

1. **User Input**  
   - User selects **State, District, Season, Crop, Area, and Year** from the Streamlit interface.

2. **Data Preprocessing**  
   - Inputs are converted into the **format required by the ML model**.  
   - Handles missing values and categorical encoding if necessary.  

3. **Model Prediction**  
   - **MLflow model** (`model/`) is loaded.  
   - Preprocessed inputs are fed into the model to **predict crop yield**.  
   - If MLflow model is unavailable, a **fallback dummy model** provides sample predictions.

4. **Post-Processing & Output**  
   - Predicted yield is formatted for display.  
   - Output is shown in **Streamlit UI** with optional charts or tables.  

5. **User Feedback / Export (Optional)**  
   - Users can **record or export predictions** for analysis.  
   - Future versions may include CSV export or batch predictions.

---

This workflow ensures **fast, reliable predictions** with a smooth user experience and graceful fallback handling.
