from models.role import Roles as RolesModel
from schemas.role import Roles as RoleSchema
import db.crud as crud
from fastapi import APIRouter, HTTPException, status

roleRouter = APIRouter()


@roleRouter.get("")
def fetch_role(role_name: str = None):
    """Fetch a role by name or all roles
    \n Args:
        Optional role_name (str): The name of the role to fetch"""
    if role_name is not None:
        return crud.dbGetOneRecordByColumnName(RolesModel, "name", role_name)
    return crud.dbGetAllRecords(RolesModel)

@roleRouter.post("")
def fetch_role(role: RoleSchema):
    """Create a new role"""
    crud.dbCreate(RolesModel, dict(role))
    raise HTTPException(status.HTTP_201_CREATED)
