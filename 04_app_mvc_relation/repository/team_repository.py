# app/repositories/team_repository.py
from typing import List, Optional
from sqlmodel import Session, select
from model.models import Team 
from model.dto import TeamCreate

class TeamRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self, offset: int = 0, limit: int = 100) -> List[Team]:
        return list(self.session.exec(select(Team).offset(offset).limit(limit)).all())

    def get(self, team_id: int) -> Optional[Team]:
        return self.session.get(Team, team_id)

    def get_by_name(self, name: str) -> Optional[Team]:
        return self.session.exec(select(Team).where(Team.name == name)).first()

    def create(self, data: TeamCreate) -> Team:
        team = Team.model_validate(data)
        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team
