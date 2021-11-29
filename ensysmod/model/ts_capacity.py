from sqlalchemy import Column, DECIMAL

from ensysmod.database.base_class import Base
from ensysmod.database.base_class_timeseries import TimeSeriesBase


class Capacity(TimeSeriesBase, Base):
    quantity = Column(DECIMAL, nullable=False)
