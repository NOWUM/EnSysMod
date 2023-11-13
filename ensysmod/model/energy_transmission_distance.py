from sqlalchemy import Column, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base


class EnergyTransmissionDistance(Base):
    """
    EnergyTransmissionDistance table definition

    See https://vsa-fine.readthedocs.io/en/master/sourceCodeDocumentation/components/transmissionClassDoc.html
    """

    id = Column(Integer, primary_key=True)
    ref_component = Column(Integer, ForeignKey("energy_transmission.ref_component"), index=True, nullable=False)
    ref_region = Column(Integer, ForeignKey("region.id"), index=True, nullable=False)
    ref_region_to = Column(Integer, ForeignKey("region.id"), index=True, nullable=False)

    distance = Column(Float, nullable=True)

    # Relationships
    transmission = relationship("EnergyTransmission", back_populates="distances")
    region = relationship("Region", foreign_keys=[ref_region])
    region_to = relationship("Region", foreign_keys=[ref_region_to])

    # table constraints
    __table_args__ = (UniqueConstraint("ref_component", "ref_region", "ref_region_to", name="_transmission_distances_regions_uc"),)
