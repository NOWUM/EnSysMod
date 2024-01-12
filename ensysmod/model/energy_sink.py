from sqlalchemy.orm import Mapped

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCommodity, RefComponentUnique, RefDataset


class EnergySink(RefCommodity, RefComponentUnique, RefDataset, Base):
    commodity_cost: Mapped[float | None]
    yearly_limit: Mapped[float | None]
    commodity_limit_id: Mapped[str | None]
