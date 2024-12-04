from fastapi import APIRouter, Depends, status, HTTPException
from routes.auth import fetch_current_user
from models.team import Teams as TeamsModel
from schemas.team import Teams as TeamSchema
import db.crud as crud

teamRouter = APIRouter()

# Team Routes
@teamRouter.get("", status_code=status.HTTP_200_OK)
def fetch_team(team_name: str = None, payload=Depends(fetch_current_user)):
    """Fetch a team by name or all teams
    \n Args:
        Optional team_name (str): The name of the team to fetch"""
    if team_name is not None:
        return crud.getOneRecordByColumnName(TeamsModel, "name", team_name)
    return crud.getAllRecords(TeamsModel)

@teamRouter.post("", status_code=status.HTTP_201_CREATED)
def create_team(team: TeamSchema, payload=Depends(fetch_current_user)):
    """Create a new team"""
        # Check if user is superAdmin if not raise an error
    if payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to create a team",
        )
    crud.create(TeamsModel, dict(team))

@teamRouter.put("", status_code=status.HTTP_200_OK)
def update_team(team: TeamSchema, payload=Depends(fetch_current_user)):
    """Update a team"""
        # Check if user is superAdmin if not raise an error
    if payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update a team",
        )
    crud.update(TeamsModel, dict(team))

@teamRouter.delete("", status_code=status.HTTP_200_OK)
def delete_team(team_name: str, payload=Depends(fetch_current_user)):
    """Delete a team"""
    # Check if user is superAdmin if not raise an error
    if payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete a team",
        )
    
    # first check that the team exists then delete it
    crud.getOneRecordByColumnName(TeamsModel, "name", team_name)
    crud.delete(TeamsModel, "name", team_name)
