from . import models, schema
import db.crud as crud
from fastapi import APIRouter, HTTPException

roleRouter = APIRouter()

# Role Routes
@roleRouter.get("")
def fetch_all_roles():
    try:
        db_roles = crud.dbGetAll(models.Roles)
    except Exception:
        raise HTTPException(status_code=404, detail="No roles exist")
    return db_roles

@roleRouter.get("/{role_id}")
def fetch_role(role_id: int):
    try:
        db_role = crud.dbGet(models.Roles, 'id', role_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@roleRouter.post("")
def fetch_role(role: schema.Roles):
    try:
        crud.dbCreate(models.Roles, dict(role))
    except Exception:
        raise HTTPException(status_code=404, detail="Role not found")
    return role