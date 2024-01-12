from sqlalchemy.orm import Mapped

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponent, RefDataset, RefRegion, RefRegionToOptional


class YearlyFullLoadHoursMax(RefRegionToOptional, RefRegion, RefComponent, RefDataset, Base):
    yearly_full_load_hours_max: Mapped[float]
