from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

schemas_with_ref_component_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_ref_component_optional: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_ref_component = schemas_with_ref_component_required + schemas_with_ref_component_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_component_required)
def test_error_missing_ref_component(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a component is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_component",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_component_optional)
def test_ok_missing_ref_component(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a component is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_component)
def test_error_on_zero_ref_component(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a component is not zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_component=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_component",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than"


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_component)
def test_error_on_negative_ref_component(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a component is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_component=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_component",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than"


@pytest.mark.parametrize(("schema", "data"), schemas_with_ref_component)
def test_ok_ref_components(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a reference to a component with positive id is valid
    """
    schema(ref_component=1, **data)
