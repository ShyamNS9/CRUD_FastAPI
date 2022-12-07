from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint
from pydantic.validators import datetime


class UserBase(BaseModel):
    email: EmailStr
    user_name: str
    password: str


class CreateUser(UserBase):
    pass


class ResponseUsersSchema(BaseModel):
    id: int
    email: EmailStr
    user_name: str
    created_at: datetime

    class Config:
        orm_mode = True  # let the pydentic know that we are using orm model
        # pydentic only works with dict so if we specify orm_mode = True it will work fine


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePostSchema(BaseSchema):
    pass


class UpdatePostSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]


class ResponsePostSchema(BaseSchema):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUsersSchema

    class Config:
        orm_mode = True


class ResponsePostSchemaWithVote(BaseModel):
    Post: ResponsePostSchema
    Vote_count: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)
