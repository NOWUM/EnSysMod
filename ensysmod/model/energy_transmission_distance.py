from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergyTransmissionDistance(Base):
    """
    EnergyTransmission table definition

    See https://vsa-fine.readthedocs.io/en/latest/storageClassDoc.html
    """
    ref_component = Column(Integer, ForeignKey("energy_transmission.ref_component"), index=True, nullable=False,
                           primary_key=True)
    ref_region_from = Column(Integer, ForeignKey("region.id"), index=True, nullable=False)
    ref_region_to = Column(Integer, ForeignKey("region.id"), index=True, nullable=False)

    distance = Column(DECIMAL, nullable=True)

    # Relationships
    transmission = relationship("EnergyTransmission", back_populates="distances")
    region_from = relationship("Region", foreign_keys=[ref_region_from])
    region_to = relationship("Region", foreign_keys=[ref_region_to])

    # table constraints
    __table_args__ = (
        UniqueConstraint("ref_component", "ref_region_from", "ref_region_to",
                         name="_transmission_distances_regions_uc"),
    )
