from typing import Optional

from pydantic import BaseModel, Field

from ensysmod.model.energy_model_parameter import EnergyModelParameterAttribute, EnergyModelParameterOperation
from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.schemas.region import Region


class EnergyModelParameterBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a model parameter. Used as a base class for all schemas.
    """
    attribute: EnergyModelParameterAttribute = Field(..., description="The attribute of the parameter.",
                                                     example=EnergyModelParameterAttribute.yearly_limit)
    operation: EnergyModelParameterOperation = Field(..., description="The operation of the parameter.",
                                                     example=EnergyModelParameterOperation.add)
    value: float = Field(..., description="The value of the parameter.", example=-5.5)


class EnergyModelParameterCreate(EnergyModelParameterBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a model parameter.

    ref_model and ref_dataset are overridden on create.

    Region is optional.
   . """
    ref_model: Optional[int] = None
    ref_dataset: Optional[int] = None
    region: Optional[str] = None


class EnergyModelParameterUpdate(EnergyModelParameterBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a model parameter.
    """
    attribute: Optional[EnergyModelParameterAttribute] = None
    operation: Optional[EnergyModelParameterOperation] = None
    value: Optional[float] = None


class EnergyModelParameter(EnergyModelParameterBase, RefCRBase):
    """
    Attributes to return via API for a model parameter.
    """
    id: int

    # Region is optional.
    region: Optional[Region] = None

    class Config:
        orm_mode = True
