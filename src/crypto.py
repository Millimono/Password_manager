from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def generate_salt():
    return os.urandom(32)

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_data(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv + encryptor.tag + encrypted_data

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]
    tag = encrypted_data[16:32]
    data = encrypted_data[32:]
    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

def generate_password(length=16, use_symbols=True):
    import random
    import string
    
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    return ''.join(random.choice(chars) for _ in range(length))
