from fastapi import APIRouter, HTTPException
from .models import Users as UsersModel
from .schema import Users as UserSchema

import db.crud as crud

userRouter = APIRouter()


@userRouter.get("")
def fetch_user(user_id: int = None, email: str = None, team: str = None):
    # If no query parameters are passed, return all users
    if user_id is None and email is None and team is None:
        try:
            return crud.dbGetAllRecords(UsersModel)
        except Exception:
            raise HTTPException(status_code=404, detail="No users exist")
    else:
        # If query parameters are passed, return the user(s) that match the query
        if user_id is not None:
            try:
                return crud.dbGetOneRecordByColumnName(UsersModel, "id", user_id)
            except Exception:
                raise HTTPException(status_code=404, detail="User not found")
        elif email is not None:
            try:
                return crud.dbGetOneRecordByColumnName(UsersModel, "email", email)
            except Exception:
                raise HTTPException(status_code=404, detail="User not found")
        elif team is not None:
            try:
                return crud.dbGetAllRecordsByColumnName(UsersModel, "team_name", team)
            except Exception:
                raise HTTPException(status_code=404, detail="User not found")
    raise HTTPException(status_code=404, detail="Invalid query parameters")


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
        crud.dbUpdate(UsersModel, "id", dict(user))
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be updated")
    return user


@userRouter.delete("/{user_id}")
def delete_user(user_id: int):
    try:
        crud.dbDelete(UsersModel, user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="User could not be deleted")
    return {"message": "User deleted successfully"}
