from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_create(password: str):
    return pwd_context.hash(password)


def verify_pass(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)
