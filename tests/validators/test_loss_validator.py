from typing import Any, Dict, List, Tuple, Type

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyTransmissionLossCreate, EnergyTransmissionLossUpdate

schemas_with_loss_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyTransmissionLossCreate, {"ref_dataset": 1, "component": "test", "region_from": "Region 1", "region_to": "Region 2"}),
    (EnergyTransmissionLossUpdate, {}),
]

schemas_with_loss_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_loss = schemas_with_loss_required + schemas_with_loss_optional


@pytest.mark.parametrize("schema,data", schemas_with_loss_optional)
def test_ok_missing_loss(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_loss_optional)
def test_ok_none_loss(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss is optional for a schema
    """
    schema(loss=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_loss_required)
def test_error_missing_loss(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_loss)
def test_error_negative_loss(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(loss=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss",)
    assert exc_info.value.errors()[0]["msg"] == "The loss must be between zero and one."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_loss)
def test_error_loss_above_one(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss is not above one
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(loss=1.01, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss",)
    assert exc_info.value.errors()[0]["msg"] == "The loss must be between zero and one."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_loss)
def test_ok_losses(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a loss is between zero and one valid
    """
    schema(loss=0, **data)
    schema(loss=0.5, **data)
    schema(loss=1, **data)
