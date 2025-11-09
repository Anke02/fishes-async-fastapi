from fastapi import Path, Depends
from typing import Any

from src.regions import services as region_service
from src.regions import exceptions as region_exceptions
from src.regions import schemas as region_schemas


async def valid_region_id(
    region_id: int = Path(...)
) -> dict[str, Any]:

    region = await region_service.get_region_by_id(region_id)
    if not region:
        raise region_exceptions.RegionNotFound()
    return region


async def valid_region_create(
    region_data: region_schemas.RegionCreate
) -> region_schemas.RegionCreate:

    name_exists = await region_service.check_region_name_exists(
        name_pl=region_data.name_pl,
        name_en=region_data.name_en
    )
    if name_exists:
        raise region_exceptions.RegionAlreadyExists()
    return region_data


async def valid_region_update(
    region_data: region_schemas.RegionUpdate,
    existing_region: dict[str, Any] = Depends(valid_region_id)
) -> region_schemas.RegionUpdate:

    if region_data.name_pl or region_data.name_en:
        name_exists = await region_service.check_region_name_exists(
            name_pl=region_data.name_pl,
            name_en=region_data.name_en,
            exclude_id=existing_region['id']
        )
        if name_exists:
            raise region_exceptions.RegionAlreadyExists()
    
    return region_data


async def region_not_in_use(
    region: dict[str, Any] = Depends(valid_region_id)
) -> dict[str, Any]:
    
    region_in_use = await region_service.check_region_in_use(region['id'])
    if region_in_use:
        raise region_exceptions.RegionInUse()
    return region
