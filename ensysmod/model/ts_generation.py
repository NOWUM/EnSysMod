from sqlalchemy import Column, DECIMAL

from ensysmod.database.base_class import Base
from ensysmod.database.ts_base_class import TimeSeriesBase


class Generation(TimeSeriesBase, Base):
    quantity = Column(DECIMAL, nullable=False)
