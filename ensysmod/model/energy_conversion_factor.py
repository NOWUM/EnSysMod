from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCommodity

if TYPE_CHECKING:
    from model.energy_conversion import EnergyConversion


class EnergyConversionFactor(RefCommodity, Base):
    ref_component: Mapped[int] = mapped_column(ForeignKey("energy_conversion.ref_component"))
    conversion_factor: Mapped[float]

    # relationships
    conversion: Mapped[EnergyConversion] = relationship(back_populates="conversion_factors")

    # table constraints
    __table_args__ = (UniqueConstraint("ref_component", "ref_commodity", name="_conversion_factors_component_commodity_uc"),)
