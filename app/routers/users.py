from typing import Optional, List
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, auth2
from .. database import engine, SessionLocal, get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model=schemas.NewUser) 
def add_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    
    return new_user


@router.get('/{id}', response_model=schemas.UserInfo)
def get_user(id:int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    
    user =  db.query(models.Users).filter(models.Users.id == id).first()
  
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'this id: {id} does not exist.')

    return user