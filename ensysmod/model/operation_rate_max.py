from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import PickleType

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponent, RefDataset, RefRegion, RefRegionToOptional


class OperationRateMax(RefRegionToOptional, RefRegion, RefComponent, RefDataset, Base):
    operation_rate_max: Mapped[list[float]] = mapped_column(PickleType)
