from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Made it because id don't want people to see everyone else's user id
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    # id: int
    # created_at: datetime
    user_id: int
    # you don't need it if you're not working with any ORM model
    class Config:
        orm_mode = True

# --- USER --- #
################

class UserCreate(BaseModel): # HTTP Request
    email: EmailStr
    password: str

class UserOut(BaseModel): # HTTP Response
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
################

# --- LOGIN --- #
#################

class UserLogin(BaseModel):
    email: EmailStr
    password: str
#################

# --- JWT --- #
#################

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str = None
#################

class GetPostResponse(BaseModel):
    title: str
    content: str
    published: bool
    user: UserOut
    
    class Config:
        orm_mode = True

class GetPostResponseWithLikes(BaseModel):
    Post: GetPostResponse
    post_likes: int

    class Config:
        orm_mode = True

class LikePost(BaseModel): # HTTP Request
    postId: int
    voteDir: bool

    class Config:
        orm_mode = True

