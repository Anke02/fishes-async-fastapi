from fastapi import APIRouter, Depends, Path, Query, status
from typing import Any

from src.regions import services as region_services
from src.regions import dependencies as region_dependencies
from src.regions.schemas import RegionCreate, RegionList, RegionResponse, RegionUpdate


router = APIRouter(prefix="/regions", tags=["regions"])

# OK
@router.get(
    "", 
    response_model=RegionList,
    status_code=status.HTTP_200_OK,
    description="Get list of all available regions",
)
async def list_regions(
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    page: int = Query(0, ge=0, description="Page number")
) -> dict[str, Any]:
    
    return await region_services.list_regions(limit=limit, page=page)

# W trakcie
@router.post(
    "",
    response_model=RegionResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new region"
)
async def create_region(
    region_data: RegionCreate = Depends(region_dependencies.valid_region_create)
):
    return await region_services.create_region(region_data)

# OK
@router.get(
    "/{region_id}",
    response_model=RegionResponse,
    description="Get detailed information about a specific region"
)
async def get_region(
    region: dict[str, Any] = Depends(region_dependencies.valid_region_id)
):
    return region
   

# OK
@router.put(
    "/{region_id}",
    response_model=RegionResponse,
    description="Update region details"
)
async def update_region(
    region_data: RegionUpdate = Depends(region_dependencies.valid_region_update),
    region: dict[str, Any] = Depends(region_dependencies.valid_region_id)
):
    return await region_services.update_region(
        region_id=region['id'],
        region_data=region_data
    )


# OK
@router.delete(
    "/{region_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete region"
)
async def delete_region(
    region: dict[str, Any] = Depends(region_dependencies.region_not_in_use)
):
    await region_services.delete_region(region['id'])
