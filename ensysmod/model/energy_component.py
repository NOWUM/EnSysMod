import enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, UniqueConstraint, Float

from ensysmod.database.base_class import Base


class EnergyComponentType(enum.Enum):
    """
    Enum for the different types of energy components.
    """
    UNDEFINED = 'UNDEFINED'  # Undefined component (should not be used)
    SOURCE = 'SOURCE'
    SINK = 'SINK'
    CONVERSION = 'CONVERSION'
    TRANSMISSION = 'TRANSMISSION'
    STORAGE = 'STORAGE'


class CapacityVariableDomain(enum.Enum):
    """
    Enum for the different types of capacity variables.
    """
    CONTINUOUS = 'CONTINUOUS'
    DISCRETE = 'DISCRETE'


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

    # specifies if the component should be modeled with a capacity or not.
    capacity_variable = Column(Boolean, nullable=False, default=False)
    capacity_variable_domain = Column(Enum(CapacityVariableDomain),
                                      default=CapacityVariableDomain.CONTINUOUS,
                                      nullable=False)
    capacity_per_plant_unit = Column(Integer, nullable=True, default=1.0)

    invest_per_capacity = Column(Float, nullable=False, default=0.0)
    opex_per_capacity = Column(Float, nullable=False, default=0.0)
    interest_rate = Column(Float, nullable=False, default=0.08)
    economic_lifetime = Column(Integer, nullable=False, default=10)

    shared_potential_id = Column(String, nullable=True)

    # constraint capacityVariableDomain

    # table constraints
    __table_args__ = (
        UniqueConstraint("ref_dataset", "name", name="_commodity_name_dataset_uc"),
    )
