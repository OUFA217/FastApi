from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,Schemas,utils 
from ..database import  get_db





router=APIRouter(
    prefix="/users",
    tags= ['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Schemas.UserOut)
def created_user(user:Schemas.UserCreate ,db: Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    New_User=models.Users(**user.dict())
    db.add(New_User)
    db.commit()
    db.refresh(New_User)
    return New_User

@router.get("/{id}",response_model=Schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not found ")
    return user

