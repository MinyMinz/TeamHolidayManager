from . import models, schema
import db.crud as crud
from fastapi import APIRouter, HTTPException

userRouter = APIRouter()

# User Routes
@userRouter.get("")
def fetch_all_users():
    try:
        db_users = crud.dbGetAll(models.Users)
    except Exception:
        raise HTTPException(status_code=404, detail="No users exist")
    return db_users

@userRouter.get("/{user_id}")
def fetch_user(user_id: int):
    try:
        db_user = crud.dbGet(models.Users, 'id', user_id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@userRouter.get("/email/{email}")
def fetch_user_by_email(email: str):
    try:
        db_user = crud.dbGet(models.Users, 'email', email)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@userRouter.post("")
def create_user(user: schema.Users):
    try:
        db_user = crud.dbCreate(models.Users, dict(user))
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@userRouter.put("")
def update_user(user: schema.Users):
    try:
        db_user = crud.dbUpdate(models.Users, user)
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be updated")
    return db_user

@userRouter.delete("/{user_id}")
def delete_user(user_id: int):
    try:
        crud.dbDelete(models.Users, user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be deleted")
    return {"message": "User deleted successfully"}