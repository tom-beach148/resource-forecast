# Finance & Resourcing Forecast App (Collaborative)

A collaborative web application for forecasting costs and margins. Data is stored in Google Sheets so your team can work together in real-time.

---

## What You'll Set Up

1. A Google Sheet to store your data
2. A Google Cloud "service account" (like a robot user that lets your app access the sheet)
3. The app itself, deployed online

**Time needed:** About 20-30 minutes for first-time setup.

---

## Part 1: Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Click **+ Blank** to create a new spreadsheet
3. Name it exactly: `Resource Forecast` (click "Untitled spreadsheet" at the top left)
4. In the first row, add these column headers (one per cell, A through G):

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Name | Business Unit | Start Date | End Date | Number of Days | Per Diem | Cost Rate |

5. **Important:** Keep this tab open — you'll need the sheet URL later.

---

## Part 2: Set Up Google Cloud (One Time Only)

This creates a "service account" — think of it as a robot assistant that lets your app read and write to your Google Sheet.

### Step 2.1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. If prompted, sign in with your Google account
3. At the top of the page, click on the project dropdown (might say "Select a project")
4. Click **New Project** in the popup window
5. Enter a name like `Resource Forecast App`
6. Click **Create**
7. Wait a few seconds, then make sure your new project is selected in the dropdown

### Step 2.2: Enable the Google Sheets API

1. In the search bar at the top, type `Google Sheets API`
2. Click on **Google Sheets API** in the results
3. Click the blue **Enable** button
4. Wait for it to enable (a few seconds)

### Step 2.3: Enable the Google Drive API

1. In the search bar at the top, type `Google Drive API`
2. Click on **Google Drive API** in the results
3. Click the blue **Enable** button

### Step 2.4: Create a Service Account

1. In the search bar, type `Service Accounts`
2. Click on **Service Accounts** (under IAM & Admin)
3. Click **+ Create Service Account** at the top
4. Fill in:
   - **Service account name:** `resource-forecast-app`
   - **Service account ID:** (auto-fills)
5. Click **Create and Continue**
6. Click **Continue** (skip the optional permissions)
7. Click **Done**

### Step 2.5: Create and Download the Key

1. You should see your new service account in the list. Click on it.
2. Click the **Keys** tab at the top
3. Click **Add Key** → **Create new key**
4. Select **JSON** and click **Create**
5. A file will download — this is your `credentials.json` file. **Keep this safe!**

### Step 2.6: Share Your Sheet with the Service Account

1. Open the `credentials.json` file you just downloaded in Notepad
2. Find the line that says `"client_email":` — it will look something like:
   ```
   "client_email": "resource-forecast-app@your-project-123.iam.gserviceaccount.com"
   ```
3. Copy that email address (just the part in quotes)
4. Go back to your Google Sheet
5. Click **Share** (top right)
6. Paste the service account email
7. Make sure it says **Editor**
8. Uncheck "Notify people"
9. Click **Share**

---

## Part 3: Test Locally (Optional but Recommended)

Before deploying online, you can test on your computer:

1. Put the `credentials.json` file in your `finance-forecast-collab` folder
2. Open Command Prompt, navigate to the folder:
   ```
   cd C:\Users\YourName\Downloads\finance-forecast-collab
   ```
3. Create and activate the virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the app:
   ```
   python app.py
   ```
6. Open `http://localhost:5000` in your browser

If it works, you'll see the app connected to your Google Sheet!

---

## Part 4: Deploy Online (Render)

### Step 4.1: Push to GitHub

1. Create a GitHub account if you don't have one: [github.com](https://github.com)
2. Click the **+** in the top right → **New repository**
3. Name it `resource-forecast`
4. Keep it **Public** (or Private if you prefer)
5. Click **Create repository**
6. Follow GitHub's instructions to upload your files, OR:
   - Download [GitHub Desktop](https://desktop.github.com) (easier for beginners)
   - Clone your new repo
   - Copy your app files into the folder
   - Commit and push

**Important:** Do NOT upload your `credentials.json` file to GitHub — we'll add it securely in Render.

### Step 4.2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New +** → **Web Service**
3. Connect your GitHub account and select your `resource-forecast` repository
4. Configure:
   - **Name:** `resource-forecast` (or anything you like)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

5. Scroll down to **Environment Variables** and add these two:

   | Key | Value |
   |-----|-------|
   | `SHEET_NAME` | `Resource Forecast` |
   | `GOOGLE_CREDENTIALS` | (see below) |

6. For `GOOGLE_CREDENTIALS`:
   - Open your `credentials.json` file in Notepad
   - Select all (Ctrl+A) and copy (Ctrl+C)
   - Paste the entire contents as the value

7. Click **Create Web Service**
8. Wait 2-3 minutes for deployment

### Step 4.3: You're Live!

Render will give you a URL like `https://resource-forecast.onrender.com`

Share this URL with your team — everyone can now:
- Add, edit, and delete associates
- See changes update within 3 seconds
- Also edit directly in the Google Sheet if preferred

---

## How It Works

- All data is stored in your Google Sheet
- The app checks for updates every 3 seconds
- When anyone makes a change, everyone sees it shortly after
- You can also open the Google Sheet directly to view or edit data

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Failed to connect to Google Sheets" | Check that you shared the sheet with the service account email |
| App won't start on Render | Check the `GOOGLE_CREDENTIALS` environment variable is the full JSON contents |
| Changes not appearing | Wait a few seconds and click the refresh button |
| "No credentials found" | Make sure `credentials.json` is in the folder (local) or the environment variable is set (Render) |

---

## File Structure

```
finance-forecast-collab/
├── app.py              # Flask application with Google Sheets API
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── credentials.json   # Your Google credentials (local only, don't upload!)
├── templates/
│   └── index.html     # React frontend
└── README.md          # This file
```

---

## Security Notes

- Never share your `credentials.json` file publicly
- Never commit it to GitHub
- The service account can only access sheets you explicitly share with it
- On Render, credentials are stored as encrypted environment variables
