from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostCreate(BaseModel):
    text: constr(min_length=1, max_length=1000)