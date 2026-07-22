from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hash(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password cannot be longer than 72 bytes")

    return context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    if len(password.encode("utf-8")) > 72:
        return False

    return context.verify(password, hash)
