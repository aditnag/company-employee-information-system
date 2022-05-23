from fastapi import APIRouter, status, HTTPException, Depends
from schemas import UserSchema, MyUserSchema
from schemas import CompanySchema, MyCompanySchema
from typing import List
from db import Employee, database, engine, User
from passlib.hash import pbkdf2_sha256

router = APIRouter(
    tags=["Users"]
)


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=MyUserSchema)
async def save_user(user: UserSchema):
    hashed_password = pbkdf2_sha256.hash(user.password)
    query = User.insert().values(username=user.username, password=hashed_password)
    last_record_id = await database.execute(query)  # execute_query
    return {**user.dict(), "id": last_record_id}


@router.put("/users/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=MyUserSchema)
async def update_users(id: int, user: UserSchema):
    query = User.update().where(id == User.c.id).values(username=user.username, password=user.password)
    await database.execute(query=query)
    return {**user.dict(), "id": id}


@router.get("/users/", status_code=status.HTTP_200_OK, response_model=List[MyUserSchema])
async def get_all_users():
    query = User.select()
    return await database.fetch_all(query=query)


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(id: int):
    query = User.delete().where(id == User.c.id)
    await database.execute(query=query)
    return "User deleted!"
