from optparse import Option
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

#defining the base mode of a new or updated post (our schema) using pydantic  
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#heritating the property from our PosteBase BaseModel (here with no addional properties but we could evolve it)
class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True  # For Pydantic to read something else than a dictionary (in that case a SqlAlchemy model), we need to pass orm_mode to True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True  # For Pydantic to read something else than a dictionary (in that case a SqlAlchemy model), we need to pass orm_mode to True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True  # For Pydantic to read something else than a dictionary (in that case a SqlAlchemy model), we need to pass orm_mode to True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # ge enforces integer to be greater than or equal to the set value and enforces integer to be less than or equal to the set value


