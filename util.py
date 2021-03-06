from datetime import datetime
from flask import session
import data_manager
import bcrypt


def get_user_id_session():
    if session:
        user_id = data_manager.get_user_id(session['username'])
        return user_id['id']
    return 0


def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def hash_pass(password):
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass.decode('utf-8')


def verify_password(password, hashed_pass):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pass.encode('utf-8'))


def check_password(password, confirm_password):
    if password == confirm_password:
        return True
    return False



