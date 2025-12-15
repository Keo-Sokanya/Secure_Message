from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_DIR = os.path.join(BASE_DIR, "data/keys")
os.makedirs(KEY_DIR, exist_ok=True)

SENDER_PRIV = os.path.join(KEY_DIR, "sender_private.pem")
SENDER_PUB = os.path.join(KEY_DIR, "sender_public.pem")
RECEIVER_PRIV = os.path.join(KEY_DIR, "receiver_private.pem")
RECEIVER_PUB = os.path.join(KEY_DIR, "receiver_public.pem")

def generate_rsa_pair(private_file, public_file, role):
    key = RSA.generate(2048)
    with open(private_file, "wb") as f:
        f.write(key.export_key())
    with open(public_file, "wb") as f:
        f.write(key.publickey().export_key())
    print(f"[RSA] {role} RSA keys created.")

def ensure_rsa_keys():
    if not (os.path.exists(SENDER_PRIV) and os.path.exists(SENDER_PUB)):
        generate_rsa_pair(SENDER_PRIV, SENDER_PUB, "Sender")

    if not (os.path.exists(RECEIVER_PRIV) and os.path.exists(RECEIVER_PUB)):
        generate_rsa_pair(RECEIVER_PRIV, RECEIVER_PUB, "Receiver")

def load_key(path):
    with open(path, "rb") as f:
        return RSA.import_key(f.read())

def rsa_encrypt(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

def rsa_decrypt(data, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(data)
