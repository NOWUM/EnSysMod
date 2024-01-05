from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_sink import EnergySinkCreate, EnergySinkUpdate
from ensysmod.schemas.energy_source import EnergySourceCreate, EnergySourceUpdate

schemas_with_yearly_limit_required: list[tuple[type[BaseModel], dict[str, Any]]] = []

schemas_with_yearly_limit_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergySourceUpdate, {}),
    (EnergySourceCreate, {"name": "test", "ref_dataset": 42, "type": EnergyComponentType.SOURCE, "commodity": "bar"}),
    (EnergySinkUpdate, {}),
    (EnergySinkCreate, {"name": "test", "ref_dataset": 42, "type": EnergyComponentType.SINK, "commodity": "bar"}),
]

schemas_with_yearly_limit = schemas_with_yearly_limit_required + schemas_with_yearly_limit_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_yearly_limit_optional)
def test_ok_missing_yearly_limit_and_commodity_limit_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that yearly limit and commodity limit id is optional for a schema
    """
    schema(**data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_yearly_limit_optional)
def test_ok_none_yearly_limit_and_commodity_limit_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that yearly limit and commodity limit id is optional for a schema
    """
    schema(yearly_limit=None, commodity_limit_id=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_yearly_limit)
def test_error_missing_commodity_limit_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that commodity limit id is required if yearly limit is specified
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(yearly_limit=999, commodity_limit_id=None, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "If yearly_limit is specified, commodity_limit_id must be specified as well."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_yearly_limit)
def test_error_on_negative_yearly_limit(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that yearly limit under zero is invalid
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(yearly_limit=-0.5, commodity_limit_id="limit", **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Yearly limit must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_yearly_limit)
def test_error_long_commodity_limit_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that commodity limit id longer than 100 characters is invalid
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(yearly_limit=999, commodity_limit_id="a" * 101, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Commodity limit ID must not be longer than 100 characters."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_yearly_limit)
def test_ok_yearly_limit_and_commodity_limit_id(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that yearly limit above zero and commodity limit id between 1 and 100 characters is valid
    """
    schema(yearly_limit=0, commodity_limit_id="a", **data)
    schema(yearly_limit=999, commodity_limit_id="a" * 100, **data)
