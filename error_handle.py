import data_manager
import util


def is_error_occur(username, email, confirmed_password, forbidden_char):
    errors = ({'name_error': 'ok'}, {'email_error': 'ok'}, {'confirmed_password': 'ok'}, {'forbidden_char': 'ok'})
    if name_in_use(username) is True:
        errors[0]['name_error'] = 'Can\'t use that name!'
    if email_in_use(email) is True:
        errors[1]['email_error'] = 'Can\'t use that e-mail!'
    if confirmed_password is False:
        errors[2]['confirmed_password'] = 'It\'s not the same'
    if forbidden_char is True:
        errors[3]['forbidden_char'] = 'Forbidden Character!'

    return errors


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


def get_error_messages(errors):
    error_mssgs = []
    for error in errors:
        for key in error.keys():
            if error[key] != 'ok':
                error_mssgs.append((key, error[key]))
    return error_mssgs


def check_error(username, password, confirm_password, email):
    forbidden = forbidden_char(username=username, password=password, confirm_password=confirm_password, email=email)
    confirmed_password = util.check_password(password, confirm_password)
    errors = is_error_occur(username=username, confirmed_password=confirmed_password, email=email, forbidden_char=forbidden)
    error_messages = get_error_messages(errors)
    return error_messages


def forbidden_char(username, password, confirm_password, email):
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