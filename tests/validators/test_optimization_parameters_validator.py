from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas.energy_model import EnergyModelOptimizationCreate

schemas_with_optimization_parameters_required: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (
        EnergyModelOptimizationCreate,
        {
            "end_year": 2050,
            "number_of_steps": 3,
            "years_per_step": 10,
            "CO2_reference": 366,
            "CO2_reduction_targets": [0, 25, 50, 100],
        },
    ),
]

schemas_with_optimization_parameters_optional: list[tuple[type[BaseModel], dict[str, Any]]] = [
    (EnergyModelOptimizationCreate, {"start_year": 2020}),
]

schemas_with_optimization_parameters = schemas_with_optimization_parameters_required + schemas_with_optimization_parameters_optional


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_ok_missing_optimization_parameters(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that optimization parameters are optional for a schema
    """
    schema(end_year=2050, number_of_steps=3, years_per_step=10, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_ok_none_optimization_parameters(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that optimization parameters are optional for a schema
    """
    schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=None, CO2_reduction_targets=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_required)
def test_error_missing_start_year(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that start year is required for optimization parameters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("start_year",)
    assert exc_info.value.errors()[0]["msg"] == "Field required"
    assert exc_info.value.errors()[0]["type"] == "missing"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_required)
def test_error_negative_start_year(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that a start year is not negative
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(start_year=-1, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("start_year",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_missing_timeframe_parameters(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert (
        exc_info.value.errors()[0]["msg"]
        == "Value error, At least two of the parameters end_year, number_of_steps or years_per_step must be specified."
    )
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_only_end_year_given(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=None, years_per_step=None, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert (
        exc_info.value.errors()[0]["msg"] == "Value error, At least one of the parameters number_of_steps or years_per_step must also be specified."
    )
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_only_number_of_steps_given(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=None, number_of_steps=3, years_per_step=None, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert exc_info.value.errors()[0]["msg"] == "Value error, At least one of the parameters end_year or years_per_step must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_only_years_per_step_given(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=None, number_of_steps=None, years_per_step=10, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert exc_info.value.errors()[0]["msg"] == "Value error, At least one of the parameters end_year or number_of_steps must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_ok_missing_end_year(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that if end_year is missing, it will be calculated based on the remaining timeframe parameters
    """
    schema(end_year=None, number_of_steps=3, years_per_step=10, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_ok_missing_number_of_steps(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that if number_of_steps is missing, it will be calculated based on the remaining timeframe parameters
    """
    schema(end_year=2050, number_of_steps=None, years_per_step=10, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_ok_missing_years_per_step(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that if years_per_step is missing, it will be calculated based on the remaining timeframe parameters
    """
    schema(end_year=2050, number_of_steps=3, years_per_step=None, **data)


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_invalid_timeframe_parameter(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that the timeframe parameters must satisfy the equation: (end_year - start_year) = number_of_steps * years_per_step
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=9999, number_of_steps=3, years_per_step=10, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert (
        exc_info.value.errors()[0]["msg"]
        == "Value error, The parameters must satisfy the equation: (end_year - start_year) = number_of_steps * years_per_step."
    )
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_missing_CO2_Reference(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that both CO2_reference and CO2_reduction_targets are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=None, CO2_reduction_targets=[0, 25, 50, 100], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert exc_info.value.errors()[0]["msg"] == "Value error, If CO2_reduction_targets is specified, CO2_reference must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_missing_CO2_reduction_targets(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that both CO2_reference and CO2_reduction_targets are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=366, CO2_reduction_targets=None, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert exc_info.value.errors()[0]["msg"] == "Value error, If CO2_reference is specified, CO2_reduction_targets must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_negative_CO2_reference(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that CO2_reference has to be zero or positive
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=-366, CO2_reduction_targets=[0, 25, 50, 100], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("CO2_reference",)
    assert exc_info.value.errors()[0]["msg"] == "Input should be greater than or equal to 0"
    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_negative_CO2_reduction_target(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that values of CO2_reduction_targets must be between 0 and 100
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=366, CO2_reduction_targets=[0, -25, 50, 101], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert exc_info.value.errors()[0]["msg"] == "Value error, Values of CO2_reduction_targets must be between 0 and 100."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize(("schema", "data"), schemas_with_optimization_parameters_optional)
def test_error_invalid_CO2_reduction_target_length(schema: type[BaseModel], data: dict[str, Any]):
    """
    Test that the number of values given in CO2_reduction_targets must match the number of optimization runs
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=366, CO2_reduction_targets=[0, 25, 50], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ()
    assert (
        exc_info.value.errors()[0]["msg"]
        == "Value error, The number of values given in CO2_reduction_targets must match the number of optimization runs. Expected: 4, given: 3."
    )
    assert exc_info.value.errors()[0]["type"] == "value_error"
