from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from .. import database,schemas, models, utils, auth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication'],

)

@router.post('/login', response_model=schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    
    user = db.query(models.Users).filter(models.Users.email == user_credential.username).first()
   
    if not user:
       raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"this user: \'{user_credential.username}\' does not exist")
   
    if not utils.verify(user_credential.password, user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credential")
   
    #create a token
    access_token = auth2.create_access_token(data={"user_id": str(user.id)})
    
    #return token
    return {'access_token': access_token, "token_type": "bearer"}
   
   
   
   
   
   
   
   