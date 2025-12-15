from aes_crypto import aes_encrypt, aes_decrypt
from utils import save_message, load_all_messages
import time


def send_message(text, key, sender_label="Sender", is_exit=False):
    if is_exit:
        text = "__EXIT__"

    cipher = aes_encrypt(text, key)
    package = {
        "sender": sender_label,
        "cipher": {"iv": cipher["iv"], "ciphertext": cipher["ciphertext"]},
        "hmac": cipher["hmac"],
        "is_exit": is_exit
    }

    save_message(package)


def receive_message(key, last_index):
    messages = load_all_messages()
    if last_index >= len(messages):
        return None, last_index
    
    package = messages[last_index]
    try:
        text = aes_decrypt({
            "iv": package["cipher"]["iv"],
            "ciphertext": package["cipher"]["ciphertext"],
            "hmac": package["hmac"]
        }, key)
    except ValueError:
        print(f"[Warning] Message integrity failed for message {last_index}!")
        return None, last_index + 1

    if text == "__EXIT__":
        return (package["sender"], "__EXIT__"), last_index + 1

    return (package["sender"], text), last_index + 1
