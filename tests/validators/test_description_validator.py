from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import DatasetCreate, DatasetUpdate, EnergyCommodityCreate, EnergyCommodityUpdate, \
    EnergyComponentCreate
from ensysmod.schemas.energy_model import EnergyModelCreate, EnergyModelUpdate

schemas_with_description_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_description_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (DatasetCreate, {"name": "foo"}),
    (EnergyCommodityCreate, {"name": "foo", "unit": "bar", "ref_dataset": 42}),
    (EnergyComponentCreate, {"name": "foo", "type": EnergyComponentType.SOURCE, "ref_dataset": 42}),
    (EnergyModelCreate, {"name": "foo", "ref_dataset": 42}),
    (DatasetUpdate, {}),
    (EnergyCommodityUpdate, {}),
    (EnergyCommodityUpdate, {}),
    (EnergyModelUpdate, {})
]

schemas_with_description = schemas_with_description_required + schemas_with_description_optional


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
    with pytest.raises(ValidationError) as exc_info:
        schema(description="a" * 1025, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("description",)
    assert exc_info.value.errors()[0]["msg"] == "Description must not be longer than 1024 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_description)
def test_ok_descriptions(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a description with everything between 1 and 1024 characters is valid
    """
    schema(description="a", **data)
    schema(description="a" * 1024, **data)
