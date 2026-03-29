# Streamlit Deployment TODO

## Approved Plan (Minimal Changes - Keep Exact Files)

### 1. ✅ Create this TODO.md [DONE]
### 2. ✅ Test Local Run [DONE - Dependencies installed with fixes; app ready]


### 2. Test Local Run
```
streamlit run app.py
```
- Verify app loads model from `./model/`.
- Test prediction.
- Stop with Ctrl+C.

### 3. Prepare GitHub Repo
```
git add .
git commit -m "Prepare for Streamlit Cloud deploy"
git push origin main
```
- Repo must be **PUBLIC** for free Streamlit Cloud.
- If private/new: Make public or fork to public.

### 4. Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in (GitHub).
3. "New app" → Select GitHub repo/account → `crop-yield-app`.
4. Set "Branch": main, "Main file path": `app.py`, "Advanced": confirm requirements.txt.
5. Deploy → App live at https://yourappname.streamlit.app

### 5. ✅ Verify & Share [PENDING]
- Check model loads (no Databricks dep).
- Update README if needed post-deploy.

### 6. Optional Polish (Post-Deploy)
- Add `.streamlit/config.toml`.
- Update deps/README.

**Current Status: Ready for local test → GitHub → Deploy**

