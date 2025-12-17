from Crypto.Cipher import AES
import os
from hmac_utils import compute_hmac, verify_hmac

def generate_aes_key():
    return os.urandom(64) 

def aes_encrypt(plaintext, key):
    K_enc = key[:32]
    K_mac = key[32:]
    
    nonce = os.urandom(12)  
    cipher = AES.new(K_enc, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(plaintext.encode())
    mac = compute_hmac(nonce + ciphertext, K_mac)
    return {"nonce": nonce.hex(), "ciphertext": ciphertext.hex(), "hmac": mac}

def aes_decrypt(package, key):
    K_enc = key[:32]
    K_mac = key[32:]

    nonce = bytes.fromhex(package["nonce"])
    ciphertext = bytes.fromhex(package["ciphertext"])
    received_hmac = package.get("hmac", "")
   
    if not verify_hmac(nonce + ciphertext, received_hmac, K_mac):
        raise ValueError("HMAC verification failed! Message may be tampered.")

    cipher = AES.new(K_enc, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()
