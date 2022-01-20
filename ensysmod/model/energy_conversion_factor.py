from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Float
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base
from ensysmod.model.energy_commodity import EnergyCommodity


class EnergyConversionFactor(Base):
    """
    EnergyConversionFactors table

    This class is used to store the energy conversion factors for a energy conversion component.
    """
    id = Column(Integer, primary_key=True, index=True)
    ref_component = Column(Integer, ForeignKey("energy_conversion.ref_component"), index=True, nullable=False)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)
    conversion_factor = Column(Float, nullable=False)

    # Relationships
    conversion = relationship("EnergyConversion", back_populates="conversion_factors")
    commodity: EnergyCommodity = relationship("EnergyCommodity")

    # table constraints
    __table_args__ = (
        UniqueConstraint("ref_component", "ref_commodity", name="_conversion_factors_component_commodity_uc"),
    )
