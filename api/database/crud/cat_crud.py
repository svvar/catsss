from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.models import SpyCat, Mission


async def new_cat(session: AsyncSession, cat_data: dict):
    async with session:
        await session.execute(insert(SpyCat).values(**cat_data))
        await session.commit()


async def get_cats(session: AsyncSession):
    async with session:
        result = await session.execute(select(SpyCat))
        return result.scalars().all()


async def get_cat(session: AsyncSession, cat_id: int):
    async with session:
        result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))               # type: ignore
        return result.scalars().first()


async def update_cat(session: AsyncSession, cat_id: int, cat_data: dict):
    async with session:
        await session.execute(update(SpyCat).where(SpyCat.id == cat_id).values(**cat_data))     # type: ignore
        await session.commit()


async def delete_cat(session: AsyncSession, cat_id: int):
    async with session:
        await session.execute(delete(SpyCat).where(SpyCat.id == cat_id))                        # type: ignore
        await session.commit()


async def check_active_mission(session: AsyncSession, cat_id: int):
    async with session:
        result = await session.execute(
            select(SpyCat).join(Mission).where(SpyCat.id == cat_id).where(Mission.is_completed.is_(False)).limit(1)  # type: ignore
        )
        return result.scalars().first()
