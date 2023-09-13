from typing import Optional, List
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, auth2
from .. database import engine, SessionLocal, get_db
from sqlalchemy import desc


router = APIRouter(
    prefix="/vote",
     tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED) 
def add_user(vote: schemas.Vote, db: Session = Depends(get_db),current_user: int = Depends(auth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="no post found")    

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"user {current_user.id} is already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {'message': 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')
        
        vote_query.delete(synchronize_session=False)
        db.commit()  
        return {'message': 'successfully deleted vote'}


