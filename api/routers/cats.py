from aiohttp import ClientSession
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from api.database.session import get_db
from api.database.crud.cat_crud import new_cat, get_cats, get_cat, update_cat, delete_cat
from api.schemas.cat import CreateCat, CatResponse


cats_router = APIRouter()


@cats_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_cat(
        cat: CreateCat,
        db: AsyncSession = Depends(get_db)
):
    if await validate_breed(cat.breed):
        await new_cat(db, cat.model_dump())
        return {'message': 'Cat created'}
    else:
        return {'message': 'Invalid breed'}


@cats_router.get('/', response_model=list[CatResponse])
async def get_cats_list(
        db: AsyncSession = Depends(get_db)
):
    return await get_cats(db)


@cats_router.get('/{cat_id}', response_model=CatResponse)
async def get_cat_by_id(
        cat_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await get_cat(db, cat_id)


@cats_router.patch('/{cat_id}')
async def modify_cat(
        cat_id: int,
        cat: CreateCat,
        db: AsyncSession = Depends(get_db)
):
    await update_cat(db, cat_id, cat.model_dump())
    return {'message': 'Cat updated'}


@cats_router.delete('/{cat_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_cat(
        cat_id: int,
        db: AsyncSession = Depends(get_db)
):
    await delete_cat(db, cat_id)
    return {'message': 'Cat deleted'}


async def validate_breed(breed: str) -> bool:
    url = 'https://api.thecatapi.com/v1/breeds'
    async with ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            breeds = [breed['name'].lower() for breed in data]
            if breed.lower() not in breeds:
                return False
            return True
