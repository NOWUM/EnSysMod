from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyConversionFactorCreate, EnergyConversionFactorUpdate

schemas_with_conversion_factor_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyConversionFactorCreate, {"commodity_name": "bar"}),
]

schemas_with_conversion_factor_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyConversionFactorUpdate, {}),
]

schemas_with_conversion_factor = schemas_with_conversion_factor_required + schemas_with_conversion_factor_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factor_optional)
def test_ok_missing_conversion_factor(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factor is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factor_optional)
def test_ok_none_conversion_factor(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factor is optional for a schema
    """
    schema(conversion_factor=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factor_required)
def test_error_missing_conversion_factor(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factor is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("conversion_factor",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factor)
def test_error_too_high_conversion_factor(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factor is not greater than 5
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(conversion_factor=6, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("conversion_factor",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be less than or equal to 5"
    assert exc_info.value.errors()[0]["type"] == "less_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factor)
def test_error_too_low_conversion_factor(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factor is not less than -5
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(conversion_factor=-6, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("conversion_factor",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to -5"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_conversion_factor)
def test_ok_conversion_factors(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a conversion factor with everything between -5 and 5 is valid
    """
    schema(conversion_factor=5, **data)
    schema(conversion_factor=0, **data)
    schema(conversion_factor=-5, **data)
