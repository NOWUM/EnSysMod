from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponent, RefDataset, RefRegion, RefRegionTo


class TransmissionDistance(RefRegionTo, RefRegion, RefComponent, RefDataset, Base):
    distance: Mapped[float]

    # table constraints
    __table_args__ = (UniqueConstraint("ref_component", "ref_region", "ref_region_to", name="_transmission_distances_regions_uc"),)
