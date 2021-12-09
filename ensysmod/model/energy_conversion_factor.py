from sqlalchemy import Column, Integer, ForeignKey, DECIMAL

from ensysmod.database.base_class import Base


class EnergyConversionFactor(Base):
    """
    EnergyConversionFactors table

    This class is used to store the energy conversion factors for a energy conversion component.
    """
    id = Column(Integer, primary_key=True, index=True)
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)
    conversion_factor = Column(DECIMAL, nullable=False)
