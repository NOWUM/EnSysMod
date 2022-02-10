from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergyTransmission(Base):
    """
    EnergyTransmission table definition

    See https://vsa-fine.readthedocs.io/en/latest/storageClassDoc.html
    """
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, primary_key=True)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

    loss_per_unit = Column(Float, nullable=True)

    # Relationships
    component = relationship("EnergyComponent")
    commodity = relationship("EnergyCommodity", back_populates="energy_transmissions")

    distances = relationship("EnergyTransmissionDistance", back_populates="transmission")
