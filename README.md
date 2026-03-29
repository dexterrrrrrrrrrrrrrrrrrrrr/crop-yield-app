# 🌾 Crop Yield Prediction App

A Streamlit app for predicting crop yield using MLflow model.

## Quick Local Run
```
export PATH=$PATH:/Users/anuragpaul/Library/Python/3.9/bin
streamlit run app.py
```
Open http://localhost:8501

## Deploy to Streamlit Cloud (Recommended)
1. Ensure repo public: GitHub → Settings → Danger Zone → Make public.
2. https://share.streamlit.io
3. New app → GitHub repo (`crop-yield-app`) → Branch `main` → `app.py` → Deploy.

App live at `https://[appname].streamlit.app`

## Features
- Predict yield from state, district, season, crop, area, year.
- MLflow model from `./model/`.
- Fallback dummy model.

## Original Databricks Instructions
[Previous content remains for reference...]

Files: `app.py`, `requirements.txt` (fixed), `model/`, `TODO.md`.

