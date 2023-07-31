import bcrypt
import secrets
import string
from cryptography.fernet import Fernet

def hash_and_salt(psw):
    psw = psw.encode('utf-8')
    hashed_psw = bcrypt.hashpw(psw, bcrypt.gensalt())
    return hashed_psw

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