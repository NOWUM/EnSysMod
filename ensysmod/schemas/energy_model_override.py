from typing import Optional

from pydantic import BaseModel, Field

from ensysmod.model.energy_model_override import (
    EnergyModelOverrideAttribute,
    EnergyModelOverrideOperation,
)
from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)
from ensysmod.schemas.region import Region


class EnergyModelOverrideBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a model parameter override. Used as a base class for all schemas.
    """
    attribute: EnergyModelOverrideAttribute = Field(..., description="The attribute of the parameter.",
                                                     example=EnergyModelOverrideAttribute.yearly_limit)
    operation: EnergyModelOverrideOperation = Field(..., description="The operation of the parameter.",
                                                     example=EnergyModelOverrideOperation.add)
    value: float = Field(..., description="The value of the parameter.", example=-5.5)


class EnergyModelOverrideCreate(EnergyModelOverrideBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a model parameter override.

    ref_model and ref_dataset are overridden on create.

    Region is optional.
   . """
    ref_model: Optional[int] = None
    ref_dataset: Optional[int] = None
    region: Optional[str] = None


class EnergyModelOverrideUpdate(EnergyModelOverrideBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a model parameter override.
    """
    attribute: Optional[EnergyModelOverrideAttribute] = None
    operation: Optional[EnergyModelOverrideOperation] = None
    value: Optional[float] = None


class EnergyModelOverride(EnergyModelOverrideBase, RefCRBase):
    """
    Attributes to return via API for a model parameter override.
    """
    id: int

    # Region is optional.
    region: Optional[Region] = None

    class Config:
        orm_mode = True
