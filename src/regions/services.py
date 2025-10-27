from typing import Any
from sqlalchemy import delete, select, insert, func, or_
import asyncio

from src import database
from src.regions.models import regions
from src.fishes.models import fish_regions


async def list_regions(
    limit: int = 10,
    page: int = 0
) -> dict[str, Any]:

    count_query = select(func.count().label('total')).select_from(regions)
    regions_query = (
        select(regions)
        .limit(limit)
        .offset(page * limit)
        .order_by(regions.c.id)
    )
    
    count_result, items = await asyncio.gather(
        database.fetch_one(count_query),
        database.fetch_all(regions_query)
    )
    
    return {
        "items": items,
        "total": count_result['total'] if count_result else 0,
        "page": page
    }


async def get_region_by_id(
    region_id: int
) -> dict[str, Any] | None:

    query = select(regions).where(regions.c.id == region_id)
    return await database.fetch_one(query)


async def check_region_name_exists(
    name_pl: str | None = None, 
    name_en: str | None = None, 
    exclude_id: int | None = None
) -> bool:
    """Check if region with given name already exists."""
    conditions = []
    
    if name_pl:
        conditions.append(regions.c.name_pl == name_pl)
    if name_en:
        conditions.append(regions.c.name_en == name_en)
    
    if not conditions:
        return False
    
    # Use OR logic - region exists if either name matches
    query = select(regions).where(or_(*conditions))
    
    if exclude_id is not None:
        query = query.where(regions.c.id != exclude_id)
    
    existing = await database.fetch_one(query)
    return existing is not None


async def create_region(
    region_data
) -> dict[str, Any]:
    
    query = (
        insert(regions)
        .values(**region_data.model_dump())
        .returning(regions)
    )
    return await database.fetch_one(query, commit_after=True)


async def update_region(
    region_id: int, 
    region_data
) -> dict[str, Any] | None:
    """Update region with provided data (only updates fields that were explicitly set)."""
    
    query = (
        regions.update()
        .where(regions.c.id == region_id)
        .values(**region_data.model_dump(exclude_unset=True))
        .returning(regions)
    )
    
    return await database.fetch_one(query, commit_after=True)


async def check_region_in_use(region_id: int) -> bool:
    """Check if region is used in any fish_regions relationships."""
    query = select(func.count().label('count')).select_from(fish_regions).where(fish_regions.c.region_id == region_id)
    result = await database.fetch_one(query)
    return result['count'] > 0


async def delete_region(
    region_id: int
) -> None:

    query = delete(regions).where(regions.c.id == region_id)
    await database.execute(query, commit_after=True)
