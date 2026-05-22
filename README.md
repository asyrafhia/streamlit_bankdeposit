# Streamlit Bank Term Deposit Predictor

This workspace contains a Streamlit app that loads the saved encoder and CatBoost model from `models/` and predicts whether a new customer will subscribe to a term deposit.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Notes

- The app uses the 13-column inference schema from `Test_Deployed_Models.ipynb`.
- It does not retrain the model.
- Threshold is adjustable from the sidebar.

## Packaging & Sharing

See `DEPLOY_GUIDE.md` for step-by-step instructions to package this project, upload to Google Drive, push code to GitHub, and run the app on another machine.

If `models/` is not included in the GitHub repo, download `streamlitml.zip` from the shared Drive link, extract it so that the `models/` folder is at the project root, then run the app locally.