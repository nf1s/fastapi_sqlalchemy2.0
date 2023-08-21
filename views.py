from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models import User
from db import get_db


class UserSchema(BaseModel):
    full_name: str


class UserSerializer(BaseModel):
    id: str
    full_name: str

    class Config:
        from_attributes = True


api = APIRouter(
    prefix="/users",
)


@api.post("/", response_model=UserSerializer)
async def create_user(user: UserSchema, db_session=Depends(get_db)):
    user = await User.create(db_session, **user.dict())
    return user


@api.get("/{id}", response_model=UserSerializer)
async def get_user(id: str, db_session=Depends(get_db)):
    user = await User.get(db_session, id)
    return user


@api.get("/", response_model=List[UserSerializer])
async def get_all_users(db_session=Depends(get_db)):
    users = await User.get_all(db_session)
    return users


@api.put("/{id}", response_model=UserSerializer)
async def update(id: str, user: UserSchema, db_session=Depends(get_db)):
    user = await User.update(db_session, id, **user.dict())
    return user


@api.delete("/{id}", response_model=bool)
async def delete_user(id: str, db_session=Depends(get_db)):
    return await User.delete(db_session, id)
