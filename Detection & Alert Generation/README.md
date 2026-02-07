# Detection & Alert Generation — Quick Guide

Brief: this module provides a small GUI to pick honeyfiles to monitor and a file-watching service that triggers multi-channel alerts (popup, email, SMS, voice) when monitored files are accessed.

## Components
- Main GUI + watcher: [`monitor_files_GUI.py`](Ransomware Code Files/Detection & Alert Generation/monitor_files_GUI.py)  
  - Key symbol: [`FileEventHandler`](Ransomware Code Files/Detection & Alert Generation/monitor_files_GUI.py) — handles on_created/on_modified/on_deleted/on_moved and calls alerting.
  - Entry point: run this file to pick files and start monitoring.
- File picker: [`gui_honeyfile_picker.py`](Ransomware Code Files/Detection & Alert Generation/gui_honeyfile_picker.py)  
  - Key symbol: [`pick_files_to_monitor`](Ransomware Code Files/Detection & Alert Generation/gui_honeyfile_picker.py) — interactive file selector used by the GUI.
- Alerting routines: [`mailAlert.py`](Ransomware Code Files/Detection & Alert Generation/mailAlert.py)  
  - Key symbols: [`send_alert`](Ransomware Code Files/Detection & Alert Generation/mailAlert.py), [`alert_queue`](Ransomware Code Files/Detection & Alert Generation/mailAlert.py)  
  - Implements: popup queueing, email (SMTP), Twilio SMS and voice calls.
- Requirements: [`requirement.txt`](Ransomware Code Files/Detection & Alert Generation/requirement.txt)
- Note: the repository ignores sensitive env file: see `.gitignore` entry for `/Detection & Alert Generation/.env`.

## Quick setup

1. Ensure Python 3.8+ is installed.
2. From the module folder, install base deps:
   pip install -r "Ransomware Code Files/Detection & Alert Generation/requirement.txt"
3. Install additional packages required by alerts:
   pip install python-dotenv twilio certifi

4. Create a `.env` file in the same folder (this file is listed in `.gitignore`) with your credentials — DO NOT commit:
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - TWILIO_NUMBER
   - ALERT_TO_NUMBER
   - SENDER_EMAIL
   - RECEIVER_EMAIL
   - EMAIL_APP_PASSWORD

5. Run the GUI and start monitoring:
   python "Ransomware Code Files/Detection & Alert Generation/monitor_files_GUI.py"

## How it works (high level)
1. User selects honeyfiles using [`pick_files_to_monitor`](Ransomware Code Files/Detection & Alert Generation/gui_honeyfile_picker.py).  
2. [`monitor_files_GUI.py`](Ransomware Code Files/Detection & Alert Generation/monitor_files_GUI.py) schedules a Watchdog observer for folders containing those files and instantiates [`FileEventHandler`](Ransomware Code Files/Detection & Alert Generation/monitor_files_GUI.py).  
3. On relevant FS events, `FileEventHandler` calls [`send_alert`](Ransomware Code Files/Detection & Alert Generation/mailAlert.py).  
4. `send_alert` enqueues a popup via `alert_queue` and also attempts email/SMS/voice alerts using configured providers.

## Notes & troubleshooting
- The `.env` file is intentionally ignored (see `/Detection & Alert Generation/.env` in `.gitignore`).
- If email or Twilio calls fail, check credentials and network access (outbound SMTP/Twilio).
- For GUI popups to appear the script uses Tkinter; ensure a desktop session is available.
- If the watcher misses events, verify permissions for the watched folders and that Watchdog supports your OS.

## Files & symbols (fast links)
- [monitor_files_GUI.py](Ransomware Code Files/Detection & Alert Generation/monitor_files_GUI.py) — [`FileEventHandler`](Ransomware Code Files/Detection & Alert Generation/monitor_files_GUI.py)
- [gui_honeyfile_picker.py](Ransomware Code Files/Detection & Alert Generation/gui_honeyfile_picker.py) — [`pick_files_to_monitor`](Ransomware Code Files/Detection & Alert Generation/gui_honeyfile_picker.py)
- [mailAlert.py](Ransomware Code Files/Detection & Alert Generation/mailAlert.py) — [`send_alert`](Ransomware Code Files/Detection & Alert Generation/mailAlert.py), [`alert_queue`](Ransomware Code Files/Detection & Alert Generation/mailAlert.py)
- [requirement.txt](Ransomware Code Files/Detection & Alert Generation/requirement.txt)
- [.gitignore entry for .env](/Users/radhe/Desktop/Major Project/Crypto-Ransomware/.gitignore)

If you want, I can add a sample `.env.template` (no secrets) you can copy