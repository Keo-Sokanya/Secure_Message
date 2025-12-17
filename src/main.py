import os
import time
import threading
from rsa_crypto import ensure_rsa_keys, load_key, rsa_encrypt
from aes_crypto import generate_aes_key
from messaging import send_message, receive_message
from utils import load_all_messages


KEY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/keys")
AES_KEY_FILE = os.path.join(KEY_DIR, "session_aes.key")
RECEIVER_PUB_FILE = os.path.join(KEY_DIR, "receiver_public.pem")

ensure_rsa_keys()

if not os.path.exists(AES_KEY_FILE):
    master_key = generate_aes_key()
    receiver_pub = load_key(RECEIVER_PUB_FILE)
    encrypted_aes = rsa_encrypt(master_key, receiver_pub)

    with open(AES_KEY_FILE, "wb") as f:
        f.write(master_key)

    MY_ROLE = "User1"
    OTHER_ROLE = "User2"
    print("[AES] New session key created.")
else:
    with open(AES_KEY_FILE, "rb") as f:
        master_key = f.read()

    MY_ROLE = "User2"
    OTHER_ROLE = "User1"
    print("[AES] Joined existing session.")


messages = load_all_messages()
last_index = len(messages)
stop_threads = False

def listen_incoming():
    global last_index, stop_threads
    while not stop_threads:
        result, last_index = receive_message(master_key, last_index)
        if result:
            sender, text = result
            if text == "EXIT":
                print(f"{sender} has left the chat.")
                stop_threads = True
                break
            if sender != MY_ROLE:
                print(f"\n[Message received] {text}")
        time.sleep(0.2)

threading.Thread(target=listen_incoming, daemon=True).start()

try:
    while True:
        msg = input(f"[{MY_ROLE}]: ").strip()
        if not msg:
            continue
        if msg.lower() == "/exit":
            send_message("", master_key, sender_label=MY_ROLE, is_exit=True)
            print("\n[Chat ended]")
            stop_threads = True
            if os.path.exists(AES_KEY_FILE):
                os.remove(AES_KEY_FILE)
            break
        send_message(msg, master_key, sender_label=MY_ROLE)

except KeyboardInterrupt:
    send_message("", master_key, sender_label=MY_ROLE, is_exit=True)
    stop_threads = True
    print("\n[Chat ended]")
    if os.path.exists(AES_KEY_FILE):
        os.remove(AES_KEY_FILE)
