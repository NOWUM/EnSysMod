from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergyStorage(Base):
    """
    EnergyStorage table definition

    See https://vsa-fine.readthedocs.io/en/latest/storageClassDoc.html
    """
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, primary_key=True)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

    charge_efficiency = Column(Float, nullable=True)
    discharge_efficiency = Column(Float, nullable=True)
    self_discharge = Column(Float, nullable=True)
    cyclic_lifetime = Column(Integer, nullable=True)
    charge_rate = Column(Float, nullable=True)
    discharge_rate = Column(Float, nullable=True)
    state_of_charge_min = Column(Float, nullable=True)
    state_of_charge_max = Column(Float, nullable=True)

    # Relationships
    component = relationship("EnergyComponent")
    commodity = relationship("EnergyCommodity", back_populates="energy_storages")
