def check_user(userData, creds):
    for user in userData:
        if user["username"] == creds["username"] and user["password"] == creds["password"]:
            return True
    return False