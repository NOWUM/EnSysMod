from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import DatasetCreate, DatasetUpdate, EnergyCommodityCreate, EnergyCommodityUpdate, \
    EnergyComponentCreate, RegionCreate, EnergyComponentUpdate, RegionUpdate

schemas_with_name_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (DatasetCreate, {"description": "foo"}),
    (EnergyCommodityCreate, {"description": "foo", "unit": "bar", "ref_dataset": 42}),
    (EnergyComponentCreate, {"type": EnergyComponentType.SOURCE, "ref_dataset": 42}),
    (RegionCreate, {}),
]

schemas_with_name_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (DatasetUpdate, {}),
    (EnergyCommodityUpdate, {}),
    (EnergyComponentUpdate, {}),
    (RegionUpdate, {}),
]

schemas_with_name = schemas_with_name_required + schemas_with_name_optional


@pytest.mark.parametrize("schema,data", schemas_with_name_required)
def test_error_empty_name(schema: Type, data: dict):
    """
    Test that a name is required for a schema
    """
    with pytest.raises(ValueError):
        schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_name_optional)
def test_ok_empty_name(schema: Type, data: dict):
    """
    Test that a name is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_name)
def test_error_long_name(schema: Type, data: dict):
    """
    Test that a name is not longer than 255 characters
    """
    with pytest.raises(ValueError):
        schema(name="a" * 256, **data)


@pytest.mark.parametrize("schema,data", schemas_with_name)
def test_ok_names(schema: Type, data: dict):
    """
    Test that a name with everything between 1 and 255 characters is valid
    """
    schema(name="a", **data)
    schema(name="a" * 255, **data)
