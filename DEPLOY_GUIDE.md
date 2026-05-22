# Deployment & Sharing Guide

This guide explains the simplest ways to share and run this Streamlit app on another machine (e.g., your brother's). Follow the numbered steps in order.

## 1 — Create a zip for sharing (you can skip if already provided)
- On Windows PowerShell (in project root):
  ```powershell
  Compress-Archive -Path .\* -DestinationPath .\streamlitml.zip -Force
  ```
- Alternatively use 7-Zip or any archive tool.

## 2 — Upload to Google Drive
1. Open https://drive.google.com
2. Click New → File upload → select `streamlitml.zip`
3. After upload, right-click the file → Get link → set to "Anyone with the link" (or restrict as desired) → Copy link
4. Share that link with the person who will run the app

## 3 — Recommended: push code to GitHub (without models)
Why: models can be large; easiest workflow is to keep `models/` out of the repo and share `streamlitml.zip` separately.

1. Create `.gitignore` (already present) that excludes `models/` and `venv/`.
2. Create a new empty repo on GitHub (do not add a README via web UI).
3. From project root, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPO.git
   git push -u origin main
   ```

Note: If you want to include models in the repo and any model file is larger than 100 MB, use Git LFS — see https://git-lfs.github.com/ (more advanced).

## 4 — Simple local run instructions (for the person receiving the zip)
1. Extract `streamlitml.zip` so the folder structure contains `streamlit_app.py`, `requirements.txt`, and a `models/` folder with `ohe.pkl` and `cbc_optuna.pkl`.
2. Open PowerShell in the extracted folder.
3. Run the following commands:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
4. Open a browser to `http://localhost:8501`.

## 5 — Optional: Deploy to Streamlit Cloud (requires models in repo)
1. Push repo to GitHub including `models/` (only if model files are small enough).
2. Sign in at https://share.streamlit.io with GitHub account.
3. Click "New app", select the repo, branch `main`, and file `streamlit_app.py`, then click Deploy.

## 6 — Troubleshooting
- If `pip install -r requirements.txt` fails due to permissions, run with `--user` or ensure Python environment is writable.
- If `streamlit run` fails with missing artifacts, confirm `models/ohe.pkl` and `models/cbc_optuna.pkl` exist at project root.
- If scripts like `streamlit` are not on PATH after venv activation, run them via `python -m streamlit run streamlit_app.py`.

---

If you want, I can create the zip here and provide it for upload, or I can push the code-only repo to GitHub (you must provide the target repo URL or authorize via `gh` CLI). Which would you like me to do next?
