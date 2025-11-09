from src.schemas import CustomModel, PaginationResponse


class FishBase(CustomModel):
    name_pl: str
    name_en: str
    name_scientific: str


class FishCreate(FishBase):
    pass


class FishUpdate(CustomModel):
    name_pl: str | None = None          
    name_en: str | None = None
    name_scientific: str | None = None


class FishResponse(FishBase):
    id: int


class FishList(PaginationResponse):
    items: list[FishResponse]


class FishRegionBase(CustomModel):
    region_id: int


class FishRegionCreate(FishRegionBase):
    pass


class FishRegionResponse(FishRegionBase):
    id: int
    fish_id: int