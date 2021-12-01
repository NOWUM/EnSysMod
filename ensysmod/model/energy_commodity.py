from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergyCommodity(Base):
    id = Column(Integer, primary_key=True, index=True)
    ref_dataset = Column(Integer, ForeignKey("dataset.id"), index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    unit = Column(String, nullable=False)

    # relationships
    energy_conversions = relationship("EnergyConversion", back_populates="commodity")
    energy_sources = relationship("EnergySource", back_populates="commodity")
    energy_sinks = relationship("EnergySink", back_populates="commodity")
    energy_storages = relationship("EnergyStorage", back_populates="commodity")
    energy_transmissions = relationship("EnergyTransmission", back_populates="commodity")
