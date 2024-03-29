from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyStorageCreate, EnergyStorageUpdate

schemas_with_cyclic_lifetime_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_cyclic_lifetime_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyStorageUpdate, {}),
    (EnergyStorageCreate, {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.STORAGE, "commodity_name": "bar"}),
]

schemas_with_cyclic_lifetime = schemas_with_cyclic_lifetime_required + schemas_with_cyclic_lifetime_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_cyclic_lifetime_optional)
def test_ok_missing_cyclic_lifetime(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a cyclic lifetime is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_cyclic_lifetime_optional)
def test_ok_none_cyclic_lifetime(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a cyclic lifetime is optional for a schema
    """
    schema(cyclic_lifetime=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_cyclic_lifetime)
def test_error_on_negative_cyclic_lifetime(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a cyclic lifetime is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(cyclic_lifetime=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("cyclic_lifetime",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than"


@pytest.mark.parametrize(("schema", "data"), schemas_with_cyclic_lifetime)
def test_error_on_zero_cyclic_lifetime(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a cyclic lifetime is not 0
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(cyclic_lifetime=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("cyclic_lifetime",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than"


@pytest.mark.parametrize(("schema", "data"), schemas_with_cyclic_lifetime)
def test_ok_cyclic_lifetimes(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a cyclic lifetime with everything over 0 is valid
    """
    schema(cyclic_lifetime=1, **data)
    schema(cyclic_lifetime=100, **data)
