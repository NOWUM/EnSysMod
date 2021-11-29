from sqlalchemy import Column, Integer, String, ForeignKey

from ensysmod.database.base_class import Base


class EnergyConversion(Base):
    """
    EnergyConversion table definition

    Represents a conversion component in the database.
    It is used to convert one commodity to another.
    See https://vsa-fine.readthedocs.io/en/latest/conversionClassDoc.html
    """
    id = Column(Integer, primary_key=True, index=True)
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False)
    commodity_unit = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)
