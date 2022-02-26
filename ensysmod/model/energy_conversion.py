from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base
from ensysmod.model.energy_conversion_factor import EnergyConversionFactor


class EnergyConversion(Base):
    """
    EnergyConversion table definition

    Represents a conversion component in the database.
    It is used to convert one commodity to another.
    See https://vsa-fine.readthedocs.io/en/latest/conversionClassDoc.html
    """
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, primary_key=True)
    ref_commodity_unit = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

    # Relationships
    component = relationship("EnergyComponent")
    commodity_unit = relationship("EnergyCommodity", back_populates="energy_conversions")
    conversion_factors: List[EnergyConversionFactor] = relationship("EnergyConversionFactor",
                                                                    back_populates="conversion")
