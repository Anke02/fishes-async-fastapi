from fastapi import Path, Depends
from typing import Any

from src.regions import services as region_service
from src.regions.exceptions import RegionNotFound, RegionAlreadyExists, RegionInUse
from src.regions.schemas import RegionCreate, RegionUpdate


async def valid_region_id(
    region_id: int = Path(...)
) -> dict[str, Any]:

    region = await region_service.get_region_by_id(region_id)
    if not region:
        raise RegionNotFound()
    return region


async def valid_region_create(
    region_data: RegionCreate
) -> RegionCreate:

    name_exists = await region_service.check_region_name_exists(
        name_pl=region_data.name_pl,
        name_en=region_data.name_en
    )
    if name_exists:
        raise RegionAlreadyExists()
    return region_data


async def valid_region_update(
    region_data: RegionUpdate,
    existing_region: dict[str, Any] = Depends(valid_region_id)
) -> RegionUpdate:

    if region_data.name_pl or region_data.name_en:
        name_exists = await region_service.check_region_name_exists(
            name_pl=region_data.name_pl,
            name_en=region_data.name_en,
            exclude_id=existing_region['id']
        )
        if name_exists:
            raise RegionAlreadyExists()
    
    return region_data


async def region_not_in_use(
    region: dict[str, Any] = Depends(valid_region_id)
) -> dict[str, Any]:
    
    region_in_use = await region_service.check_region_in_use(region['id'])
    if region_in_use:
        raise RegionInUse()
    return region
