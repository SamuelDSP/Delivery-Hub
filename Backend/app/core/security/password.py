from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hash(password: str) -> str:
    return context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return context.verify(password, hash)