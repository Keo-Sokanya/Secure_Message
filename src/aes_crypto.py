from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
from hmac_utils import compute_hmac, verify_hmac

def generate_aes_key():
    return os.urandom(64)

def aes_encrypt(plaintext, key):
    
    K_enc = key[:32]  
    K_mac = key[32:]  

    cipher = AES.new(K_enc, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))

    mac = compute_hmac(cipher.iv + ciphertext, K_mac)

    return {
        "iv": cipher.iv.hex(),
        "ciphertext": ciphertext.hex(),
        "hmac": mac
    }

def aes_decrypt(package, key):
    K_enc = key[:32]
    K_mac = key[32:]

    iv = bytes.fromhex(package["iv"])
    ciphertext = bytes.fromhex(package["ciphertext"])
    received_hmac = package.get("hmac", "")

    if not verify_hmac(iv + ciphertext, received_hmac, K_mac):
        raise ValueError("HMAC verification failed! Message may be tampered.")

    cipher = AES.new(K_enc, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()
