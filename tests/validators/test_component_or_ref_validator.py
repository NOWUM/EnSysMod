from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

schemas_with_component_or_ref_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_component_or_ref_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_component_or_ref = schemas_with_component_or_ref_required + schemas_with_component_or_ref_optional


@pytest.mark.parametrize("schema,data", schemas_with_component_or_ref_required)
def test_error_missing_component_or_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a component_or_ref is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("component_or_ref",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_component_or_ref_optional)
def test_ok_missing_component_or_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a component_or_ref is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_component_or_ref)
def test_error_on_negative_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a component_or_ref is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_component=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to a component must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_component_or_ref)
def test_error_on_zero_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a component_or_ref is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_component=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to a component must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_component_or_ref)
def test_error_on_long_component(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a component_or_ref is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(component='a' * 101, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "The component must not be longer than 100 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_component_or_ref)
def test_ok_component_or_ref(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a component_or_ref with everything over 0 is valid
    """
    schema(component='a', **data)
    schema(component='a' * 100, **data)
    schema(ref_component=1, **data)
