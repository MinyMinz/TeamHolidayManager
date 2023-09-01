from .models import Roles as RolesModel
from .schema import Roles as RoleSchema
import db.crud as crud
from fastapi import APIRouter, HTTPException

roleRouter = APIRouter()


@roleRouter.get("")
def fetch_all_roles():
    try:
        db_roles = crud.dbGetAllRecords(RolesModel)
    except Exception:
        raise HTTPException(404, "No roles exist")
    return db_roles


@roleRouter.get("/{name}")
def fetch_role(role_name: str):
    try:
        db_role = crud.dbGetOneRecordByColumnName(RolesModel, "name", role_name)
    except Exception:
        raise HTTPException(404, "Role not found")
    return db_role


@roleRouter.post("")
def fetch_role(role: RoleSchema):
    try:
        crud.dbCreate(RolesModel, dict(role))
    except Exception:
        raise HTTPException(400, "Cannot create role")
    return role
