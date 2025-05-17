from validate import login_to_account_valid
def login_to_account(username: str, password: str):
    valid = login_to_account_valid(username, password)
    return valid
