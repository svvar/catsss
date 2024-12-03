from pydantic import BaseModel, Field, field_validator
from typing import Optional

from api.schemas.target import TargetCreate, TargetRead


class Mission(BaseModel):
    name: str


class MissionCreate(Mission):
    targets: list[TargetCreate]

    @field_validator("targets")
    @classmethod
    def check_targets(cls, v):
        if len(v) > 3:
            raise ValueError("Too many targets for mission")

        return v


class MissionUpdate(BaseModel):
    is_completed: bool = False


class MissionRead(Mission):
    id: int
    cat_id: int | None = None
    is_completed: bool
    targets: list[TargetRead]

    class Config:
        from_attributes = True
