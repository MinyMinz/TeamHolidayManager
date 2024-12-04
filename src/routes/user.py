from fastapi import APIRouter, Depends, HTTPException, status
from routes.auth import fetch_current_user, bcrypt_context, check_if_user_is_superAdmin
from models.user import Users as UsersModel
from schemas.user import Users as UserSchema
from schemas.user import UserAPI as UserAPISchema
import db.crud as crud

userRouter = APIRouter()

@userRouter.get("", status_code=status.HTTP_200_OK)
def fetch_user(user_id: int = None, email: str = None, team: str = None, payload=Depends(fetch_current_user)):
    """Fetch a user by id, email, or team name or all users
    \n Args:
    \n    Optional user_id (int): The id of the user to fetch
    \n    Optional email (str): The email of the user to fetch
    \n    Optional team (str): The team name of the users to fetch"""

    # If query parameters are passed, return the user(s) that match the query
    if user_id is not None:
        user = crud.getOneRecordByColumnName(UsersModel, "id", user_id)
        return mapToUserAPISchema(user)
    elif email is not None:
        user = crud.getOneRecordByColumnName(UsersModel, "email", email)
        return mapToUserAPISchema(user)
    elif team is not None:
        users = crud.getAllRecordsByColumnName(UsersModel, "team_name", team, "id")
        return [mapToUserAPISchema(user) for user in users]
    else:
        users = crud.getAllRecords(UsersModel, "id")
        return [mapToUserAPISchema(user) for user in users]

@userRouter.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema, payload=Depends(fetch_current_user)):
    """Create a new user"""
    # Check if the user creating the user is not a SuperAdmin
    if payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to create a user"
        )
    # Check if the user to create is the SuperAdmin as SuperAdmin is a reserved role and should always exist
    if user.role_name == "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create a user with this role"
        )
    # Hash the password before saving it to the database
    user.password = bcrypt_context.hash(user.password)
    crud.create(UsersModel, dict(user))

@userRouter.put("", status_code=status.HTTP_200_OK)
def update_user(user: UserAPISchema, payload=Depends(fetch_current_user)):
    """Update an existing user"""
    # Check if the user updating the user is the same user or a SuperAdmin
    if payload["id"] != user.id and payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update this user"
        )
    # Get the user to update
    userToUpdate = crud.getOneRecordByColumnName(UsersModel, "id", user.id)
    # If the user to update is the SuperAdmin and the role set in the request is not SuperAdmin (i.e. superadmin is trying to change their role)
    if userToUpdate["role_name"] == "SuperAdmin" and user.role_name != "SuperAdmin":
        # if above is true throw error HTTP_403_FORBIDDEN
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot change the role of this user"
        )
    # If the user to update is not the SuperAdmin and the role set in the request is SuperAdmin (i.e. the user is trying to make a user a SuperAdmin) 
    elif user.role_name == "SuperAdmin":
        # if above is true throw error HTTP_403_FORBIDDEN
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot assign this role to a user"
        )
    crud.update(UsersModel, "id", dict(user))

@userRouter.patch("/password", status_code=status.HTTP_200_OK)
def update_user_password(user_id: int, password: str, payload=Depends(fetch_current_user)):
    """Update an existing user password
    \n Args:
    \n    user_id (int): The id of the user to update password
    \n    password (str): The new password to set"""
    # Check if the user updating the user is the same user or a SuperAdmin
    if int(payload['id']) != int(user_id) and payload['role_name'] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update this user"
        )
    crud.getOneRecordByColumnName(UsersModel, "id", user_id)
    # Hash the password before saving it to the database
    password = bcrypt_context.hash(password)
    crud.updatePassword(UsersModel, user_id, {"password": password})

@userRouter.delete("", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, payload=Depends(fetch_current_user)):
    """Delete an existing user
    \n Args:
    \n    user_id (int): The id of the user to delete"""
    # Check if the user deleting the user is a SuperAdmin
    check_if_user_is_superAdmin(payload, "You are not authorized to delete a user")

    # Check if the user to delete is the SuperAdmin as SuperAdmin is a reserved role and should always exist
    user = crud.getOneRecordByColumnName(UsersModel, "role_name", "SuperAdmin")
    # If the user to delete is the SuperAdmin throw an error
    if user["id"] != user_id or payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot delete users"
        )
    if user["role_name"] == "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete this user"
        )
    # If the user to delete is not the SuperAdmin delete the user
    crud.delete(UsersModel, "id", user_id)

def mapToUserAPISchema(user):
    return UserAPISchema(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        team_name=user["team_name"],
        role_name=user["role_name"]
    )
