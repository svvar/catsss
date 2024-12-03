from pydantic import BaseModel, Field
from typing import Optional


class Target(BaseModel):
    name: str
    country: str
    notes: str | None = None
    is_completed: bool = False


class TargetCreate(Target):
    pass


class TargetRead(Target):
    id: int

    class Config:
        from_attributes = True


class UpdateNotes(BaseModel):
    target_id: int
    notes: str | None = None

