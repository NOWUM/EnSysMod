import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


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


class EnergyModelOverride(RefCRBase, Base):
    """
    A energy model parameter is referenced to a model and a component.

    It can be used to overwrite different attributes from the component.
    """

    ref_model = Column(Integer, ForeignKey("energy_model.id"), nullable=False)

    # The region reference is optional.
    ref_region = Column(Integer, ForeignKey("region.id"), nullable=True)

    attribute = Column(Enum(EnergyModelOverrideAttribute), nullable=False)
    operation = Column(Enum(EnergyModelOverrideOperation), nullable=False)
    value = Column(Float, nullable=False)

    # relationships
    component = relationship("EnergyComponent")
    model = relationship("EnergyModel", back_populates="override_parameters")

    # table constraints
    __table_args__ = (UniqueConstraint("ref_model", "attribute", name="_model_attribute_uc"),)
