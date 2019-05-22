import data_manager
import util


def name_in_use(username):
    usernames = data_manager.get_users()
    for user in usernames:
        if username == user['username']:
            return True
    return False


def email_in_use(email):
    emails = data_manager.get_emails()
    for adress in emails:
        if email == adress['email']:
            return True
    return False


def explain_errors(username, confirmed_password, email, forbidden_char):
    errors = {}
    if name_in_use(username) is True:
        errors.update({'name_error': 'Can\'t use that name!'})
    if email_in_use(email) is True:
        errors.update({'email_error': 'Can\'t use that e-mail!'})
    if confirmed_password is False:
        errors.update({'confirm_password_error': 'It\'s not the same'})
    if forbidden_char is True:
        errors.update({'character_error': 'Forbidden Character!'})
    return errors


def check_error(username, password, confirm_password, email):
    is_forbidden = forbidden_char(username=username, password=password, confirm_password=confirm_password, email=email)
    is_confirmed_password = util.check_password(password, confirm_password)
    errors = explain_errors(username=username, confirmed_password=is_confirmed_password, email=email, forbidden_char=is_forbidden)
    if len(errors.keys()) > 0:
        return errors
    return None


def forbidden_char(username, password='', confirm_password='', email=''):
    forbidden = ['<', '>', ';', '\'', '\"', '\\', '/']
    for char in username:
        if char in forbidden:
            return True
    for char in password:
        if char in forbidden:
            return True
    for char in confirm_password:
        if char in forbidden:
            return True
    for char in email:
        if char in forbidden:
            return True
    return False


def check_login(username, password):
    is_forbidden = forbidden_char(username)
    saved_password = data_manager.get_hash(username)
    try:
        is_valid = util.verify_password(password, saved_password['password'])
    except TypeError:
        return True
    name_check = name_in_use(username)
    if is_forbidden is False and name_check is True and is_valid is True:
        return False