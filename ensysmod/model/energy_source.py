from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergySource(Base):
    """
    EnergySource table definition

    See https://vsa-fine.readthedocs.io/en/latest/sourceSinkClassDoc.html
    """

    ref_component = Column(Integer, ForeignKey("energy_component.id"), index=True, nullable=False, primary_key=True)
    ref_commodity = Column(Integer, ForeignKey("energy_commodity.id"), index=True, nullable=False)

    commodity_cost = Column(Float, nullable=True)
    yearly_limit = Column(Float, nullable=True)
    commodity_limit_id = Column(String, nullable=True)

    # Relationships
    component = relationship("EnergyComponent")
    commodity = relationship("EnergyCommodity", back_populates="energy_sources")
