import time
import queue
import os
import psutil
import tkinter as tk
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from mailAlert import send_alert
from gui_honeyfile_picker import pick_files_to_monitor

import threading
import mailAlert  # For alert_queue access

# === Pick files from GUI ===
monitored_files = pick_files_to_monitor()

# === Tkinter root (for alerts) ===
tk_root = tk.Tk()
tk_root.withdraw()

def process_alert_queue():
    try:
        while True:
            alert_msg = mailAlert.alert_queue.get_nowait()
            messagebox.showwarning("🚨 Security Alert 🚨", alert_msg)
    except queue.Empty:
        pass
    tk_root.after(1000, process_alert_queue)  # Keep checking every second

class FileEventHandler(FileSystemEventHandler):
    def get_process_info(self):
        process_info = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                process_info.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return process_info

    def log_event(self, event_type, event):
        process_info = self.get_process_info()
        print(f"{event_type} event: {event.src_path}")
        send_alert(event.src_path, event_type)

    def on_modified(self, event):
        if not event.is_directory and os.path.abspath(event.src_path) in monitored_files:
            self.log_event("Modified", event)

    def on_created(self, event):
        if not event.is_directory and os.path.abspath(event.src_path) in monitored_files:
            self.log_event("Created", event)

    def on_deleted(self, event):
        if not event.is_directory and os.path.abspath(event.src_path) in monitored_files:
            self.log_event("Deleted", event)

    def on_moved(self, event):
        if not event.is_directory:
            if (os.path.abspath(event.src_path) in monitored_files or
                os.path.abspath(event.dest_path) in monitored_files):
                self.log_event("Moved", event)

def start_monitoring():
    folders_to_watch = set(os.path.dirname(file) for file in monitored_files)
    event_handler = FileEventHandler()
    observer = Observer()

    for folder in folders_to_watch:
        observer.schedule(event_handler, folder, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# === Start monitoring in a separate thread
monitor_thread = threading.Thread(target=start_monitoring, daemon=True)
monitor_thread.start()

# === Start checking for alerts and run GUI loop
process_alert_queue()
tk_root.mainloop()
