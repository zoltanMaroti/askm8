import data_manager


def check_if_error()

def name_in_use(username):
    usernames = data_manager.get_users()
    for user in usernames:
        if username == user['username']:
            return True
    return False

