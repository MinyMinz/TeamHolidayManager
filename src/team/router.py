from .models import Teams as TeamsModel
from .schema import Teams as TeamSchema
import db.crud as crud
from fastapi import APIRouter, HTTPException

teamRouter = APIRouter()


# Team Routes
@teamRouter.get("")
def fetch_all_teams():
    try:
        teams = crud.dbGetAllRecords(TeamsModel)
    except Exception:
        raise HTTPException(status_code=404, detail="No teams exist")
    return teams


@teamRouter.get("/{name}")
def fetch_team(team_name: str):
    try:
        team = crud.dbGetOneRecordByColumnName(TeamsModel, "name", team_name)
        if team is None:
            raise Exception
    except Exception:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@teamRouter.post("")
def create_team(team: TeamSchema):
    try:
        crud.dbCreate(TeamsModel, dict(team))
    except Exception:
        raise HTTPException(status_code=400, detail="Team could not be created")
    return team


@teamRouter.put("")
def update_team(team: TeamSchema):
    try:
        crud.dbUpdate(TeamsModel, "name", dict(team))
    except Exception:
        raise HTTPException(status_code=400, detail="Team could not be updated")
    return team


@teamRouter.delete("/{name}")
def delete_team(team_name: str):
    try:
        crud.dbDelete(TeamsModel, team_name)
    except Exception:
        raise HTTPException(status_code=400, detail="Team could not be deleted")
    return {"Message": "Team deleted successfully"}
