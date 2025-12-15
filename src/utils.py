import os
import json
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESSAGE_DIR = os.path.join(BASE_DIR, "data/messages")
os.makedirs(MESSAGE_DIR, exist_ok=True)

MESSAGE_FILE = os.path.join(MESSAGE_DIR, "message.json")

def load_all_messages():
    if not os.path.exists(MESSAGE_FILE):
        return []
    with open(MESSAGE_FILE, "r") as f:
        return json.load(f)

def save_message(package):
    messages = load_all_messages()
    messages.append(package)
    with open(MESSAGE_FILE, "w") as f:
        json.dump(messages, f, indent=4)
