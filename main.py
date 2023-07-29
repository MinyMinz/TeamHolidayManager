from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .db import crud, schemas
from .db import models
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Get all users
@app.get("/users", response_model=list[schemas.User])
def fetch_all_users():
    db_users = crud.dbGetAll(models.User)
    if db_users is None:
        raise HTTPException(status_code=404, detail="No users exist")
    return db_users

#Get user by id
@app.get("/users/{user_id}", response_model=schemas.User)
def fetch_user_by_id(user_id: int):
    db_user = crud.dbGet(models.User, "id", user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#Get user by email
@app.get("/users/{email}", response_model=schemas.User)
def fetch_user_by_email(email: str):
    db_user = crud.dbGet(models.User, "email", email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#Create a user
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db_user = crud.dbGet(models.User, "email", user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.dbCreate(models.User, user) 
