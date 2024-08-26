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
    title: str


class AlbumPublic(AlbumSchema):
    id: int


class AlbumList(BaseModel):
    albums: list[AlbumPublic]


class PhotoSchema(BaseModel):
    name: str


class PhotoPublic(PhotoSchema):
    id: int


class PhotoList(BaseModel):
    todos: list[PhotoPublic]
