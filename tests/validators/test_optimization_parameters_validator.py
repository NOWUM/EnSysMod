from typing import Any, Dict, List, Tuple, Type

import pytest
from pydantic import BaseModel, ValidationError

from ensysmod.schemas.energy_model import EnergyModelOptimizationCreate

schemas_with_optimization_parameters_required: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyModelOptimizationCreate, {
        "end_year": 2050,
        "number_of_steps": 3,
        "years_per_step": 10,
        "CO2_reference": 366,
        "CO2_reduction_targets": [0, 25, 50, 100]
    })
]

schemas_with_optimization_parameters_optional: List[Tuple[Type[BaseModel], Dict[str, Any]]] = [
    (EnergyModelOptimizationCreate, {
        "start_year": 2020,
    })
]

schemas_with_optimization_parameters = schemas_with_optimization_parameters_required + schemas_with_optimization_parameters_optional


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_ok_missing_optimization_parameters(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that optimization parameters are optional for a schema
    """
    schema(end_year=2050, number_of_steps=3, years_per_step=10, **data)


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_ok_none_optimization_parameters(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that optimization parameters are optional for a schema
    """
    schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=None, CO2_reduction_targets=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_required)
def test_error_missing_start_year(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that start year is required for optimization parameters
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 2
    assert exc_info.value.errors()[0]["loc"] == ("start_year",)
    assert exc_info.value.errors()[0]["msg"] == "field required"
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"
    assert exc_info.value.errors()[1]["loc"] == ("__root__",)
    assert exc_info.value.errors()[1]["msg"] == "start_year must be specified."
    assert exc_info.value.errors()[1]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_missing_timeframe_parameters(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "At least two of the parameters end_year, number_of_steps or years_per_step must be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_only_end_year_given(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=None, years_per_step=None, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "At least one of the parameters number_of_steps or years_per_step must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_only_number_of_steps_given(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=None, number_of_steps=3, years_per_step=None, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "At least one of the parameters end_year or years_per_step must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_only_years_per_step_given(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that at least two of the parameters end_year, number_of_steps or years_per_step are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=None, number_of_steps=None, years_per_step=10, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "At least one of the parameters end_year or number_of_steps must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_ok_missing_end_year(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that if end_year is missing, it will be calculated based on the remaining timeframe parameters
    """
    schema(end_year=None, number_of_steps=3, years_per_step=10, **data)


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_ok_missing_number_of_steps(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that if number_of_steps is missing, it will be calculated based on the remaining timeframe parameters
    """
    schema(end_year=2050, number_of_steps=None, years_per_step=10, **data)


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_ok_missing_years_per_step(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that if years_per_step is missing, it will be calculated based on the remaining timeframe parameters
    """
    schema(end_year=2050, number_of_steps=3, years_per_step=None, **data)


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_invalid_timeframe_parameter(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that the timeframe parameters must satisfy the equation: (end_year - start_year) = number_of_steps * years_per_step
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=9999, number_of_steps=3, years_per_step=10, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert (
        exc_info.value.errors()[0]["msg"] == "The parameters must satisfy the equation: (end_year - start_year) = number_of_steps * years_per_step."
    )
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_missing_CO2_Reference(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that both CO2_reference and CO2_reduction_targets are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=None, CO2_reduction_targets=[0, 25, 50, 100], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "If CO2_reduction_targets is specified, CO2_reference must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_missing_CO2_reduction_targets(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that both CO2_reference and CO2_reduction_targets are required
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=366, CO2_reduction_targets=None, **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "If CO2_reference is specified, CO2_reduction_targets must also be specified."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_negative_CO2_reference(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that CO2_reference has to be zero or positive
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=-366, CO2_reduction_targets=[0, 25, 50, 100], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "CO2_reference must be zero or positive."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_negative_CO2_reduction_target(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that values of CO2_reduction_targets must be between 0 and 100
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=366, CO2_reduction_targets=[0, -25, 50, 101], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert exc_info.value.errors()[0]["msg"] == "Values of CO2_reduction_targets must be between 0 and 100."
    assert exc_info.value.errors()[0]["type"] == "value_error"


@pytest.mark.parametrize("schema,data", schemas_with_optimization_parameters_optional)
def test_error_invalid_CO2_reduction_target_length(schema: Type[BaseModel], data: Dict[str, Any]):
    """
    Test that the number of values given in CO2_reduction_targets must match the number of optimization runs
    """
    with pytest.raises(ValidationError) as exc_info:
        schema(end_year=2050, number_of_steps=3, years_per_step=10, CO2_reference=366, CO2_reduction_targets=[0, 25, 50], **data)

    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["loc"] == ("__root__",)
    assert (
        exc_info.value.errors()[0]["msg"]
        == "The number of values given in CO2_reduction_targets must match the number of optimization runs. Expected: 4, given: 3."
    )
    assert exc_info.value.errors()[0]["type"] == "value_error"
