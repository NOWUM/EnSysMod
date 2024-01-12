from sqlalchemy.orm import Mapped

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCommodity, RefComponentUnique, RefDataset


class EnergyStorage(RefCommodity, RefComponentUnique, RefDataset, Base):
    charge_efficiency: Mapped[float | None]
    discharge_efficiency: Mapped[float | None]
    self_discharge: Mapped[float | None]
    cyclic_lifetime: Mapped[int | None]
    charge_rate: Mapped[float | None]
    discharge_rate: Mapped[float | None]
    state_of_charge_min: Mapped[float | None]
    state_of_charge_max: Mapped[float | None]
