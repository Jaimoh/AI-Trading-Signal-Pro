import hashlib
import services.database_service as database_service

def login(username, password):

    user = database_service.get_user(username)

    if user is None:
        return False

    entered_password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    return entered_password_hash == user["password_hash"]