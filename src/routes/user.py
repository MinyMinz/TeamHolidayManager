from fastapi import APIRouter, Depends, HTTPException, status
from routes.auth import fetch_current_user, bcrypt_context, check_if_user_is_superAdmin
from models.user import Users as UsersModel
from schemas.user import Users as UserSchema
from schemas.user import UserAPI as UserAPISchema
import db.crud as crud

userRouter = APIRouter()

@userRouter.get("", status_code=status.HTTP_200_OK)
def fetch_user(payload=Depends(fetch_current_user)):
    """Fetch a user or users"""    
    if payload["role_name"] == "SuperAdmin":
        return [mapToUserAPISchema(user) for user in crud.getAllRecords(UsersModel, "id")]
    elif payload["role_name"] == "Admin":
        return [mapToUserAPISchema(user) for user in crud.getAllRecordsByColumnName(UsersModel, "team_name", payload["team_name"], "id")]
    else:
        return mapToUserAPISchema(crud.getOneRecordByColumnName(UsersModel, "id", payload["id"]))

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
    mappedUser = {"id": None, **mapToUserModel(user)}
    crud.create(UsersModel, mappedUser)

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
    elif user.role_name == "SuperAdmin" and userToUpdate["role_name"] != "SuperAdmin":
        # if above is true throw error HTTP_403_FORBIDDEN
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot assign this role to a user"
        )
    # Check user is not trying to update their own allocated or remaining holidays unless they are a SuperAdmin
    if payload["id"] == user.id and (user.allocated_holidays is not None or user.remaining_holidays is not None) and payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update your allocated or remaining holidays"
        )
    # Update the user
    mappedUser = mapToUserModel(user)
    crud.update(UsersModel, "id", mappedUser)

#Make sure this only updates the password and nothing more
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
    check_if_user_is_superAdmin(payload, "You are not authorized to delete users")

    # Check if the user to delete is the SuperAdmin as SuperAdmin is a reserved role and should always exist
    userToDelete = crud.getOneRecordByColumnName(UsersModel, "id", user_id)
    # If the user to delete is the SuperAdmin throw an error
    if userToDelete["role_name"] == "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete this user"
        )
    crud.delete(UsersModel, "id", user_id)

def mapToUserAPISchema(user: UsersModel):
    return UserAPISchema(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        team_name=user["team_name"],
        role_name=user["role_name"],
        allocated_holidays=user["number_of_allocated_holdiays"],
        remaining_holidays=user["number_of_remaining_holidays"]
    )

def mapToUserModel(user: UserSchema):
    return {
        "email": user.email,
        "full_name": user.full_name,
        "team_name": user.team_name,
        "role_name": user.role_name,
        "number_of_allocated_holdiays": user.allocated_holidays,
        "number_of_remaining_holidays": user.remaining_holidays
    }