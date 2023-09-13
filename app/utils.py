from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#to hash the password when creating a user
def hash(password: str):
    return pwd_context.hash(password)

#to convert the plain password to hash and compair it to hashed password using the verify function.
#this is during the login
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)