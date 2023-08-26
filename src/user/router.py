from .models import Users as UsersModel
from .schema import Users as UserSchema
import db.crud as crud
from fastapi import APIRouter, HTTPException

userRouter = APIRouter()

# User Routes
@userRouter.get("")
def fetch_all_users():
    try:
        db_users = crud.dbGetAll(UsersModel)
    except Exception:
        raise HTTPException(status_code=404, detail="No users exist")
    return db_users

@userRouter.get("/{user_id}")
def fetch_user(user_id: int):
    try:
        db_user = crud.dbGet(UsersModel, 'id', user_id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@userRouter.get("/email/{email}")
def fetch_user_by_email(email: str):
    try:
        db_user = crud.dbGet(UsersModel, 'email', email)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@userRouter.post("")
def create_user(user: UserSchema):
    try:
        db_user = crud.dbCreate(UsersModel, dict(user))
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@userRouter.put("")
def update_user(user: UserSchema):
    try:
        db_user = crud.dbUpdate(UsersModel, user)
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be updated")
    return db_user

@userRouter.delete("/{user_id}")
def delete_user(user_id: int):
    try:
        crud.dbDelete(UsersModel, user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be deleted")
    return {"message": "User deleted successfully"}