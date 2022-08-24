from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import APIRouter,Depends,status,HTTPException,Response,FastAPI
from app import Schemas
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
#Secret_Key
#Algorith
#Expiration_Time
SECRET_KEY="430A1C34C1123186D6DEED0239F6860385F335660DCE7D5A63ED7379F162CFD1"
Algorithm="HS256"
ACCESS_TOKEN_EXPIRES_MINUTES=10
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt= jwt.encode(to_encode,SECRET_KEY,algorithm=Algorithm)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms={Algorithm})
        id:str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=Schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=
    f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credentials_exception)
