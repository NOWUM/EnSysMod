from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergySinkCreate, EnergySinkUpdate, EnergySourceCreate, EnergySourceUpdate

schemas_with_commodity_cost_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_commodity_cost_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergySourceUpdate, {}),
    (EnergySourceCreate, {"name": "test", "ref_dataset": 42, "type": EnergyComponentType.SOURCE, "commodity": "bar"}),
    (EnergySinkUpdate, {}),
    (EnergySinkCreate, {"name": "test", "ref_dataset": 42, "type": EnergyComponentType.SINK, "commodity": "bar"}),
]

schemas_with_commodity_cost = schemas_with_commodity_cost_required + schemas_with_commodity_cost_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_cost_optional)
def test_ok_missing_commodity_cost(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity cost is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_cost_optional)
def test_ok_none_commodity_cost(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity cost is optional for a schema
    """
    schema(commodity_cost=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_cost)
def test_error_on_negative_commodity_cost(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity cost is not under zero
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(commodity_cost=-0.5, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("commodity_cost",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_commodity_cost)
def test_ok_commodity_costs(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a commodity cost with everything over 0 is valid
    """
    schema(commodity_cost=0, **data)
    schema(commodity_cost=1.5, **data)
