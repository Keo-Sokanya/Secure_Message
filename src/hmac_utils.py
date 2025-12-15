import hmac
import hashlib
import base64

def compute_hmac(data, key):
    h = hmac.new(key, data, hashlib.sha256)
    return base64.b64encode(h.digest()).decode()

def verify_hmac(data, received_hmac, key):
    expected = compute_hmac(data, key)
    return hmac.compare_digest(expected, received_hmac)
