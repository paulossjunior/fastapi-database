from model.models import HeroBase, TeamBase
from typing import  List, Optional
from sqlmodel import Field



class TeamCreate(TeamBase):
    pass

class TeamPublic(TeamBase):
    id: int
    model_config = {"from_attributes": True}

class TeamWithHeroes(TeamPublic):
    heroes: List["HeroPublic"] = []
    model_config = {"from_attributes": True}


class HeroCreate(HeroBase):
    team_id: Optional[int] = None  # permite já criar vinculado a um time

class HeroUpdate(HeroBase):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    secret_name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=200)
    
class HeroPublic(HeroBase):
    id: int
    model_config = {"from_attributes": True}
