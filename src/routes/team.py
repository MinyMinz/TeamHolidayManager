from models.team import Teams as TeamsModel
from schemas.team import Teams as TeamSchema
import db.crud as crud
from fastapi import APIRouter, HTTPException, status

teamRouter = APIRouter()


# Team Routes
@teamRouter.get("", status_code=status.HTTP_200_OK)
def fetch_team(team_name: str = None):
    """Fetch a team by name or all teams
    \n Args:
        Optional team_name (str): The name of the team to fetch"""
    if team_name is not None:
        return crud.getOneRecordByColumnName(TeamsModel, "name", team_name)
    return crud.getAllRecords(TeamsModel)


@teamRouter.post("", status_code=status.HTTP_201_CREATED)
def create_team(team: TeamSchema):
    """Create a new team"""
    crud.create(TeamsModel, dict(team))
