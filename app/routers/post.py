from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app import oauth2
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# GET ALL POSTS 
@router.get("/", response_model=List[schemas.PostOut])
# WITH ORM SQLALCHEMY
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts
# WITH SQL
# def get_posts():
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # return {"data": posts}


# CREATE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# WITH ORM SQLALCHEMY
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict()) #equivalent to new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# WITH SQL
# def create_posts(post: Post): #Making the post comes with the right scheme i.e. the class Post(BaseModel) defined
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()  #push the changes to the database
#     return {"data": new_post}


# GET ONE POST BASED ON ID
@router.get("/{id}", response_model=schemas.PostOut) #Path parameter
# WITH ORM SQLALCHEMY
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, #using status and HTTPException modules from FastAPI library to return the right HTTP error
                             detail=f"post with id: {id} was not found")
    return post
# WITH SQL
# def get_post(id: int, response: Response): #I want the id input to be an int 
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id))) #we need id to be string to inject it into the SQL query
#     post = cursor.fetchone()
#     if not post: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, #using status and HTTPException modules from FastAPI library to return the right HTTP error
#                             detail=f"post with id: {id} was not found")
#     return {"post_detail": post}


# DELETE ONE POST BASED ON ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #we want to use a 204 for deleted
# WITH ORM SQLALCHEMY
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    else: 
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
# WITH SQL
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
#     deleted_post = cursor.fetchone()
#     conn.commit() #push the changes to the database
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE ONE POST BASED ON ID
@router.put("/{id}", response_model=schemas.Post)
# WITH ORM SQLALCHEMY
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    else:
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()
    return post_query.first()
# WITH SQL
# def update_post(id: int, post: Post): #Making the post comes with the right scheme i.e. an id as integer and the class Post(BaseModel) defined
#     cursor.execute("""UPDATE posts SET title = %s, content =%s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exist")
#     return {"data": updated_post}