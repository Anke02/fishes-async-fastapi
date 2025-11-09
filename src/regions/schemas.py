from src.schemas import CustomModel, PaginationResponse


class RegionBase(CustomModel):
    name_pl: str
    name_en: str


class RegionCreate(RegionBase):
    pass


class RegionUpdate(RegionBase):
    name_pl: str | None = None
    name_en: str | None = None


class RegionResponse(RegionBase):
    id: int


class RegionList(PaginationResponse):
    items: list[RegionResponse]