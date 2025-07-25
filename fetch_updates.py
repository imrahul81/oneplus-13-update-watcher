import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Constants
PROFILE_URL = "https://community.oneplus.com/user/1099451129328566328"
LAST_SEEN_FILE = "last_seen.json"
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# Load last seen post from file
def load_last_seen():
    if not os.path.exists(LAST_SEEN_FILE):
        return None
    try:
        with open(LAST_SEEN_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return None
            return json.loads(content)
    except json.JSONDecodeError:
        return None

# Save new post as last seen
def save_last_seen(post):
    with open(LAST_SEEN_FILE, "w") as f:
        json.dump(post, f)

# Send email alert
def send_email(subject, body, html_body=None):
    if html_body:
        msg = MIMEMultipart("alternative")
        part1 = MIMEText(body, "plain")
        part2 = MIMEText(html_body, "html")
        msg.attach(part1)
        msg.attach(part2)
    else:
        msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = YOUR_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# Fetch latest posts by Winkey W.
def fetch_posts():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(PROFILE_URL)
    time.sleep(5)

    links = driver.find_elements(By.TAG_NAME, "a")
    posts = []

    for link in links:
        title = link.text.strip()
        href = link.get_attribute("href")
        if title and "OnePlus 13" in title and "OxygenOS" in title:
            posts.append({
                "title": title,
                "link": href
            })
    driver.quit()
    return posts

# Main logic
def main():
    posts = fetch_posts()
    if not posts:
        print("No posts found.")
        return

    latest = posts[0]
    last_seen = load_last_seen()

    if not last_seen or latest["link"] != last_seen.get("link"):
        print(f"🚨 New post detected:\n{latest['title']}\n{latest['link']}")
        html_body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f9f9f9;
                    color: #222;
                    padding: 20px;
                }}
                .container {{
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    padding: 24px;
                    max-width: 600px;
                    margin: auto;
                }}
                h2 {{
                    color: #d32f2f;
                }}
                a.button {{
                    display: inline-block;
                    padding: 10px 18px;
                    background: #1976d2;
                    color: #fff !important;
                    border-radius: 4px;
                    text-decoration: none;
                    margin-top: 16px;
                }}
                .meta {{
                    color: #555;
                    font-size: 0.95em;
                    margin-bottom: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🚨 New OnePlus 13 Update</h2>
                <div class="meta"><strong>Title:</strong> {latest['title']}</div>
                <a href="{latest['link']}" class="button">Read the post</a>
            </div>
        </body>
        </html>
        """
        send_email(
            subject=f"[OnePlus 13 Update] {latest['title']}",
            body=f"A new update was posted by Winkey W.:\n\n{latest['title']}\n\n{latest['link']}",
            html_body=html_body
        )
        save_last_seen(latest)
    else:
        print("✅ No new post yet.")

if __name__ == "__main__":
    main()
# This script fetches the latest posts from a specific OnePlus community profile
# and sends an email alert if a new post is detected. It uses Selenium for web scraping
# and Gmail's SMTP for sending emails. Make sure to replace YOUR_EMAIL and APP_PASSWORD
# with your actual email and app password. The script checks for posts related to
# "OnePlus 13" and "OxygenOS" and saves the last seen post to avoid duplicate alerts.
# Run this script periodically (e.g., using a cron job) to keep track of updates.
# Ensure you have the necessary permissions and comply with the website's terms of service
# when scraping content. You may need to install the required packages using pip:
# pip install selenium
# Also, ensure you have the Chrome WebDriver installed and available in your PATH.
# You can set up a cron job to run this script periodically, e.g., every hour:
# 0 * * * * /usr/bin/python3 /path/to/fetch_updates.py