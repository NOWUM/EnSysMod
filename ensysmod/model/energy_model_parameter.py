import enum

from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint, Enum
from sqlalchemy.orm import relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefCRBase


class EnergyModelParameterAttribute(enum.Enum):
    yearly_limit = 'yearly_limit'


class EnergyModelParameterOperation(enum.Enum):
    add = 'add'
    multiply = 'multiply'
    set = 'set'


class EnergyModelParameter(RefCRBase, Base):
    """
    A energy model parameter is referenced to a model and a component.

    It can be used to overwrite different attributes from the component.
    """
    ref_model = Column(Integer, ForeignKey('energy_model.id'), nullable=False)

    # The region reference is optional.
    ref_region = Column(Integer, ForeignKey('region.id'), nullable=True)

    attribute = Column(Enum(EnergyModelParameterAttribute), nullable=False)
    operation = Column(Enum(EnergyModelParameterOperation), nullable=False)
    value = Column(Float, nullable=False)

    # relationships
    component = relationship('EnergyComponent')
    model = relationship('EnergyModel', back_populates='parameters')

    # table constraints
    __table_args__ = (
        UniqueConstraint("ref_model", "attribute", name="_model_attribute_uc"),
    )
