from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

if TYPE_CHECKING:
    from ensysmod.model import Dataset, EnergyCommodity, EnergyComponent, Region


class RefDataset:
    ref_dataset: Mapped[int] = mapped_column(ForeignKey("dataset.id"), index=True)

    @declared_attr
    def dataset(self) -> Mapped[Dataset]:
        return relationship()


class RefComponentUnique:
    ref_component: Mapped[int] = mapped_column(ForeignKey("energy_component.id"), index=True, unique=True)

    @declared_attr
    def component(self) -> Mapped[EnergyComponent]:
        return relationship(cascade="all, delete")


class RefComponent:
    ref_component: Mapped[int] = mapped_column(ForeignKey("energy_component.id"), index=True)

    @declared_attr
    def component(self) -> Mapped[EnergyComponent]:
        return relationship()


class RefCommodity:
    ref_commodity: Mapped[int] = mapped_column(ForeignKey("energy_commodity.id"))

    @declared_attr
    def commodity(self) -> Mapped[EnergyCommodity]:
        return relationship()


class RefRegion:
    ref_region: Mapped[int] = mapped_column(ForeignKey("region.id"))

    @declared_attr
    def region(self) -> Mapped[Region]:
        return relationship(foreign_keys=[self.ref_region])


class RefRegionTo:
    ref_region_to: Mapped[int] = mapped_column(ForeignKey("region.id"))

    @declared_attr
    def region_to(self) -> Mapped[Region]:
        return relationship(foreign_keys=[self.ref_region_to])


class RefRegionToOptional:
    ref_region_to: Mapped[int | None] = mapped_column(ForeignKey("region.id"))

    @declared_attr
    def region_to(self) -> Mapped[Region | None]:
        return relationship(foreign_keys=[self.ref_region_to])
