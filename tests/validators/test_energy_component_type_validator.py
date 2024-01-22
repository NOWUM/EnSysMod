from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import (
    EnergyComponentCreate,
    EnergyConversionCreate,
    EnergySinkCreate,
    EnergySourceCreate,
    EnergyStorageCreate,
    EnergyTransmissionCreate,
)
from ensysmod.schemas.energy_conversion_factor import EnergyConversionFactorCreate

schemas_with_type_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyComponentCreate, {"name": "foo", "ref_dataset": 42}),
]

schemas_with_implicit_type: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (
        EnergyConversionCreate,
        {
            "name": "foo",
            "commodity_unit": "bar",
            "ref_dataset": 42,
            "conversion_factors": [EnergyConversionFactorCreate(commodity="foo", conversion_factor=0.42)],
        },
    ),
    (EnergySourceCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
    (EnergySinkCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
    (EnergyStorageCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
    (EnergyTransmissionCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
]

schemas_with_type = schemas_with_type_required + schemas_with_implicit_type


@pytest.mark.parametrize(("schema", "data"), schemas_with_type_required)
def test_error_missing_type(schema: type[BaseModel], data: dict[str, Any]) -> None:
    """
    Test that the validator raises an error when the type is not specified.
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("type",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_implicit_type)
def test_ok_implicit_type(schema: type[BaseModel], data: dict[str, Any]) -> None:
    """
    Test that the validator does not raise an error when the type is specified implicit.
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_type)
def test_error_undefined_type(schema: type[BaseModel], data: dict[str, Any]) -> None:
    """
    Test that the validator raises an error when the type is not specified.
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(type=EnergyComponentType.UNDEFINED, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("type",)
    assert exc_info.value.errors()[0]["msg"] == "Value error, Energy component type must not be undefined."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_type)
def test_error_empty_type(schema: type[BaseModel], data: dict[str, Any]) -> None:
    """
    Test that the validator raises an error when the type is not specified.
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(type="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("type",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be 'UNDEFINED', 'SOURCE', 'SINK', 'CONVERSION', 'TRANSMISSION' or 'STORAGE'"
    assert exc_info.value.errors()[0]["type"] == "enum"
