from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import DatasetCreate, DatasetUpdate, EnergyCommodityCreate, EnergyCommodityUpdate, \
    EnergyComponentCreate, RegionCreate, EnergyComponentUpdate, RegionUpdate
from ensysmod.schemas.energy_model import EnergyModelCreate, EnergyModelUpdate

schemas_with_name_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (DatasetCreate, {"description": "foo"}),
    (EnergyCommodityCreate, {"description": "foo", "unit": "bar", "ref_dataset": 42}),
    (EnergyComponentCreate, {"type": EnergyComponentType.SOURCE, "ref_dataset": 42}),
    (RegionCreate, {"ref_dataset": 42}),
    (EnergyModelCreate, {"ref_dataset": 42})
]

schemas_with_name_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (DatasetUpdate, {}),
    (EnergyCommodityUpdate, {}),
    (EnergyComponentUpdate, {}),
    (RegionUpdate, {}),
    (EnergyModelUpdate, {})
]

schemas_with_name = schemas_with_name_required + schemas_with_name_optional


@pytest.mark.parametrize("schema,data", schemas_with_name_required)
def test_error_missing_name(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a name is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("name",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_name_optional)
def test_ok_missing_name(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a name is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_name)
def test_error_empty_name(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a name is not empty, if specified
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(name="", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("name",)
    assert exc_info.value.errors()[0]["msg"] == "Name must not be empty."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_name)
def test_error_long_name(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a name is not longer than 255 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(name="a" * 256, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("name",)
    assert exc_info.value.errors()[0]["msg"] == "Name must not be longer than 255 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_name)
def test_ok_names(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a name with everything between 1 and 255 characters is valid
    """
    schema(name="a", **data)
    schema(name="a" * 255, **data)
