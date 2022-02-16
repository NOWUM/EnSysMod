from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyConversionFactorCreate
from ensysmod.schemas.energy_sink import EnergySinkCreate
from ensysmod.schemas.energy_source import EnergySourceCreate
from ensysmod.schemas.energy_storage import EnergyStorageCreate
from ensysmod.schemas.energy_transmission import EnergyTransmissionCreate

schemas_with_commodity_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyConversionFactorCreate, {"conversion_factor": 4.2}),
    (EnergySinkCreate, {"name": "foo", "ref_dataset": 42}),
    (EnergySourceCreate, {"name": "foo", "ref_dataset": 42}),
    (EnergyStorageCreate, {"name": "foo", "ref_dataset": 42}),
    (EnergyTransmissionCreate, {"name": "foo", "ref_dataset": 42, })
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
    assert exc_info.value.errors()[0]["loc"] == ("commodity",)
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
        schema(commodity="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity",)
    assert exc_info.value.errors()[0]["msg"] == "Commodity must not be empty."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_commodity)
def test_error_long_commodity(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a commodity is not longer than 255 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(commodity="a" * 256, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity",)
    assert exc_info.value.errors()[0]["msg"] == "Commodity must not be longer than 255 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_commodity)
def test_ok_commoditys(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a commodity with everything between 1 and 255 characters is valid
    """
    schema(commodity="a", **data)
    schema(commodity="a" * 255, **data)
