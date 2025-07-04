# OnePlus 13 Update Watcher 🔔

This Python script tracks OxygenOS update announcements for OnePlus 13/13R posted by Winkey W. on the OnePlus Community forum. It runs daily via GitHub Actions and sends an email alert when a new post is detected.

## Features
- Extracts official update threads for OnePlus 13/13R
- Sends notification emails when new posts are found
- Automatically tracks the last seen update
- Runs daily using GitHub Actions

## How to Use

### 🔧 Setup (locally)
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python fetch_updates.py
