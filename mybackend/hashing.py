import bcrypt

def hash_password(password: str) -> str:
    # 1. Convert the plain text string into bytes
    password_bytes = password.encode('utf-8')
    
    # 2. Generate a secure random salt
    salt = bcrypt.gensalt()
    
    # 3. Hash the password and convert the resulting bytes back into a readable string
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_password_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert both strings into bytes so bcrypt can safely compare them
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Securely compare them (prevents timing attacks)
    return bcrypt.checkpw(plain_bytes, hashed_bytes)