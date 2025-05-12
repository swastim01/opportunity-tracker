# email_utils.py
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email_alert(to_email, program_name, predicted_date, top_links):
    try:
        subject = f"🔔 Opportunity Alert: {program_name}"
        body = f"""
Hi there,

Here's what we found for your program search: **{program_name}**

📅 Predicted Deadline: {predicted_date}

🔗 Top Links:
{chr(10).join(top_links)}

Check it out and don’t miss the deadline!

– Opportunity Tracker Bot
"""

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
