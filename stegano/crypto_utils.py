# Fonctions de chiffrement/déchiffrement avec mot de passe
# stegano/crypto_utils.py

import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes = b'stegano_salt') -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashlib.sha256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt(data: bytes, password: str) -> bytes:
    key = derive_key(password)
    f = Fernet(key)
    return f.encrypt(data)

def decrypt(token: bytes, password: str) -> bytes:
    key = derive_key(password)
    f = Fernet(key)
    return f.decrypt(token)
