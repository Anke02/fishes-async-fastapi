import asyncio
from typing import Any
from sqlalchemy import delete, select, insert, func

from src import database
from src.fishes.models import fishes, fish_regions


async def get_fish_by_id(
    fish_id: int
) -> dict[str, Any]:

    query = (
        select(fishes)
        .where(fishes.c.id == fish_id)
    )
    return await database.fetch_one(query)
        

async def get_fish_by_scientific_name(
    name_scientific: str
) -> dict[str, Any] | None:

    query = (
        select(fishes)
        .where(fishes.c.name_scientific == name_scientific)
    )
    return await database.fetch_one(query)


async def create_fish(
    fish_data: dict[str, Any]
) -> dict[str, Any]:
    query = (
        insert(fishes)
        .values(**fish_data)
        .returning(fishes)
    )
    return await database.fetch_one(query, commit_after=True)


async def list_fishes(
    size: int = 10,
    page: int = 0,
) -> dict[str, Any]:

    count_query = select(func.count().label('total')).select_from(fishes)
    fishes_query = (
        select(fishes)
        .limit(size)
        .offset(page * size)
        .order_by(fishes.c.id)
    )
    
    count_result, items = await asyncio.gather(
        database.fetch_one(count_query),
        database.fetch_all(fishes_query)
    )
    
    return {
        "items": items,
        "total": count_result['total'] if count_result else 0,
        "page": page
    }


async def update_fish(
    fish_id: int, 
    fish_data: dict[str, Any]
) -> dict[str, Any]:
    
    query = (
        fishes.update()
        .where(fishes.c.id == fish_id)
        .values(**fish_data)
        .returning(fishes)
    )
    return await database.fetch_one(query, commit_after=True)  


async def delete_fish(
    fish_id: int
) -> None:

    async with database.transaction() as connection:
        await database.execute(
            delete(fish_regions).where(fish_regions.c.fish_id == fish_id),
            connection=connection
        )
        
        await database.execute(
            delete(fishes).where(fishes.c.id == fish_id),
            connection=connection
        )   


async def get_fish_regions(
    fish_id: int
) -> list[dict[str, Any]]:

    query = (
        select(fish_regions)
        .where(fish_regions.c.fish_id == fish_id)
    )
    return await database.fetch_all(query)


async def get_fish_region(
    fish_id: int,
    region_id: int
) -> dict[str, Any] | None:

    query = (
        select(fish_regions)
        .where(
            fish_regions.c.fish_id == fish_id,
            fish_regions.c.region_id == region_id
        )
    )
    return await database.fetch_one(query)


async def create_fish_region(
    fish_id: int, 
    region_id: int
) -> dict[str, Any]:

    query = (
        insert(fish_regions)
        .values(
            fish_id=fish_id,
            region_id=region_id
        )
        .returning(fish_regions)
    )
    return await database.fetch_one(query, commit_after=True)


async def remove_fish_region(
    fish_id: int, 
    region_id: int
) -> None:

    await database.execute(
        delete(fish_regions).where(
            fish_regions.c.fish_id == fish_id,
            fish_regions.c.region_id == region_id
        ),
        commit_after=True
    )