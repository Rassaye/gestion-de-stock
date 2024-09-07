from passlib.context import CryptContext
from jose import ExpiredSignatureError, jwt, JWTError

# Mise en place du bouton d'authentification
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
pwd_context = CryptContext(schemes=["bcrypt"])

#Used during the Signup operation
def hash_password(clear_password:str):
    return pwd_context.hash(clear_password)


# Used during the Login / Auth operation
def verify_password(given_password, hashed_password):
    return pwd_context.verify(given_password, hashed_password)

# Used during Auth / Login
ALGORITHM = "HS256"
SECRET_KEY = "5ae48e781d227cabc077167f64005ff949922d586157d6ae07078fee3f3ad170"

# Generate a JWT token used by /auth
def generate_token(given_id:int, username: str):
    payload = {"user_id": given_id, "username": username}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return {
        "access_token": encoded_jwt, # JWT
        "token_type": "bearer"
    }

# Used to retreive the customer id stored in the JWT
def decode_token(given_token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(given_token, SECRET_KEY, algorithms=ALGORITHM) # Vérifie si la signature du JWT (en blue) est valide ou non
        username = payload.get('username')
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError : # if JWT no provided or without a valide signature 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )   
    return username

