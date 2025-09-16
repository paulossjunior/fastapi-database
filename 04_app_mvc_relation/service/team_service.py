# app/services/team_service.py
from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session
from model.dto import TeamCreate, TeamPublic, TeamWithHeroes
from repository.team_repository import TeamRepository

class TeamService:
    def __init__(self, session: Session):
        self.repo = TeamRepository(session)

    def create(self, payload: TeamCreate) -> TeamPublic:
        if self.repo.get_by_name(payload.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Team name already exists")
        team = self.repo.create(payload)
        return TeamPublic.model_validate(team)

    def list(self, offset: int, limit: int) -> List[TeamPublic]:
        teams = self.repo.list(offset, limit)
        return [TeamPublic.model_validate(t) for t in teams]

    def get(self, team_id: int) -> TeamWithHeroes:
        team = self.repo.get(team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        # Retorna time com heróis aninhados
        return TeamWithHeroes.model_validate(team)
