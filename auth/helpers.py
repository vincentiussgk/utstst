from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==== Password Hashing ====

# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Verify inputted pasword
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Check if user exists
def check_user(userData, creds):
    for user in userData:
        if verify_password(creds["password"], user["password"]) and user["username"] == creds["username"]:
            return True
    return False