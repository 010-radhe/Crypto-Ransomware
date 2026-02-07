import socket
import requests
import certifi
import smtplib
import ssl
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import queue

# Load .env from project tree
load_dotenv(find_dotenv())

alert_queue = queue.Queue()

# Twilio Credentials (loaded from environment)
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
to_number = os.getenv("ALERT_TO_NUMBER")

# Email Credentials (loaded from environment)
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
email_password = os.getenv("EMAIL_APP_PASSWORD")  # Use App Password

# Optional: warn if required credentials are missing
_missing = [k for k,v in {
    "TWILIO_ACCOUNT_SID": account_sid,
    "TWILIO_AUTH_TOKEN": auth_token,
    "TWILIO_NUMBER": twilio_number,
    "ALERT_TO_NUMBER": to_number,
    "SENDER_EMAIL": sender_email,
    "RECEIVER_EMAIL": receiver_email,
    "EMAIL_APP_PASSWORD": email_password
}.items() if not v]
if _missing:
    print(f"⚠️ Missing environment variables: {', '.join(_missing)}")


ssl_context = ssl.create_default_context(cafile=certifi.where())

def get_network_info():
    """
    Retrieves public IP, private IP, and hostname of the system.
    """
    try:
        public_ip = requests.get("https://api64.ipify.org").text
        local_ip = socket.gethostbyname(socket.gethostname())
        hostname = socket.gethostname()
        return public_ip, local_ip, hostname
    except Exception:
        return "Unavailable", "Unavailable", "Unavailable"

def get_alert_message(file, access_type):
    """
    Constructs the alert message with system and file information.
    """
    public_ip, private_ip, hostname = get_network_info()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alert_message = (
        f"🚨 Security Alert Isolate this PC Urgently to avoid other pc Distruction🚨\n"
        f"File Compromised: '{file}'\n"
        f"Access Type: {access_type}\n"
        f"📅 Date & Time: {now}\n"
        f"🌐 Public IP: {public_ip}\n"
        f"🏠 Private IP: {private_ip}\n"
        f"🖥 Hostname: {hostname}\n"
        f"\n⚠️ Urgently communicate with the IT Security team!\n"
        
    )
    return alert_message

def send_email_alert(alert_message):
    """
    Sends an Email alert with detailed security information.
    """
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "🚨 Security Alert: File Accessed! 🚨"
        message.attach(MIMEText(alert_message, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")

def send_sms_alert(alert_message):
    """
    Sends an SMS alert using Twilio.
    """
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="File Accessed",
            from_=twilio_number,
            to=to_number
        )
        print(f"✅ SMS sent successfully! Message SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")

def send_voice_alert(alert_message):
    """
    Sends a voice call with a short alert message using Twilio.
    """
    try:
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            to=to_number,
            from_=twilio_number,
            twiml=f'<Response><Say voice="alice">{alert_message}</Say></Response>'
        )
        print(f"✅ Voice call initiated! Call SID: {call.sid}")
    except Exception as e:
        print(f"❌ Error making voice call: {str(e)}")

def show_popup_alert(alert_message):
    """
    Displays a popup alert using tkinter.
    """
    try:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        messagebox.showwarning("🚨 Security Alert 🚨", alert_message)
        root.destroy()
    except Exception as e:
        print(f"❌ Error showing popup alert: {str(e)}")


def send_alert(file, access_type):
    alert_message = get_alert_message(file, access_type)

    # Put alert message in the queue (for popup to pick)
    alert_queue.put(alert_message)

    # Other alerts can run in background threads
    send_email_alert(alert_message)
    send_sms_alert(alert_message)
    send_voice_alert(alert_message)

'''
def send_alert(file, access_type):
    """
    Main function: triggers all alerts (Popup, Email, SMS, Voice) with the alert message.
    """
    alert_message = get_alert_message(file, access_type)

    show_popup_alert(alert_message)
    send_email_alert(alert_message)
    send_sms_alert(alert_message)
    send_voice_alert("Alert! A critical file has been accessed. Please check immediately.")  # Shorter message for voice

'''
