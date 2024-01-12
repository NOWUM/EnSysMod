from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefDataset

if TYPE_CHECKING:
    from model.capacity_fix import CapacityFix
    from model.capacity_max import CapacityMax
    from model.capacity_min import CapacityMin
    from model.operation_rate_fix import OperationRateFix
    from model.operation_rate_max import OperationRateMax
    from model.transmission_distance import TransmissionDistance
    from model.transmission_loss import TransmissionLoss
    from model.yearly_full_load_hours_max import YearlyFullLoadHoursMax
    from model.yearly_full_load_hours_min import YearlyFullLoadHoursMin


class EnergyComponentType(enum.Enum):
    UNDEFINED = "UNDEFINED"  # Undefined component (should not be used)
    SOURCE = "SOURCE"
    SINK = "SINK"
    CONVERSION = "CONVERSION"
    TRANSMISSION = "TRANSMISSION"
    STORAGE = "STORAGE"


class CapacityVariableDomain(enum.Enum):
    CONTINUOUS = "CONTINUOUS"
    DISCRETE = "DISCRETE"


class EnergyComponent(RefDataset, Base):
    name: Mapped[str] = mapped_column(index=True)
    type: Mapped[EnergyComponentType]
    description: Mapped[str | None]

    capacity_variable: Mapped[bool] = mapped_column(default=False)
    capacity_variable_domain: Mapped[CapacityVariableDomain] = mapped_column(default=CapacityVariableDomain.CONTINUOUS)
    capacity_per_plant_unit: Mapped[float | None] = mapped_column(default=1.0)

    invest_per_capacity: Mapped[float] = mapped_column(default=0.0)
    opex_per_capacity: Mapped[float] = mapped_column(default=0.0)
    interest_rate: Mapped[float] = mapped_column(default=0.08)
    economic_lifetime: Mapped[int] = mapped_column(default=10)

    shared_potential_id: Mapped[str | None]
    linked_quantity_id: Mapped[str | None]

    # relationships
    capacity_fix: Mapped[list[CapacityFix]] = relationship(back_populates="component")
    capacity_max: Mapped[list[CapacityMax]] = relationship(back_populates="component")
    capacity_min: Mapped[list[CapacityMin]] = relationship(back_populates="component")
    operation_rate_fix: Mapped[list[OperationRateFix]] = relationship(back_populates="component")
    operation_rate_max: Mapped[list[OperationRateMax]] = relationship(back_populates="component")
    yearly_full_load_hours_max: Mapped[list[YearlyFullLoadHoursMax]] = relationship(back_populates="component")
    yearly_full_load_hours_min: Mapped[list[YearlyFullLoadHoursMin]] = relationship(back_populates="component")
    distances: Mapped[list[TransmissionDistance]] = relationship(back_populates="component")
    losses: Mapped[list[TransmissionLoss]] = relationship(back_populates="component")

    # table constraints
    __table_args__ = (UniqueConstraint("ref_dataset", "name", name="_component_name_dataset_uc"),)
