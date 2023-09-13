
#import not from sqlachemy.


#This is import is for sql alchemy
from . database import Base
from sqlalchemy.sql.expression import null, text
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts" 
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default='TRUE', nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()')) 
    
     # Foreign Key
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Relationship with the Users table
    owner = relationship("Users")

    
class Users(Base):
    __tablename__ = "users" 
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()')) 
    
     # Relationship with the Posts table


class Vote(Base):
    __tablename__ = "votes" 

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)