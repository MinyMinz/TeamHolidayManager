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
        return user


@userRouter.get("", status_code=status.HTTP_200_OK)
def fetch_user(user_id: int = None, email: str = None, team: str = None):
    """Fetch a user by id, email, or team name or all users
    \n Args:
    \n    Optional user_id (int): The id of the user to fetch
    \n    Optional email (str): The email of the user to fetch
    \n    Optional team (str): The team name of the users to fetch"""

    # If query parameters are passed, return the user(s) that match the query
    if user_id is not None:
        return crud.getOneRecordByColumnName(UsersModel, "id", user_id)
    elif email is not None:
        return crud.getOneRecordByColumnName(UsersModel, "email", email)
    elif team is not None:
        return crud.getAllRecordsByColumnName(UsersModel, "team_name", team, "id")
    else:
        # If no query parameters are passed, return all users
        return crud.getAllRecords(UsersModel, "id")


@userRouter.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    """Create a new user"""
    # Check if the user to create is the SuperAdmin as SuperAdmin is a reserved role and should always exist
    if user.role_name == "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create a user with this role",
        )
    crud.create(UsersModel, dict(user))


@userRouter.put("", status_code=status.HTTP_200_OK)
def update_user(user: UserSchema):
    """Update an existing user"""
    # Get the user to update
    userToUpdate = crud.getOneRecordByColumnName(UsersModel, "id", user.id)
    # If the user to update is the SuperAdmin and the role set in the request is not SuperAdmin (i.e. superadmin is trying to change their role)
    if userToUpdate["role_name"] == "SuperAdmin" and user.role_name != "SuperAdmin":
        # if above is true throw error HTTP_403_FORBIDDEN
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot change the role of this user",
        )
    # If the user to update is not the SuperAdmin and the role set in the request is SuperAdmin (i.e. the user is trying to make a user a SuperAdmin) 
    elif userToUpdate["role_name"] != "SuperAdmin" and user.role_name == "SuperAdmin":
        # if above is true throw error HTTP_403_FORBIDDEN
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot assign this role to a user",
        )
    crud.update(UsersModel, "id", dict(user))


@userRouter.delete("", status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    """Delete an existing user
    \n Args:
    \n    user_id (int): The id of the user to delete"""
    # Check if the user to delete is the SuperAdmin as SuperAdmin is a reserved role and should always exist
    user = crud.getOneRecordByColumnName(UsersModel, "role_name", "SuperAdmin")
    # If the user to delete is the SuperAdmin throw an error
    if user["id"] == user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot delete this user",
        )
    # If the user to delete is not the SuperAdmin delete the user
    crud.delete(UsersModel, "id", user_id)
