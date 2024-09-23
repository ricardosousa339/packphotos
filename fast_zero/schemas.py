from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AlbumSchema(BaseModel):
    price_per_photo: float
    title: str


class AlbumPublic(AlbumSchema):
    id: int
    user_id: int


class AlbumList(BaseModel):
    albums: list[AlbumPublic]


class PhotoSchema(BaseModel):
    name: str
    url: str


class PhotoPublic(PhotoSchema):
    id: int
    album_id: int


class PhotoList(BaseModel):
    photos: list[PhotoPublic]


class PhotoResponse(BaseModel):
    id: int
    album_id: int
    name: str
    url: str


class PurchaseCreate(BaseModel):
    photo_ids: List[int]
    amount: float

class PurchasePublic(BaseModel):
    id: int
    user_id: int
    amount: float
    status: str
    created_at: datetime
    photos: List[PhotoPublic]