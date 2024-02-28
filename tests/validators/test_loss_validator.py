from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import TransmissionLossCreate, TransmissionLossUpdate

schemas_with_loss_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (TransmissionLossCreate, {"ref_dataset": 1, "component_name": "test", "region_name": "Region 1", "region_to_name": "Region 2"}),
    (TransmissionLossUpdate, {}),
]

schemas_with_loss_optional: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_loss = schemas_with_loss_required + schemas_with_loss_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_loss_optional)
def test_ok_missing_loss(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a loss is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_loss_optional)
def test_ok_none_loss(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a loss is optional for a schema
    """
    schema(loss=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_loss_required)
def test_error_missing_loss(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a loss is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_loss)
def test_error_negative_loss(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a loss is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(loss=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_loss)
def test_error_loss_above_one(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a loss is not above one
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(loss=1.01, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("loss",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be less than or equal to 1"
    assert exc_info.value.errors()[0]["type"] == "less_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_loss)
def test_ok_losses(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a loss is between zero and one valid
    """
    schema(loss=0, **data)
    schema(loss=0.5, **data)
    schema(loss=1, **data)
