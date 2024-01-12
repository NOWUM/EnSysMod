from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import PickleType

from ensysmod.database.base_class import Base

if TYPE_CHECKING:
    from model.energy_model import EnergyModel


class EnergyModelOptimization(Base):
    ref_model: Mapped[int] = mapped_column(ForeignKey("energy_model.id"), unique=True)

    start_year: Mapped[int]
    end_year: Mapped[int | None]
    number_of_steps: Mapped[int | None]
    years_per_step: Mapped[int | None]
    CO2_reference: Mapped[float | None]
    CO2_reduction_targets: Mapped[list[float] | None] = mapped_column(PickleType)

    # relationships
    model: Mapped[EnergyModel] = relationship(back_populates="optimization_parameters")
