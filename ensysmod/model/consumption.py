from sqlalchemy import Column, Integer
from sqlalchemy.sql.schema import ForeignKey
from ensysmod.database.base_class import Base


class Consumption(Base):
    id = Column(Integer, primary_key=True, index=True)
    ref_region = Column(Integer, ForeignKey("region.id"), index=True, nullable=False)
    ref_source = Column(Integer, ForeignKey("energysource.id"), index=True, nullable=False)
    ref_sink = Column(Integer, ForeignKey("energysink.id"), index=True, nullable=False)
    year = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
