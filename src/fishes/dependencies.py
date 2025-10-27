from fastapi import Depends, Path
from typing import Any

from src.fishes import services as fish_service
from src.fishes.exceptions import FishNotFound, DuplicateScientificName, FishRegionAlreadyExists, FishRegionNotFound
from src.fishes.schemas import FishCreate, FishUpdate
from src.regions import dependencies as region_dependencies


async def valid_fish_id(
    fish_id: int = Path(..., description="The ID of the fish")
) -> dict[str, Any]:
    
    fish = await fish_service.get_fish_by_id(fish_id)
    if not fish:
        raise FishNotFound()
    return fish


async def verify_scientific_name(
    name: str, 
    exclude_fish_id: int | None = None
) -> None:

    if not name:
        return
        
    existing = await fish_service.get_fish_by_scientific_name(name)
    if existing and (exclude_fish_id is None or existing['id'] != exclude_fish_id):
        raise DuplicateScientificName()


async def valid_fish_create(
    fish_data: FishCreate
) -> FishCreate:

    await verify_scientific_name(fish_data.name_scientific)
    return fish_data


async def valid_fish_update(
    fish_data: FishUpdate,
    existing_fish: dict[str, Any] = Depends(valid_fish_id)
) -> FishUpdate:

    await verify_scientific_name(fish_data.name_scientific, exclude_fish_id=existing_fish['id'])
    return fish_data


async def valid_fish_region_create(
    fish: dict[str, Any] = Depends(valid_fish_id),
    region: dict[str, Any] = Depends(region_dependencies.valid_region_id)
) -> dict[str, Any]:

    existing = await fish_service.get_fish_region(fish['id'], region['id'])
    if existing:
        raise FishRegionAlreadyExists()
    
    return {"fish": fish, "region": region}


async def valid_fish_region_delete(
    fish: dict[str, Any] = Depends(valid_fish_id),
    region: dict[str, Any] = Depends(region_dependencies.valid_region_id)
) -> dict[str, Any]:

    existing = await fish_service.get_fish_region(fish['id'], region['id'])
    if not existing:
        raise FishRegionNotFound()
    
    return {"fish": fish, "region": region}
