from fastapi import APIRouter, Depends, Query, status
from typing import Any

from src.fishes import services as fish_services
from src.fishes import dependencies as fish_dependencies
from src.fishes import schemas as fish_schemas


router = APIRouter(prefix="/fishes", tags=["fishes"])


@router.get(
    "",
    response_model=fish_schemas.FishList,
    status_code=status.HTTP_200_OK,
    description="Get list of all fishes"
)
async def list_fishes(
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    page: int = Query(0, ge=0, description="Page number (0-based)")
):
    return await fish_services.list_fishes(size=size, page=page)


@router.post(
    "",
    response_model=fish_schemas.FishResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new fish"
)
async def create_fish(
    fish_data: fish_schemas.FishCreate = Depends(fish_dependencies.valid_fish_create)
):
    return await fish_services.create_fish(fish_data)


@router.get(
    "/{fish_id}",
    response_model=fish_schemas.FishResponse,
    status_code=status.HTTP_200_OK,
    description="Get detailed information about a specific fish"
)
async def get_fish_by_id(
    fish: dict[str, Any] = Depends(fish_dependencies.valid_fish_id)
):
    return fish


@router.put(
    "/{fish_id}",
    response_model=fish_schemas.FishResponse,
    status_code=status.HTTP_200_OK,
    description="Update fish details"
)
async def update_fish(
    update_data: fish_schemas.FishUpdate = Depends(fish_dependencies.valid_fish_update),
    fish: dict[str, Any] = Depends(fish_dependencies.valid_fish_id)
):
    return await fish_services.update_fish(fish['id'], update_data)


@router.delete(
    "/{fish_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete fish"
)
async def delete_fish(
    fish: dict[str, Any] = Depends(fish_dependencies.valid_fish_id)
):
    await fish_services.delete_fish(fish['id'])


@router.get(
    "/{fish_id}/regions",
    response_model=list[fish_schemas.FishRegionResponse],
    status_code=status.HTTP_200_OK,
    description="Get all regions where fish occurs"
)
async def get_fish_regions(
    fish: dict[str, Any] = Depends(fish_dependencies.valid_fish_id)
):
    return await fish_services.get_fish_regions(fish['id'])


@router.post(
    "/{fish_id}/regions/{region_id}",
    response_model=fish_schemas.FishRegionResponse,
    status_code=status.HTTP_201_CREATED,
    description="Assign a region to a fish"
)
async def add_fish_region(
    validated: dict[str, Any] = Depends(fish_dependencies.valid_fish_region_create)
):
    return await fish_services.create_fish_region(
        validated['fish']['id'], 
        validated['region']['id']
    )


@router.delete(
    "/{fish_id}/regions/{region_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove region assignment from fish")
async def remove_fish_region(
    validated: dict[str, Any] = Depends(fish_dependencies.valid_fish_region_delete)
):
    await fish_services.remove_fish_region(validated['fish']['id'], validated['region']['id'])



