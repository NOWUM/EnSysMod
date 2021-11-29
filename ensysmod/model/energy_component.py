import enum

from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, Enum

from ensysmod.database.base_class import Base


class EnergyComponentType(enum.Enum):
    """
    Enum for the different types of energy components.
    """
    SOURCE = 'source'
    SINK = 'sink'
    CONVERSION = 'conversion'
    TRANSMISSION = 'transmission'
    STORAGE = 'storage'


class CapacityVariableDomain(enum.Enum):
    """
    Enum for the different types of capacity variables.
    """
    CONTINUOUS = 'continuous'
    DISCRETE = 'discrete'


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
    capacity_variable = Column(Boolean, nullable=False)
    capacity_variable_domain = Column(Enum(CapacityVariableDomain),
                                      default=CapacityVariableDomain.CONTINUOUS,
                                      nullable=False)
    capacity_per_plant_unit = Column(DECIMAL, nullable=True, default=1.0)

    invest_per_capacity = Column(DECIMAL, nullable=False, default=0.0)
    opex_per_capacity = Column(DECIMAL, nullable=False, default=0.0)
    interest_rate = Column(DECIMAL, nullable=False, default=0.08)
    economic_lifetime = Column(Integer, nullable=False, default=10)

    # Relationships

    # constraint capacityVariableDomain
