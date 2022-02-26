from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_storage import EnergyStorageCreate, EnergyStorageUpdate

schemas_with_self_discharge_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_self_discharge_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyStorageUpdate, {}),
    (EnergyStorageCreate,
     {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.STORAGE, "commodity": "bar"})
]

schemas_with_self_discharge = schemas_with_self_discharge_required + schemas_with_self_discharge_optional


@pytest.mark.parametrize("schema,data", schemas_with_self_discharge_optional)
def test_ok_missing_self_discharge(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a self discharge is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_self_discharge_optional)
def test_ok_none_self_discharge(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a self discharge is optional for a schema
    """
    schema(self_discharge=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_self_discharge)
def test_error_on_negative_self_discharge(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a self discharge is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(self_discharge=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("self_discharge",)
    assert exc_info.value.errors()[0]["msg"] == "Self discharge must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_self_discharge)
def test_error_on_positive_self_discharge(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a self discharge is not over 1
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(self_discharge=1.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("self_discharge",)
    assert exc_info.value.errors()[0]["msg"] == "Self discharge must be between 0 and 1."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_self_discharge)
def test_ok_self_discharge(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a self discharge with everything between 0 and 1 is valid
    """
    schema(self_discharge=0, **data)
    schema(self_discharge=0.5, **data)
    schema(self_discharge=1, **data)
