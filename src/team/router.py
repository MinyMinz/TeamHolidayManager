from . import models, schema
import db.crud as crud
from fastapi import APIRouter, HTTPException

teamRouter = APIRouter()

# Team Routes
@teamRouter.get("")
def fetch_all_teams():
    try:
        teams = crud.dbGetAll(models.Teams)
    except Exception:
        raise HTTPException(status_code=404, detail="No teams exist")
    return teams

@teamRouter.get("/{team_id}")
def fetch_team(team_id: int):
    try:
        team = crud.dbGet(models.Teams, 'id', team_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@teamRouter.post("")
def create_team(team: schema.Teams):
    try:
        crud.dbCreate(models.Teams, dict(team))
    except Exception:
        raise HTTPException(status_code=400, detail="Team could not be created")
    return team

@teamRouter.put("")
def update_team(team: schema.Teams):
    try:
        response = crud.dbUpdate(models.Teams, team)
    except Exception:
        raise HTTPException(status_code=400, detail="Team could not be updated")
    return response

@teamRouter.delete("/{team_id}")
def delete_team(team_id: int):
    try:
        crud.dbDelete(models.Teams, team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Team could not be deleted")
    return {"Message": "Team deleted successfully"}