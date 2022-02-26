from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyConversionFactorCreate
from ensysmod.schemas.energy_conversion import EnergyConversionCreate

schemas_with_commodity_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyConversionCreate, {"name": "foo", "ref_dataset": 42, "conversion_factors": [
        EnergyConversionFactorCreate(commodity="bar", conversion_factor=0.42)]})
]

schemas_with_commodity_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
]

schemas_with_commodity = schemas_with_commodity_required + schemas_with_commodity_optional


@pytest.mark.parametrize("schema,data", schemas_with_commodity_required)
def test_error_missing_commodity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a commodity is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity_unit",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_commodity_optional)
def test_ok_missing_commodity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a commodity is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_commodity)
def test_error_empty_commodity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a commodity is not empty, if specified
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(commodity_unit="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity_unit",)
    assert exc_info.value.errors()[0]["msg"] == "Commodity must not be empty."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_commodity)
def test_error_long_commodity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a commodity is not longer than 255 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(commodity_unit="a" * 256, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity_unit",)
    assert exc_info.value.errors()[0]["msg"] == "Commodity must not be longer than 255 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_commodity)
def test_ok_commoditys(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a commodity with everything between 1 and 255 characters is valid
    """
    schema(commodity_unit="a", **data)
    schema(commodity_unit="a" * 255, **data)
