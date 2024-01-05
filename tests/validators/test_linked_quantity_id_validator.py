from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponentUpdate

schemas_with_linked_quantity_id_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_linked_quantity_id_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyComponentUpdate, {}),
    (EnergyComponentCreate, {"name": "test", "description": "foo", "ref_dataset": 42, "type": EnergyComponentType.SOURCE}),
]

schemas_with_linked_quantity_id = schemas_with_linked_quantity_id_required + schemas_with_linked_quantity_id_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_linked_quantity_id_optional)
def test_ok_missing_linked_quantity_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a linked quantity id is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_linked_quantity_id_optional)
def test_ok_none_linked_quantity_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a linked quantity id is optional for a schema
    """
    schema(linked_quantity_id=None, **data)
    schema(linked_quantity_id="", **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_linked_quantity_id)
def test_error_long_linked_quantity_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a linked quantity id is not longer than 100 characters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(linked_quantity_id="a" * 101, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("linked_quantity_id",)
    assert exc_info.value.errors()[0]["msg"] == "Linked quantity id must not be longer than 100 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_linked_quantity_id)
def test_ok_linked_quantity_ids(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a linked quantity id between 1 and 100 characters is valid
    """
    schema(linked_quantity_id="a", **data)
    schema(linked_quantity_id="a" * 100, **data)
