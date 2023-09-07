from fastapi import APIRouter, HTTPException, status
from models.user import Users as UsersModel
from schemas.user import Users as UserSchema
from schemas.user import Auth as AuthSchema
import db.crud as crud


userRouter = APIRouter()


@userRouter.post("/login", status_code=status.HTTP_200_OK)
def login_user(login: AuthSchema):
    """Login a user
    \n Args:
    \n    login (AuthSchema): The email and password of the user to login"""
    if login.email is not None and login.password is not None:
        user = crud.getOneRecordByColumnName(UsersModel, "email", login.email)
        if user["password"] != login.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login details",
            )


@userRouter.get("", status_code=status.HTTP_200_OK)
def fetch_user(user_id: int = None, email: str = None, team: str = None):
    """Fetch a user by id, email, or team name or all users
    \n Args:
    \n    Optional user_id (int): The id of the user to fetch
    \n    Optional email (str): The email of the user to fetch
    \n    Optional team (str): The team name of the users to fetch"""
    # If no query parameters are passed, return all users
    if user_id is None and email is None and team is None:
        return crud.getAllRecords(UsersModel)
    else:
        # If query parameters are passed, return the user(s) that match the query
        if user_id is not None:
            return crud.getOneRecordByColumnName(UsersModel, "id", user_id)
        elif email is not None:
            return crud.getOneRecordByColumnName(UsersModel, "email", email)
        elif team is not None:
            return crud.getAllRecordsByColumnName(UsersModel, "team_name", team)


@userRouter.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    """Create a new user"""
    crud.create(UsersModel, dict(user))


@userRouter.put("", status_code=status.HTTP_200_OK)
def update_user(user: UserSchema):
    """Update an existing user"""
    crud.getOneRecordByColumnName(UsersModel, "id", user.id)
    crud.update(UsersModel, "id", dict(user))


@userRouter.delete("", status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    """Delete an existing user
    \n Args:
    \n    user_id (int): The id of the user to delete"""
    crud.delete(UsersModel, user_id)