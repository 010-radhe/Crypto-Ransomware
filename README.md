...existing code...
# 🛡️ Detection & Alert Generation — Quick Start & Guide

A compact GUI + watcher that protects honeyfiles and triggers multi-channel alerts (desktop popup, email, SMS, voice) when a monitored file is accessed. Built for easy setup and safe secret handling.

## 🚀 What this module does
- Lets an operator pick honeyfiles to monitor via a simple GUI.
- Uses Watchdog to observe filesystem events for selected files/folders.
- On access/modify/move/delete events, enqueues a popup and sends email/SMS/voice alerts.
- Keeps credentials out of source control using a local `.env` file (already ignored by .gitignore).

## ⚙️ Quick setup (macOS)
1. Install Python 3.8+.
2. From the module folder:
   ```bash
   cd "Ransomware Code Files/Detection & Alert Generation"
   pip install -r requirement.txt
   pip install python-dotenv twilio certifi
   ```
3. Create credentials (see below) and run:
   ```bash
   python monitor_files_GUI.py
   ```

## 🔐 Environment variables — create & use safely
Purpose: keep secrets (Twilio, email) out of the repo. The repo already ignores /Detection & Alert Generation/.env.

- Create a `.env` (recommended) by copying the template:
  ```bash
  cp .env.template .env
  open .env    # or edit with your editor
  ```
- Or create from terminal:
  ```bash
  echo "TWILIO_ACCOUNT_SID=your_sid" > .env
  echo "TWILIO_AUTH_TOKEN=your_token" >> .env
  echo "TWILIO_NUMBER=+1234567890" >> .env
  echo "ALERT_TO_NUMBER=+1987654321" >> .env
  echo "SENDER_EMAIL=you@example.com" >> .env
  echo "RECEIVER_EMAIL=ops@example.com" >> .env
  echo "EMAIL_APP_PASSWORD=app_password" >> .env
  ```

.env.template (safe to commit)
```text
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_NUMBER=
ALERT_TO_NUMBER=
SENDER_EMAIL=
RECEIVER_EMAIL=
EMAIL_APP_PASSWORD=
```

## 🧩 Load env vars in Python
Install the loader:
```bash
pip install python-dotenv
```
Example usage:
```python
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)             # loads .env into os.environ

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
```

## 🖥️ Shell alternatives (macOS)
- Temporary for current shell:
  ```bash
  export TWILIO_ACCOUNT_SID="your_sid"
  echo $TWILIO_ACCOUNT_SID
  ```
- Persist (zsh):
  Add exports to `~/.zshrc` and run:
  ```bash
  source ~/.zshrc
  ```

## ⚠️ Security notes
- Never commit `.env` with real secrets. If secrets were committed, rotate them and remove from history.
- To stop tracking a committed .env:
  ```bash
  git rm --cached "Detection & Alert Generation/.env"
  git commit -m "Stop tracking .env"
  ```
- Ensure network access for SMTP/Twilio and desktop session for Tkinter popups.

## 🧪 Quick troubleshooting
- No popups: verify Tkinter availability and desktop session.
- Missing events: check folder permissions and Watchdog support for the platform.
- Alert failures: validate credentials and outbound network (SMTP/Twilio).

## 🔗 Where to look
- monitor_files_GUI.py — watcher + FileEventHandler (entrypoint)
- gui_honeyfile_picker.py — file picker helper
- mailAlert.py — alert queue + email/SMS/voice senders
- requirement.txt — dependencies

...existing
