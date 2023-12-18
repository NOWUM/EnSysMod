import enum

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Session

from ensysmod.database.base_class import Base
from ensysmod.model.capacity_fix import CapacityFix
from ensysmod.model.capacity_max import CapacityMax
from ensysmod.model.capacity_min import CapacityMin
from ensysmod.model.operation_rate_fix import OperationRateFix
from ensysmod.model.operation_rate_max import OperationRateMax
from ensysmod.model.yearly_full_load_hours_max import YearlyFullLoadHoursMax
from ensysmod.model.yearly_full_load_hours_min import YearlyFullLoadHoursMin


class EnergyComponentType(enum.Enum):
    """
    Enum for the different types of energy components.
    """

    UNDEFINED = "UNDEFINED"  # Undefined component (should not be used)
    SOURCE = "SOURCE"
    SINK = "SINK"
    CONVERSION = "CONVERSION"
    TRANSMISSION = "TRANSMISSION"
    STORAGE = "STORAGE"


class CapacityVariableDomain(enum.Enum):
    """
    Enum for the different types of capacity variables.
    """

    CONTINUOUS = "CONTINUOUS"
    DISCRETE = "DISCRETE"


class EnergyComponent(Base):
    """
    EnergyComponent table definition
    Represents a abstract component in fine.
    See https://vsa-fine.readthedocs.io/en/latest/componentClassDoc.html
    """

    id = Column(Integer, primary_key=True)
    ref_dataset = Column(Integer, ForeignKey("dataset.id"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    type = Column(Enum(EnergyComponentType), index=True, nullable=False)
    description = Column(String, nullable=True)

    capacity_variable = Column(Boolean, nullable=False, default=False)
    capacity_variable_domain = Column(Enum(CapacityVariableDomain), default=CapacityVariableDomain.CONTINUOUS, nullable=False)
    capacity_per_plant_unit = Column(Integer, nullable=True, default=1.0)

    invest_per_capacity = Column(Float, nullable=False, default=0.0)
    opex_per_capacity = Column(Float, nullable=False, default=0.0)
    interest_rate = Column(Float, nullable=False, default=0.08)
    economic_lifetime = Column(Integer, nullable=False, default=10)

    shared_potential_id = Column(String, nullable=True, default=None)
    linked_quantity_id = Column(String, nullable=True, default=None)

    # table constraints
    __table_args__ = (UniqueConstraint("ref_dataset", "name", name="_commodity_name_dataset_uc"),)

    # properties
    @property
    def capacity_fix(self) -> list[CapacityFix]:
        session = Session.object_session(self)
        return session.query(CapacityFix).filter(CapacityFix.ref_component == self.id).all()

    @property
    def capacity_max(self) -> list[CapacityMax]:
        session = Session.object_session(self)
        return session.query(CapacityMax).filter(CapacityMax.ref_component == self.id).all()

    @property
    def capacity_min(self) -> list[CapacityMin]:
        session = Session.object_session(self)
        return session.query(CapacityMin).filter(CapacityMin.ref_component == self.id).all()

    @property
    def operation_rate_fix(self) -> list[OperationRateFix]:
        session = Session.object_session(self)
        return session.query(OperationRateFix).filter(OperationRateFix.ref_component == self.id).all()

    @property
    def operation_rate_max(self) -> list[OperationRateMax]:
        session = Session.object_session(self)
        return session.query(OperationRateMax).filter(OperationRateMax.ref_component == self.id).all()

    @property
    def yearly_full_load_hours_max(self) -> list[YearlyFullLoadHoursMax]:
        session = Session.object_session(self)
        return session.query(YearlyFullLoadHoursMax).filter(YearlyFullLoadHoursMax.ref_component == self.id).all()

    @property
    def yearly_full_load_hours_min(self) -> list[YearlyFullLoadHoursMin]:
        session = Session.object_session(self)
        return session.query(YearlyFullLoadHoursMin).filter(YearlyFullLoadHoursMin.ref_component == self.id).all()
