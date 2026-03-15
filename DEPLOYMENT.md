# Streamlit Cloud Deployment Guide

## Complete Step-by-Step Deployment Instructions

### Prerequisites
- GitHub account
- Streamlit account (use the same email as GitHub)
- Your project files ready

---

## Part 1: Prepare for Deployment

### 1. Create a `.gitignore` file ✓ (Already created)
Make sure large files and sensitive data are not committed:
- `__pycache__/`
- `.streamlit/secrets.toml`
- `venv/`

### 2. Create `requirements.txt` ✓ (Already created)
This file lists all Python dependencies:
```
streamlit==1.28.0
pandas==2.1.1
```

### 3. Organize your project structure ✓ (Already done)
```
Mirchi/
├── app.py
├── utils.py
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
└── README.md
```

---

## Part 2: Set Up GitHub Repository

### Step 1: Initialize Git

Open PowerShell in your project directory:

```powershell
cd d:\Mirchi
git init
git config user.name "Your Name"
git config user.email "your.email@gmail.com"
```

### Step 2: Add and Commit Files

```powershell
git add .
git commit -m "Initial commit: Chilly Yard Manager application"
```

### Step 3: Create Repository on GitHub

1. Go to [github.com](https://github.com)
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `Mirchi` or `chilly-yard-manager`
4. Description: "Chilly Yard Business Management Application"
5. Choose **Public** (required for free Streamlit Cloud)
6. Do NOT initialize with README (we already have one)
7. Click **Create repository**

### Step 4: Push to GitHub

Copy the commands from GitHub and run in PowerShell:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Mirchi.git
git push -u origin main
```

You'll be prompted to authenticate. Use:
- Username: Your GitHub username
- Password: Your GitHub personal access token

**To create a Personal Access Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `gist`
4. Copy the token and use it as password

---

## Part 3: Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud

1. Open [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub (if not already)

### Step 2: Create New App

1. Click **New app** button
2. Fill in the deployment details:
   - **Repository**: `YOUR_USERNAME/Mirchi`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **Deploy!**

### Step 3: Wait for Deployment

- Streamlit will build the app automatically
- Takes 2-5 minutes typically
- You'll see logs showing the build progress
- Once complete, your app URL will be displayed

### Step 4: Share Your App

Your app will be accessible at:
```
https://your-username-mirchi.streamlit.app
```

Or a custom URL if you configure it in Streamlit settings.

---

## Part 4: Update Your App After Deployment

### To update the app:

1. Make changes locally
2. Commit and push to GitHub:
```powershell
git add .
git commit -m "Update features"
git push origin main
```

3. Streamlit Cloud automatically detects changes
4. App redeploys automatically within a few minutes

---

## Part 5: Data Management in Streamlit Cloud

⚠️ **Important:** Streamlit Cloud has ephemeral storage. This means:

- **Data in `data/` folder will NOT persist** across redeploys
- The `data/` folder is recreated fresh on each deployment

### Solutions:

#### Option 1: Use Streamlit Secrets (Recommended for Production)
1. In Streamlit Cloud app settings
2. Add a "Secrets" section
3. Store connection strings for databases

#### Option 2: Add Database Integration
Consider adding:
- **Supabase** (PostgreSQL cloud)
- **Firebase** (NoSQL cloud)
- **AWS S3** (for JSON files)

#### Option 3: Keep Local Deployment
Keep the app running on your local machine or a local server where data persists.

---

## Troubleshooting

### "requirements.txt not found"
- Make sure `requirements.txt` is in the root directory
- Commit and push the file to GitHub

### App crashes on Streamlit Cloud
- Check the logs on Streamlit Cloud dashboard
- Common issues:
  - Missing dependencies in `requirements.txt`
  - File path issues (use relative paths)
  - Library version incompatibilities

### Data not persisting
- This is expected on Streamlit Cloud (ephemeral storage)
- Consider implementing database integration

### Permission denied on GitHub push
- Generate a new Personal Access Token
- Use token as password when prompted

---

## Optional: Enhanced Deployment

### Add Environment Variables
Store sensitive information securely:

1. In Streamlit Cloud app settings → Secrets
2. Add your variables:
```toml
[database]
url = "your-database-url"

[api]
key = "your-api-key"
```

### Alternative: Database Integration

If you want persistent data in cloud:

**Add to your project:**

```bash
pip install supabase
```

Then modify `app.py` to use Supabase instead of JSON files.

---

## Success Checklist

- ✅ GitHub repository created
- ✅ Project pushed to GitHub
- ✅ Streamlit Cloud deployment created
- ✅ App accessible via URL
- ✅ Data loading correctly
- ✅ All features working

---

## Support Contacts

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **GitHub Help**: https://docs.github.com

---

**Your Chilly Yard Manager is now live! 🌶️🎉**
