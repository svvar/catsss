from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.models import Target


async def new_target(session: AsyncSession, target_data: dict):
    async with session:
        await session.execute(insert(Target).values(**target_data))
        await session.commit()


async def get_target_status(session: AsyncSession, target_id: int):
    async with session:
        result = await session.execute(select(Target.is_completed).where(Target.id == target_id))
        return result.scalar()


async def update_target(session: AsyncSession, target_id: int, target_data: dict):
    async with session:
        res = await session.execute(update(Target).where(Target.id == target_id).values(**target_data).returning(Target.mission_id))
        await session.commit()
        return res.scalar()
