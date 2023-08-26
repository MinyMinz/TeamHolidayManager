from .models import Roles as RolesModel
from .schema import Roles as RoleSchema
import db.crud as crud
from fastapi import APIRouter, HTTPException

roleRouter = APIRouter()

# Role Routes
@roleRouter.get("")
def fetch_all_roles():
    try:
        db_roles = crud.dbGetAll(RolesModel)
    except Exception:
        raise HTTPException(status_code=404, detail="No roles exist")
    return db_roles

@roleRouter.get("/{role_id}")
def fetch_role(role_id: int):
    try:
        db_role = crud.dbGet(RolesModel, 'id', role_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@roleRouter.post("")
def fetch_role(role: RoleSchema):
    try:
        crud.dbCreate(RolesModel, dict(role))
    except Exception:
        raise HTTPException(status_code=404, detail="Role not found")
    return role