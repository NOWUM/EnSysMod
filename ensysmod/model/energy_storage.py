from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergyStorage(Base):
    """
    EnergyStorage table definition

    See https://vsa-fine.readthedocs.io/en/latest/storageClassDoc.html
    """
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, primary_key=True)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

    charge_efficiency = Column(DECIMAL, nullable=True)
    discharge_efficiency = Column(DECIMAL, nullable=True)
    self_discharge = Column(DECIMAL, nullable=True)
    cyclic_lifetime = Column(Integer, nullable=True)
    charge_rate = Column(DECIMAL, nullable=True)
    discharge_rate = Column(DECIMAL, nullable=True)
    state_of_charge_min = Column(DECIMAL, nullable=True)
    state_of_charge_max = Column(DECIMAL, nullable=True)

    # Relationships
    component = relationship("EnergyComponent")
    commodity = relationship("EnergyCommodity", back_populates="energy_storages")
