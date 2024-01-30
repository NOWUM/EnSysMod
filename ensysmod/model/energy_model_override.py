from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponent

if TYPE_CHECKING:
    from ensysmod.model.energy_model import EnergyModel


class EnergyModelOverrideAttribute(enum.Enum):
    hasCapacityVariable = "capacity_variable"
    capacityVariableDomain = "capacity_variable_domain"
    capacityPerPlantUnit = "capacity_per_plant_unit"
    investPerCapacity = "invest_per_capacity"
    opexPerCapacity = "opex_per_capacity"
    interestRate = "interest_rate"
    economicLifetime = "economic_lifetime"
    sharedPotentialID = "shared_potential_id"
    linkedQuantityID = "linked_quantity_id"

    commodityCost = "commodity_cost"
    yearlyLimit = "yearly_limit"
    commodityLimitID = "commodity_limit_id"
    chargeEfficiency = "charge_efficiency"
    dischargeEfficiency = "discharge_efficiency"
    selfDischarge = "self_discharge"
    cyclicLifetime = "cyclic_lifetime"
    chargeRate = "charge_rate"
    dischargeRate = "discharge_rate"
    stateOfChargeMin = "state_of_charge_min"
    stateOfChargeMax = "state_of_charge_max"


class EnergyModelOverrideOperation(enum.Enum):
    add = "add"
    multiply = "multiply"
    set = "set"


class EnergyModelOverride(RefComponent, Base):
    ref_model: Mapped[int] = mapped_column(ForeignKey("energy_model.id"))

    attribute: Mapped[EnergyModelOverrideAttribute]
    operation: Mapped[EnergyModelOverrideOperation]
    value: Mapped[float]

    # relationships
    model: Mapped[EnergyModel] = relationship(back_populates="override_parameters")

    # table constraints
    __table_args__ = (UniqueConstraint("ref_model", "attribute", name="_model_attribute_uc"),)
