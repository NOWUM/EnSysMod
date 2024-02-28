from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import (
    EnergyCommodityCreate,
    EnergyComponentCreate,
    EnergyModelCreate,
    RegionCreate,
    TransmissionDistanceCreate,
    TransmissionLossCreate,
)

schemas_with_ref_dataset_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyCommodityCreate, {"name": "test", "description": "foo", "unit": "bar"}),
    (EnergyComponentCreate, {"name": "test", "description": "foo", "type": EnergyComponentType.SOURCE}),
    (EnergyModelCreate, {"name": "test"}),
    (RegionCreate, {"name": "test"}),
    (TransmissionDistanceCreate, {"distance": 1000, "component_name": "test", "region_name": "Region 1", "region_to_name": "Region 2"}),
    (TransmissionLossCreate, {"loss": 0.00001, "component_name": "test", "region_name": "Region 1", "region_to_name": "Region 2"}),
]

schemas_with_ref_dataset_optional: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_ref_dataset = schemas_with_ref_dataset_required + schemas_with_ref_dataset_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_dataset_required)
def test_error_missing_ref_dataset(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a dataset is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_dataset",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_dataset_optional)
def test_ok_missing_ref_dataset(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a dataset is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_dataset)
def test_error_on_zero_ref_dataset(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a dataset is not zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_dataset=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_dataset",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than"


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_dataset)
def test_error_on_negative_ref_dataset(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a dataset is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_dataset=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_dataset",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than"


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_dataset)
def test_ok_ref_datasets(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a dataset with positive id is valid
    """
    schema(ref_dataset=1, **data)
