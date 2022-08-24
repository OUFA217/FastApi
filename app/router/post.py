from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

from app import Oauth2
from .. import models,Schemas
from ..database import  get_db
from typing import List 

router=APIRouter(
    prefix="/posts",
    tags= ['Posts']

)

@router.get("/",response_model=List[Schemas.Post])
def get_posts(db: Session = Depends(get_db),user_id: int=Depends(Oauth2.get_current_user)):
    # cursor.execute("""Select * FROM posts""")
    # posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return posts



@router.post("/",status_code=status.HTTP_201_CREATED)
def create_posts(post:Schemas.PostBase,db: Session = Depends(get_db),user_id: int=Depends(Oauth2.get_current_user)):
    # cursor.execute("""Insert INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # New_Post=cursor.fetchone()
    # conn.commit()
    # New_Post=models.Post(title=post.title,content=post.content,Published=post.published)
    New_Post=models.Post(**post.dict())
    db.add(New_Post)
    db.commit()
    db.refresh(New_Post)
    return{"data":New_Post}

    # post_dict=post.dict()
    # post_dict['id']=randrange(0, 100000)
    # My_Posts.append(post_dict)
    # return{"data":post_dict}




@router.get("/{id}",response_model=Schemas.Post)
def get_IDposts(id:int,db: Session = Depends(get_db),user_id: int=Depends(Oauth2.get_current_user) ):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """,(str(id)))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    
    return{"Post Detail":post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),user_id: int=Depends(Oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning*""",(str(id)))
    # Deleted_Post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    
    if post.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not found ")

    post.delete(synchronize_session=False)
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=Schemas.Post)
def update_post(id:int,updated_post:Schemas.Post_Create,db: Session = Depends(get_db),user_id: int=Depends(Oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s returning*""",(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not found ")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    

    return post_query.first()