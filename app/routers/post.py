from typing import Optional, List
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, utils, auth2
from fastapi.responses import JSONResponse
from .. database import engine, SessionLocal, get_db
from sqlalchemy import desc

router = APIRouter(
    prefix="/post",
     tags=['Post']
)



@router.get("/all", response_model=List[schemas.PostOutVote])
def get_all_post(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user),
                 limit: int = 0 , skip: int = 0, search: Optional[str]=""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .all()
        #.limit(limit) \
        #.offset(skin) \
    
    return results


#get all the top 5 latest post
@router.get("/latest", response_model=List[schemas.PostOutVote])
def get_latest(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user),
                 limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .order_by(desc(models.Post.created_at)) \
        .limit(limit) \
        .all()
        
    return posts


#get all post from a the user that is logged in
@router.get("/", response_model=List[schemas.PostOutVote])
def get_all_post(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
     
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.owner_id == current_user.id) \
        .all()
    
    return posts
 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)): 
    print(current_user)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post


@router.get("/{id}", response_model=schemas.PostOutVote) 
def get_post_details(id:int, db: Session = Depends(get_db),  current_user: int = Depends(auth2.get_current_user), search: Optional[str]=""):

    post  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .first()
        
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f" post with an id of {id} is not found")
        
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This id \'{id}\' does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized! You're not the owner of this post.")
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return JSONResponse(content={"message": "Post deleted successfully"}, status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post) 
def update_post(id:int, updated_post:schemas.UpdatePost, db: Session = Depends(get_db),current_user: int = Depends(auth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This id \'{id}\' does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized! You are not the owner of this post.")
  
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()


    return post_query.first()
