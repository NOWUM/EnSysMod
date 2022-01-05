from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyConversionCreate, EnergySourceCreate, EnergySinkCreate, \
    EnergyStorageCreate, EnergyTransmissionCreate
from ensysmod.schemas.energy_conversion_factor import EnergyConversionFactorCreate

schemas_with_type_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyComponentCreate, {"name": "foo", "ref_dataset": 42}),
]

schemas_with_implicit_type: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyConversionCreate, {"name": "foo", "commodity_unit": "bar", "ref_dataset": 42, "conversion_factors": [
        EnergyConversionFactorCreate(commodity="foo", conversion_factor=0.42)]}),
    (EnergySourceCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
    (EnergySinkCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
    (EnergyStorageCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
    (EnergyTransmissionCreate, {"name": "foo", "ref_dataset": 42, "commodity": "bar"}),
]

schemas_with_type = schemas_with_type_required + schemas_with_implicit_type


@pytest.mark.parametrize("schema,data", schemas_with_type_required)
def test_error_missing_type(schema: Type[BaseModel], data: Dict[str, Any]) -> None:
    """
    Test that the validator raises an error when the type is not specified.
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("type",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_implicit_type)
def test_ok_implicit_type(schema: Type[BaseModel], data: Dict[str, Any]) -> None:
    """
    Test that the validator does not raise an error when the type is specified implicit.
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_type)
def test_error_undefined_type(schema: Type[BaseModel], data: Dict[str, Any]) -> None:
    """
    Test that the validator raises an error when the type is not specified.
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(type=EnergyComponentType.UNDEFINED, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("type",)
    assert exc_info.value.errors()[0]["msg"] == "Energy component type must not be undefined."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_type)
def test_error_empty_type(schema: Type[BaseModel], data: Dict[str, Any]) -> None:
    """
    Test that the validator raises an error when the type is not specified.
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(type="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("type",)
    assert "value is not a valid enumeration member;" in exc_info.value.errors()[0]["msg"]
    assert exc_info.value.errors()[0]["type"] == "type_error.enum"
