from pydantic import BaseModel, ConfigDict


class CustomModel(BaseModel):    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class PaginationResponse(CustomModel):
    total: int = 0
    page: int = 0