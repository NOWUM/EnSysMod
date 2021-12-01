from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql.schema import ForeignKey


class TimeSeriesBase:
    """
    Base class for all time series classes.
    """

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def ref_region(self):
        return Column(Integer, ForeignKey("region.id"), index=True, nullable=False)

    @declared_attr
    def ref_component(self):
        return Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False)

    @declared_attr
    def datetime(self):
        return Column(DateTime, nullable=False)
