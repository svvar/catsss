from fastapi import APIRouter, Depends, status, Body, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from api.database.session import get_db
from api.database.crud.mission_crud import (new_mission, get_missions_with_targets, assign_cat,
                                            get_cat, delete_mission, get_mission_with_targets, complete_mission)
from api.database.crud.target_crud import new_target, update_target, get_target_status
from api.database.crud.cat_crud import check_active_mission
from api.schemas.missions import MissionCreate, MissionRead
from api.schemas.target import UpdateNotes


missions_router = APIRouter()


@missions_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_mission(
        mission: MissionCreate,
        db: AsyncSession = Depends(get_db)
):
    mission_id = await new_mission(db, {k: v for k, v in mission.model_dump().items() if k != "targets"})

    for target in mission.targets:
        await new_target(db, target.model_dump() | {"mission_id": mission_id})

    return {"message": "Mission created"}


@missions_router.get("/", response_model=list[MissionRead])
async def list_missions(
        db: AsyncSession = Depends(get_db)
):
    return await get_missions_with_targets(db)


@missions_router.get("/{mission_id}", response_model=MissionRead)
async def get_mission(
        mission_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await get_mission_with_targets(db, mission_id)


@missions_router.patch("/{mission_id}/cat", status_code=status.HTTP_200_OK)
async def assign_cat_to_mission(
        mission_id: int,
        cat_id: int = Body(..., ge=1, embed=True),
        db: AsyncSession = Depends(get_db)
):
    if await get_cat(db, mission_id):
        return {"message": "Mission already has a cat assigned"}

    if await check_active_mission(db, cat_id):
        return {"message": "Cat is already assigned to an active mission"}

    await assign_cat(db, mission_id, cat_id)
    return {"message": "Cat assigned to mission"}


@missions_router.patch("/target-notes", status_code=status.HTTP_200_OK)
async def update_target_notes(
        target_data: UpdateNotes,
        db: AsyncSession = Depends(get_db)
):
    target_status = await get_target_status(db, target_data.id)
    if target_status:
        return {"message": "Target is completed, notes cannot be updated"}

    await update_target(db, target_data.id, {"id": target_data.target_id, "notes": target_data.notes})
    return {"message": "Target notes updated"}


@missions_router.patch("/target-complete", status_code=status.HTTP_200_OK)
async def update_target_status(
        target_id: int = Body(..., ge=1, embed=True),
        db: AsyncSession = Depends(get_db)
):
    mission_id = await update_target(db, target_id, {"is_completed": True})
    text = "Target is completed. "
    mission = await get_mission_with_targets(db, mission_id)
    if all(target.is_completed for target in mission.targets):
        await complete_mission(db, mission_id)
        text += "All tasks are completed. Mission is completed"

    return {"message": text}


@missions_router.delete("/{mission_id}")
async def delete_mission(
        mission_id: int,
        db: AsyncSession = Depends(get_db)
):
    if await get_cat(db, mission_id):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mission has a cat assigned")

    await delete_mission(db, mission_id)



