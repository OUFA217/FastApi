from os import access
from fastapi import APIRouter,Depends,status,HTTPException,Response,FastAPI
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import Schemas,models,utils,Oauth2
router=APIRouter(
    tags=['Authentication']

)
@router.post('/login',response_model=Schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
   user= db.query(models.Users).filter(models.Users.email==user_credential.username).first()
   
   if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invaild Credentials")
   if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invaild Credentials")

   access_token=Oauth2.create_access_token(data={"user_id":user.id})
   return {"access_token":access_token,"token_type":"Bearer"}