# OnePlus 13 Update Watcher 🔔

This Python script tracks OxygenOS update announcements for OnePlus 13/13R posted by Winkey W. on the OnePlus Community forum. It runs daily via GitHub Actions and sends an email alert when a new post is detected.

## Features
- Extracts official update threads for OnePlus 13/13R
- Sends notification emails when new posts are found
- Automatically tracks the last seen update
- Runs daily using GitHub Actions [ToDo]

## How to Use

# Email notification settings, make a .env file in repo root
# to get app password go to https://myaccount.google.com/apppasswords
# 🛡️ How to Get a Gmail App Password
# Go to: https://myaccount.google.com/apppasswords
# Enable 2-Step Verification if not already enabled
# Generate a new App Password for “Mail” → “Other”
# Paste that password into .env under APP_PASSWORD

# contents of .env file below

YOUR_EMAIL=your_email@gmail.com
APP_PASSWORD=your_app_password
TO_EMAIL=your_email@gmail.com

### 🔧 Setup (locally)
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python fetch_updates.py
