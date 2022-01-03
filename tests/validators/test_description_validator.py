from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import DatasetCreate, DatasetUpdate, EnergyCommodityCreate, EnergyCommodityUpdate, \
    EnergyComponentCreate

schemas_with_description_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_description_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (DatasetCreate, {"name": "foo"}),
    (EnergyCommodityCreate, {"name": "foo", "unit": "bar", "ref_dataset": 42}),
    (EnergyComponentCreate, {"name": "foo", "type": EnergyComponentType.SOURCE, "ref_dataset": 42}),
    (DatasetUpdate, {}),
    (EnergyCommodityUpdate, {}),
    (EnergyCommodityUpdate, {})
]

schemas_with_description = schemas_with_description_required + schemas_with_description_optional


@pytest.mark.parametrize("schema,data", schemas_with_description_required)
def test_error_empty_description(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a description is required for a schema
    """
    with pytest.raises(ValueError):
        schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_description_optional)
def test_ok_empty_description(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a description is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_description)
def test_error_long_description(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a description is not longer than 1024 characters
    """
    with pytest.raises(ValueError):
        schema(description="a" * 1025, **data)


@pytest.mark.parametrize("schema,data", schemas_with_description)
def test_ok_descriptions(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a description with everything between 1 and 1024 characters is valid
    """
    schema(description="a", **data)
    schema(description="a" * 1024, **data)
