from sqlalchemy import Column, Float, ForeignKey, Integer, UniqueConstraint

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class TransmissionDistance(RefCRBase, Base):
    distance = Column(Float, nullable=False)
    ref_region_to = Column(Integer, ForeignKey("region.id"), index=True, nullable=False)

    # table constraints
    __table_args__ = (UniqueConstraint("ref_component", "ref_region", "ref_region_to", name="_transmission_distances_regions_uc"),)
