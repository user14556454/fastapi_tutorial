from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def posts(db : Session = Depends(get_db),
           current_user: models.User = Depends(oauth2.get_current_user),
           Limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # curr.execute(""" SELECT * FROM posts""")
    # post = curr.fetchall()

    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                       models.Post.id == models.Vote.post_id,
                       isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def createpost(cp: schemas.CreatePost, db : Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # curr.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #             (cp.title, cp.content, cp.published))
    # new_post = curr.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id ,**cp.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db : Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):

    # curr.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = curr.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def post_delete(id: int, db : Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # post = curr.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    if current_user.id != post.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid details")
    post.delete(synchronize_session=False)
    db.commit()
    # conn.commit()       
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ResponsePost)
def post_update(id: int, up: schemas.Post, db : Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # curr.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #              (up.title, up.content, up.published, id))
    # updated_post = curr.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} not found")
    if current_user.id != post_query.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid details")
    post_query.update(up.model_dump(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first()