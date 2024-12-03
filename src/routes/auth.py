from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from db import crud
from starlette import status
from models.user import Users as UsersModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

authRouter = APIRouter()

SECRET_KEY = "Temp"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str


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
    
    token = create_access_token(form_data.username, user["id"], timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(username: str, password: str):
    user = crud.getOneRecordByColumnName(UsersModel, "email", username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(email: str, user_id: str, expries_delta: timedelta):
    ## excluded expire for now to avoid issues with testing and demonstrations
    # expire = datetime.now() + expries_delta
    to_encode = {"sub": email, "id": user_id}
    # to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def fetch_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user credentials.")
        return {
            "email": email,
            "id": user_id
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user credentials.")
