# app/services/hero_service.py
from fastapi import HTTPException, status
from typing import List
from sqlmodel import Session
from model.models import Hero
from model.dto import HeroCreate, HeroUpdate, HeroPublic
from repository.hero_repository import HeroRepository
from repository.team_repository import TeamRepository

class HeroService:
    def __init__(self, session: Session):
        self.repo = HeroRepository(session)
        self.team_repo = TeamRepository(session)

    def create(self, payload: HeroCreate) -> HeroPublic:
        if self.repo.get_by_name(payload.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Hero name already exists")
        if payload.team_id is not None and not self.team_repo.get(payload.team_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="team_id not found")
        hero = self.repo.create(payload)
        return HeroPublic.model_validate(hero)

    def list(self, offset: int, limit: int, team_id: int | None = None) -> List[HeroPublic]:
        heroes = (
            self.repo.list_by_team(team_id, offset, limit) if team_id is not None
            else self.repo.list(offset, limit)
        )
        return [HeroPublic.model_validate(h) for h in heroes]

    def get(self, hero_id: int) -> HeroPublic:
        hero = self.repo.get(hero_id)
        if not hero:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
        return HeroPublic.model_validate(hero)

    def update(self, hero_id: int, payload: HeroUpdate) -> HeroPublic:
        hero = self.repo.get(hero_id)
        if not hero:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
        if payload.team_id is not None and not self.team_repo.get(payload.team_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="team_id not found")
        hero = self.repo.update(hero, payload)
        return HeroPublic.model_validate(hero)

    def delete(self, hero_id: int) -> None:
        hero = self.repo.get(hero_id)
        if not hero:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
        self.repo.delete(hero)