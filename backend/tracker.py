import gspread
from oauth2client.service_account import ServiceAccountCredentials

import requests
from bs4 import BeautifulSoup
import dateparser
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("CSE_ID")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# 🔍 Google Search
def google_search(query, num_results=5):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CSE_ID}&num={num_results}"
    response = requests.get(url)
    results = response.json()
    links = [item['link'] for item in results.get('items', [])]
    return links

# 🧠 Extract dates
def extract_dates_from_url(url):
    try:
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        dates = re.findall(r"\b(?:\d{1,2}[\s/-])?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s/-]?\d{2,4}\b", text, re.IGNORECASE)
        parsed = [dateparser.parse(d) for d in dates]
        return [d for d in parsed if d]
    except:
        return []

# 📅 Predict deadline
def predict_deadline(dates):
    if not dates:
        return "Unknown"
    months = [d.month for d in dates if d.year < datetime.now().year + 1]
    if not months:
        return "Unknown"
    most_common_month = max(set(months), key=months.count)
    predicted = datetime(datetime.now().year + 1, most_common_month, 15)
    return predicted.strftime("%Y-%m-%d")

# 🏷️ Auto-label type
def infer_type(program_name):
    name = program_name.lower()
    if any(k in name for k in ["scholar", "bursary", "grant"]):
        return "Scholarship"
    if "intern" in name or "fellow" in name:
        return "Internship"
    if "hack" in name:
        return "Hackathon"
    if "award" in name or "recognition" in name:
        return "Award"
    return "Other"

# 📧 Send email
def send_email(to_email, program, predicted, links):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📌 Opportunity: {program}"
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        html = f"""
        <html>
          <body>
            <h2>🔍 {program}</h2>
            <p><strong>Predicted Deadline:</strong> {predicted}</p>
            <p><strong>Top Links:</strong></p>
            <ul>
              {''.join(f'<li><a href="{link}">{link}</a></li>' for link in links)}
            </ul>
            <p>Track more on the app. 🚀</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

    except Exception as e:
        print("❌ Email Error:", e)

# 🧠 Master function
def process_program(program_name, email):
    links = google_search(program_name)
    all_dates = []
    for url in links:
        all_dates.extend(extract_dates_from_url(url))

    predicted = predict_deadline(all_dates)
    program_type = infer_type(program_name)

    # 📝 Write to sheet
    write_to_google_sheet({
        "program": program_name,
        "predicted": predicted,
        "type": program_type,
        "links": links,
    })

    # 📧 Send user the summary
    send_email(email, program_name, predicted, links[:3])

    return {
        "program": program_name,
        "predicted": predicted,
        "type": program_type,
        "links": links[:3],
    }

# 📄 Google Sheet
def write_to_google_sheet(data):
    try:
        print("⏳ Checking for duplicates in Google Sheet...")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)

        sheet = client.open("opportunity-tracker").sheet1
        existing = sheet.col_values(1)  # Column A = program names

        if data.get("program") in existing:
            print("⚠️ Duplicate detected. Skipping write.")
            return

        sheet.append_row([
            data.get("program"),
            data.get("predicted"),
            data.get("type"),
            ", ".join(data.get("links", [])),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ])
        print("✅ Written to Google Sheet.")
    except Exception as e:
        print("❌ Error writing to sheet:", e)

