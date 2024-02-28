from sqlalchemy.orm import Mapped

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponent, RefDataset, RefRegion, RefRegionToOptional


class CapacityMax(RefRegionToOptional, RefRegion, RefComponent, RefDataset, Base):
    capacity_max: Mapped[float]
