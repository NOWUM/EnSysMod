from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base

if TYPE_CHECKING:
    from ensysmod.model.dataset_permission import DatasetPermission
    from ensysmod.model.energy_commodity import EnergyCommodity
    from ensysmod.model.energy_component import EnergyComponent
    from ensysmod.model.energy_conversion import EnergyConversion
    from ensysmod.model.energy_model import EnergyModel
    from ensysmod.model.energy_sink import EnergySink
    from ensysmod.model.energy_source import EnergySource
    from ensysmod.model.energy_storage import EnergyStorage
    from ensysmod.model.energy_transmission import EnergyTransmission
    from ensysmod.model.region import Region
    from ensysmod.model.user import User


class Dataset(Base):
    ref_user: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]
    hours_per_time_step: Mapped[int] = mapped_column(default=1)
    number_of_time_steps: Mapped[int] = mapped_column(default=8760)
    cost_unit: Mapped[str] = mapped_column(default="1e9 Euro")
    length_unit: Mapped[str] = mapped_column(default="km")

    # relationships
    user: Mapped[User] = relationship()
    permissions: Mapped[list[DatasetPermission]] = relationship(back_populates="dataset", cascade="all, delete-orphan")

    regions: Mapped[list[Region]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    commodities: Mapped[list[EnergyCommodity]] = relationship(back_populates="dataset", cascade="all, delete-orphan")

    components: Mapped[list[EnergyComponent]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    sources: Mapped[list[EnergySource]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    sinks: Mapped[list[EnergySink]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    conversions: Mapped[list[EnergyConversion]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    storages: Mapped[list[EnergyStorage]] = relationship(back_populates="dataset", cascade="all, delete-orphan")
    transmissions: Mapped[list[EnergyTransmission]] = relationship(back_populates="dataset", cascade="all, delete-orphan")

    models: Mapped[list[EnergyModel]] = relationship(back_populates="dataset", cascade="all, delete-orphan")

    # table constraints
    __table_args__ = (UniqueConstraint("name", "ref_user", name="_dataset_user_uc"),)
