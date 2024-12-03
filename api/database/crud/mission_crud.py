from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.database.models import Mission


async def new_mission(session: AsyncSession, mission_data: dict):
    async with session:
        res = await session.execute(insert(Mission).values(**mission_data).returning(Mission.id))
        await session.commit()
        return res.scalar()


async def get_missions_with_targets(session: AsyncSession):
    async with session:
        result = await session.execute(select(Mission).options(selectinload(Mission.targets)))
        return result.scalars().all()


async def get_mission_with_targets(session: AsyncSession, mission_id: int):
    async with session:
        result = await session.execute(
            select(Mission).options(selectinload(Mission.targets)).where(Mission.id == mission_id))
        return result.scalars().first()


async def delete_mission(session: AsyncSession, mission_id: int):
    async with session:
        await session.execute(delete(Mission).where(Mission.id == mission_id))
        await session.commit()


async def assign_cat(session: AsyncSession, mission_id: int, cat_id: int):
    async with session:
        await session.execute(
            update(Mission).where(Mission.id == mission_id).values(cat_id=cat_id)
        )
        await session.commit()


async def get_cat(session: AsyncSession, mission_id: int):
    async with session:
        result = await session.execute(select(Mission.cat_id).where(Mission.id == mission_id))
        return result.scalar()


async def complete_mission(session: AsyncSession, mission_id: int):
    async with session:
        await session.execute(update(Mission).where(Mission.id == mission_id).values(is_completed=True))
        await session.commit()

