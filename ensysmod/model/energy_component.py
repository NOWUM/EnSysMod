from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefDataset

if TYPE_CHECKING:
    from ensysmod.model.capacity_fix import CapacityFix
    from ensysmod.model.capacity_max import CapacityMax
    from ensysmod.model.capacity_min import CapacityMin
    from ensysmod.model.energy_conversion import EnergyConversion
    from ensysmod.model.energy_sink import EnergySink
    from ensysmod.model.energy_source import EnergySource
    from ensysmod.model.energy_storage import EnergyStorage
    from ensysmod.model.energy_transmission import EnergyTransmission
    from ensysmod.model.operation_rate_fix import OperationRateFix
    from ensysmod.model.operation_rate_max import OperationRateMax
    from ensysmod.model.transmission_distance import TransmissionDistance
    from ensysmod.model.transmission_loss import TransmissionLoss
    from ensysmod.model.yearly_full_load_hours_max import YearlyFullLoadHoursMax
    from ensysmod.model.yearly_full_load_hours_min import YearlyFullLoadHoursMin


class EnergyComponentType(enum.Enum):
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

    capacity_variable: Mapped[bool]
    capacity_variable_domain: Mapped[CapacityVariableDomain]
    capacity_per_plant_unit: Mapped[float | None]

    invest_per_capacity: Mapped[float]
    opex_per_capacity: Mapped[float]
    interest_rate: Mapped[float]
    economic_lifetime: Mapped[int]

    shared_potential_id: Mapped[str | None]
    linked_quantity_id: Mapped[str | None]

    # relationships
    source: Mapped[EnergySource] = relationship(back_populates="component", cascade="all, delete-orphan")
    sink: Mapped[EnergySink] = relationship(back_populates="component", cascade="all, delete-orphan")
    conversion: Mapped[EnergyConversion] = relationship(back_populates="component", cascade="all, delete-orphan")
    storage: Mapped[EnergyStorage] = relationship(back_populates="component", cascade="all, delete-orphan")
    transmission: Mapped[EnergyTransmission] = relationship(back_populates="component", cascade="all, delete-orphan")

    capacity_fix: Mapped[list[CapacityFix]] = relationship(back_populates="component", cascade="all, delete-orphan")
    capacity_max: Mapped[list[CapacityMax]] = relationship(back_populates="component", cascade="all, delete-orphan")
    capacity_min: Mapped[list[CapacityMin]] = relationship(back_populates="component", cascade="all, delete-orphan")
    operation_rate_fix: Mapped[list[OperationRateFix]] = relationship(back_populates="component", cascade="all, delete-orphan")
    operation_rate_max: Mapped[list[OperationRateMax]] = relationship(back_populates="component", cascade="all, delete-orphan")
    yearly_full_load_hours_max: Mapped[list[YearlyFullLoadHoursMax]] = relationship(back_populates="component", cascade="all, delete-orphan")
    yearly_full_load_hours_min: Mapped[list[YearlyFullLoadHoursMin]] = relationship(back_populates="component", cascade="all, delete-orphan")
    distances: Mapped[list[TransmissionDistance]] = relationship(back_populates="component", cascade="all, delete-orphan")
    losses: Mapped[list[TransmissionLoss]] = relationship(back_populates="component", cascade="all, delete-orphan")

    # table constraints
    __table_args__ = (UniqueConstraint("ref_dataset", "name", name="_component_name_dataset_uc"),)
