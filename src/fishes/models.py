from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String

from src.database import metadata


fishes = Table(
    "fishes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_pl", String(100), nullable=False),
    Column("name_en", String(100)),
    Column("name_scientific", String(100), unique=True, nullable=False),
)


fish_regions = Table(
    "fish_regions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("fish_id", Integer, ForeignKey("fishes.id"), nullable=False),
    Column("region_id", Integer, ForeignKey("regions.id"), nullable=False)
)