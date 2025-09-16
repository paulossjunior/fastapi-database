# app/controllers/teams.py
from typing import List, Annotated
from fastapi import APIRouter, Depends, Query
from util.database import SessionDep
from model.dto import TeamCreate, TeamPublic, TeamWithHeroes
from service.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])

def get_team_service(session: SessionDep) -> TeamService:
    return TeamService(session)

ServiceDep = Annotated[TeamService, Depends(get_team_service)]

@router.post("/", response_model=TeamPublic, status_code=201)
def create_team(payload: TeamCreate, service: ServiceDep):
    return service.create(payload)

@router.get("/", response_model=List[TeamPublic])
def list_teams(
    service: ServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    return service.list(offset, limit)

@router.get("/{team_id}", response_model=TeamWithHeroes)
def get_team(team_id: int, service: ServiceDep):
    return service.get(team_id)
