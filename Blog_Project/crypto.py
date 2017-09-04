import hashlib
import hmac
import random
import string

SECRET_KEY = 'my_kitten_is_a_russian_spy'

def create_hash(mesg):
    return hmac.new(SECRET_KEY, mesg, hashlib.sha256).hexdigest()

def secure_mesg(mesg):
    return '{0}|{1}'.format(mesg, create_hash(mesg))

def validate(hmesg):
    msg = hmesg.split('|')[0]
    if (hmesg == secure_mesg(msg)):
        return msg
    return

def create_salt(length):
    return ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(max(1, length))])

def hash_password(uname, passw, salt=''):
    if not salt:
        salt = create_salt(16)
    hashed = hashlib.sha256(''.join((uname, passw, salt))).hexdigest()
    return (hashed, salt)

def verify_password(uname, passw, salt, hashed):
    if not (salt and hashed): return False
    return bool(hashed == hash_password(uname, passw, salt)[0])
