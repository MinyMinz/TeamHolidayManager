from os import environ as env
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from db import crud
from starlette import status
from models.user import Users as UsersModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from schemas.user import UserAPI as UserAPISchema

authRouter = APIRouter()

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str
    user_data: dict

@authRouter.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login a user
    \n Args:
    \n    The email and password of the user to login"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user credentials.")
    
    user_data = mapToUserAPISchema(user)
    
    token = create_access_token(user_data, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer","user_data": dict(user_data)}

def authenticate_user(username: str, password: str):
    user = crud.getOneRecordByColumnName(UsersModel, "email", username)
    if not user:
        return False
    verification = bcrypt_context.verify(password, user["password"])
    if verification == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.")
    return user

def create_access_token(user_data: UserAPISchema, expries_delta: timedelta):
    ##NOTE excluded expire for now for demonstrations
    # expire = datetime.now() + expries_delta
    to_encode = {"id": user_data.id, "sub": user_data.email, "role_name": user_data.role_name, "team_name": user_data.team_name}
    # to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def fetch_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        email: str = payload.get("sub")
        role: str = payload.get("role_name")
        team: str = payload.get("team_name")
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user credentials.")
        return {
            "id": user_id,            
            "email": email,
            "role_name": role,
            "team_name": team
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "JWT Error")

def check_if_user_is_superAdmin(payload: dict, detail: str):
    if payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= detail
        )

def mapToUserAPISchema(user):
    return UserAPISchema(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        team_name=user["team_name"],
        role_name=user["role_name"]
    )
