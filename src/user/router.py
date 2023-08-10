from . import models, schema
import db.crud as crud
from fastapi import APIRouter, HTTPException

userRouter = APIRouter()

# User Routes
@userRouter.get("/users")
def fetch_all_users():
    try:
        db_users = crud.dbGetAll(models.Users)
    except Exception:
        raise HTTPException(status_code=404, detail="No users exist")
    return db_users

@userRouter.get("/users/{user_id}")
def fetch_user(user_id: int):
    try:
        db_user = crud.dbGet(models.Users, 'id', user_id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@userRouter.post("/users")
def create_user(user: schema.Users):
    try:
        db_user = crud.dbCreate(models.Users, dict(user))
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@userRouter.put("/users")
def update_user(user: schema.Users):
    try:
        db_user = crud.dbUpdate(models.Users, user)
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be updated")
    return db_user

@userRouter.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        crud.dbDelete(models.Users, user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be deleted")

# Role Routes
@userRouter.get("/roles")
def fetch_all_roles():
    try:
        db_roles = crud.dbGetAll(models.Roles)
    except Exception:
        raise HTTPException(status_code=404, detail="No roles exist")
    return db_roles

@userRouter.get("/roles/{role_id}")
def fetch_role(role_id: int):
    try:
        db_role = crud.dbGet(models.Roles, 'id', role_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@userRouter.post("/roles")
def fetch_role(role: schema.Roles):
    try:
        crud.dbCreate(models.Roles, dict(role))
    except Exception:
        raise HTTPException(status_code=404, detail="Role not found")
    return role