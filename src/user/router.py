from . import models
import db.crud as crud
from fastapi import APIRouter, HTTPException, Depends

userRouter = APIRouter()

@userRouter.get("/users")
def fetch_all_users():
    db_users = crud.dbGetAll(models.User)
    if db_users is None or len(db_users) == 0:
        raise HTTPException(status_code=404, detail="No users exist")
    return db_users
