from models.role import Roles as RolesModel
from schemas.role import Roles as RoleSchema
import db.crud as crud
from fastapi import APIRouter, status

roleRouter = APIRouter()


@roleRouter.get("", status_code=status.HTTP_200_OK)
def fetch_role(role_name: str = None):
    """Fetch a role by name or all roles
    \n Args:
        Optional role_name (str): The name of the role to fetch"""
    if role_name is not None:
        return crud.getOneRecordByColumnName(RolesModel, "name", role_name)
    return crud.getAllRecords(RolesModel)

@roleRouter.post("", status_code=status.HTTP_201_CREATED)
def fetch_role(role: RoleSchema):
    """Create a new role"""
    crud.create(RolesModel, dict(role))
