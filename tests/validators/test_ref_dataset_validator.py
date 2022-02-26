from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model.energy_component import EnergyComponentType
from ensysmod.schemas import EnergyCommodityCreate, EnergyComponentCreate, EnergyConversionFactorCreate
from ensysmod.schemas.energy_model import EnergyModelCreate
from ensysmod.schemas.energy_transmission_distance import EnergyTransmissionDistanceCreate
from ensysmod.schemas.region import RegionCreate

schemas_with_ref_dataset_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyCommodityCreate, {"name": "test", "description": "foo", "unit": "bar"}),
    (EnergyComponentCreate, {"name": "test", "description": "foo", "type": EnergyComponentType.SOURCE}),
    (EnergyModelCreate, {"name": "test"}),
    (RegionCreate, {"name": "test"})
]

schemas_with_ref_dataset_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyConversionFactorCreate, {"conversion_factor": 4.2, "commodity": "bar"}),
    (EnergyTransmissionDistanceCreate, {"distance": 5, "ref_region_from": 42, "ref_region_to": 1337})
]

schemas_with_ref_dataset = schemas_with_ref_dataset_required + schemas_with_ref_dataset_optional


@pytest.mark.parametrize("schema,data", schemas_with_ref_dataset_required)
def test_error_missing_ref_dataset(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a dataset is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_dataset",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_ref_dataset_optional)
def test_ok_missing_ref_dataset(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a dataset is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_ref_dataset)
def test_error_on_zero_ref_dataset(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a dataset is not zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_dataset=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_dataset",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to a dataset must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_ref_dataset)
def test_error_on_negative_ref_dataset(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a dataset is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_dataset=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_dataset",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to a dataset must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_ref_dataset)
def test_ok_ref_datasets(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a dataset with positive id is valid
    """
    schema(ref_dataset=1, **data)
