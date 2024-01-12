from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponent, RefDataset, RefRegion, RefRegionTo


class TransmissionLoss(RefRegionTo, RefRegion, RefComponent, RefDataset, Base):
    loss: Mapped[float]

    # table constraints
    __table_args__ = (UniqueConstraint("ref_component", "ref_region", "ref_region_to", name="_transmission_losses_regions_uc"),)
