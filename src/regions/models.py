from src.database import metadata
from sqlalchemy import Column, Integer, String, Table


regions = Table(
    "regions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name_pl", String(100), unique=True, nullable=False),
    Column("name_en", String(100), unique=True, nullable=False),
)