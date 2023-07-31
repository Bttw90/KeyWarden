import bcrypt
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

def hash_and_salt(psw):
    psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_psw = bcrypt.hashpw(psw, salt)
    return hashed_psw, salt

def psw_check(psw, hashed_psw):
    psw = psw.encode('utf-8')
    if bcrypt.checkpw(psw, hashed_psw):
        print('It Matches!')
        return True
    else:
        print('It Does not Match.')
        return False

def generate_random_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def encrypt_psw(psw, key):
    fernet = Fernet(key)
    encrypted_psw = fernet.encrypt(psw.encode())
    return encrypted_psw

def decrypt_psw(encrypted_psw, key):
    fernet = Fernet(key)
    decrypted_psw = fernet.decrypt(encrypted_psw).decode()
    return decrypted_psw

def get_fernet_key(psw, salt):
    psw = psw.encode()
    # Create a key using PBKDF2 with SHA-256 as hashing function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(psw))
    return key