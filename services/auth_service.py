import hashlib
import services.database_service as database_service

def login(username, password):

    user = database_service.get_user(username)

    if user is None:
        return False

    entered_password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    if entered_password_hash == user["password_hash"]:
        # Find the user...

      return {
        "id": user["id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "email": user["email"]
    }
      return None





    
   # return entered_password_hash == user["password_hash"]