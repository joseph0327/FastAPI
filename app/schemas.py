from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint




#-----------------------THIS IS FOR USERS----------------------#


#handling user's request
class UserCreate(BaseModel):
    email: EmailStr
    password: str




#handling response to the user

class NewUser(BaseModel):
    email: EmailStr
    id:int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class UserInfo(NewUser):
    pass
    
    class Config:
        from_attributes = True
        



#----------------------THIS IS FOR POSTS----------------------#

#handling user's request

class PostBase(BaseModel):
    title:str
    content:str
    published : bool=True
    

class CreatePost(PostBase):
    pass
    
    
class UpdatePost(PostBase):
    pass
    

#handling response to the user

class Post(PostBase):
    id:int
    created_at: datetime
    owner_id: int
    owner:NewUser
    
    
    class Config:
        from_attributes = True


class PostOutVote(BaseModel):
    Post:Post
    votes:int
    
    class Config:
        from_attributes = True

#-----------------------THIS IS FOR LOGIN----------------------#


#user's request
class UserLogin(BaseModel):
    email:EmailStr
    password: str
    
class TokenData(BaseModel): 
    id: Optional[str] = None  
    
    
#response to the user
class Token(BaseModel):
    access_token: str
    token_type: str
    
#----------------------THIS IS FOR Vote----------------------#

#user's request
class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)