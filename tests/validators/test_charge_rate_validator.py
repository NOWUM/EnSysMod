from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_storage import EnergyStorageCreate, EnergyStorageUpdate

schemas_with_charge_rate_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_charge_rate_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyStorageUpdate, {}),
    (EnergyStorageCreate,
     {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.STORAGE, "commodity": "bar"})
]

schemas_with_charge_rate = schemas_with_charge_rate_required + schemas_with_charge_rate_optional


@pytest.mark.parametrize("schema,data", schemas_with_charge_rate_optional)
def test_ok_missing_charge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a charge rate is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_charge_rate_optional)
def test_ok_none_charge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a charge rate is optional for a schema
    """
    schema(charge_rate=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_charge_rate)
def test_error_on_negative_charge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a charge rate is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(charge_rate=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("charge_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Charge rate must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_charge_rate)
def test_error_on_positive_charge_rate(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a charge rate is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(charge_rate=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("charge_rate",)
    assert exc_info.value.errors()[0]["msg"] == "Charge rate must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_charge_rate)
def test_ok_charge_rates(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a charge rate with everything between 0 and 1 is valid
    """
    schema(charge_rate=0, **data)
    schema(charge_rate=0.5, **data)
    schema(charge_rate=1, **data)
