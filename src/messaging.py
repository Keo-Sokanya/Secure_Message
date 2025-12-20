from aes_crypto import aes_encrypt, aes_decrypt
from utils import save_message, load_all_messages


def send_message(text, key, sender_label="Sender", is_exit=False):
    if is_exit:
        text = "EXIT"

    cipher = aes_encrypt(text, key) 
    package = {
        "sender": sender_label,
        "cipher": {
            "nonce": cipher["nonce"],      
            "ciphertext": cipher["ciphertext"]
        },
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
            "nonce": package["cipher"]["nonce"],  
            "ciphertext": package["cipher"]["ciphertext"],
            "hmac": package["hmac"]
        }, key)
    except ValueError:
        return None, last_index + 1

    if text == "EXIT":
        return (package["sender"], "EXIT"), last_index + 1

    return (package["sender"], text), last_index + 1
