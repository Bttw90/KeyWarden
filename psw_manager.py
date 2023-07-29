import bcrypt

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
