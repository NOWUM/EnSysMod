from sqlalchemy import Column, Integer
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.sql.schema import ForeignKey


class RefCRBase:
    """
    Base class for tables referencing components and regions.
    """

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def ref_component(self):
        return Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False)

    @declared_attr
    def ref_region(self):
        return Column(Integer, ForeignKey("region.id"), index=True, nullable=False)

    @declared_attr
    def component(self):
        return relationship("EnergyComponent")

    @declared_attr
    def region(self):
        return relationship("Region")
