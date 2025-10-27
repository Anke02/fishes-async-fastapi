from src.schemas import CustomModel


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


from src.schemas import PaginationResponse


class RegionList(PaginationResponse):
    items: list[RegionResponse]