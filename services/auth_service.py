def login(username, password):

    VALID_USERNAME = "admin"
    VALID_PASSWORD = "1234"

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return True

    return False