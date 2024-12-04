from fastapi import APIRouter, Depends, status
from routes.auth import fetch_current_user
from models.role import Roles as RolesModel
from schemas.role import Roles as RoleSchema
import db.crud as crud
from fastapi import APIRouter, status

roleRouter = APIRouter()

@roleRouter.get("", status_code=status.HTTP_200_OK)
def fetch_role(payload=Depends(fetch_current_user)):
    """Fetch a role by name or all roles
    \n Args:
        Optional role_name (str): The name of the role to fetch"""
    if payload["role_name"] == "Admin" or payload["role_name"] == "User":
        return crud.getOneRecordByColumnName(RolesModel, "name", "User")
    return crud.getAllRecords(RolesModel)

@roleRouter.post("", status_code=status.HTTP_201_CREATED)
def fetch_role(role: RoleSchema, payload=Depends(fetch_current_user)):
    """Create a new role"""
    crud.create(RolesModel, dict(role))
