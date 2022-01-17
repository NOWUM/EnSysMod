from typing import Type, List, Tuple, Dict, Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas import EnergyConversionFactorCreate

schemas_with_ref_component_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = []

schemas_with_ref_component_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyConversionFactorCreate, {"conversion_factor": 4.2, "commodity": "bar"})
]

schemas_with_ref_component = schemas_with_ref_component_required + schemas_with_ref_component_optional


@pytest.mark.parametrize("schema,data", schemas_with_ref_component_required)
def test_error_missing_ref_component(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a component is required for a schema
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_component",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@pytest.mark.parametrize("schema,data", schemas_with_ref_component_optional)
def test_ok_missing_ref_component(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a component is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize("schema,data", schemas_with_ref_component)
def test_error_on_zero_ref_component(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a component is not zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_component=0, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_component",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to a component must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_ref_component)
def test_error_on_negative_ref_component(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a component is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(ref_component=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("ref_component",)
    assert exc_info.value.errors()[0]["msg"] == "Reference to a component must be positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_ref_component)
def test_ok_ref_components(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that a reference to a component with positive id is valid
    """
    schema(ref_component=1, **data)
