from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergySource(Base):
    """
    EnergySource table definition

    See https://vsa-fine.readthedocs.io/en/latest/sourceSinkClassDoc.html
    """
    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, primary_key=True)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

    # Relationships
    component = relationship("EnergyComponent")
    commodity = relationship("EnergyCommodity", back_populates="energy_sources")
