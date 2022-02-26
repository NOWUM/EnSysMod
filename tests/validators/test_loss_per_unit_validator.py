from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_transmission import EnergyTransmissionCreate, EnergyTransmissionUpdate

schemas_with_loss_per_unit_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_loss_per_unit_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyTransmissionUpdate, {}),
    (EnergyTransmissionCreate,
     {"name": "test", "ref_dataset": 42, "type": EnergyComponentType.TRANSMISSION, "commodity": "bar"})
]

schemas_with_loss_per_unit = schemas_with_loss_per_unit_required + schemas_with_loss_per_unit_optional


@pytest.mark.parametrize("schema,data", schemas_with_loss_per_unit_optional)
def test_ok_missing_loss_per_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss per unit is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_loss_per_unit_optional)
def test_ok_none_loss_per_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss per unit is optional for a schema
    """
    schema(loss_per_unit=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_loss_per_unit)
def test_error_on_negative_loss_per_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss per unit is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(loss_per_unit=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss_per_unit",)
    assert exc_info.value.errors()[0]["msg"] == "The loss per unit must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_loss_per_unit)
def test_error_on_positive_loss_per_unit(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss per unit is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(loss_per_unit=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss_per_unit",)
    assert exc_info.value.errors()[0]["msg"] == "The loss per unit must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_loss_per_unit)
def test_ok_loss_per_units(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss per unit with everything over 0 is valid
    """
    schema(loss_per_unit=0, **data)
    schema(loss_per_unit=0.5, **data)
    schema(loss_per_unit=1, **data)
