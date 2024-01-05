from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyModel
from ensysmod.schemas import (
    EnergyModelCreate,
    EnergyModelOptimizationCreate,
    EnergyModelOverrideCreate,
)
from tests.utils.data_generator.datasets import create_example_dataset, dataset_create
from tests.utils.data_generator.energy_sinks import sink_create
from tests.utils.utils import random_lower_string


def energy_model_create_request(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyModelCreate:
    """
    Generate an energy model create request with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    component = sink_create(db, current_user_header, dataset_id)
    return EnergyModelCreate(
        name=f"EnergyModel-Dataset{dataset_id}-{random_lower_string()}",
        ref_dataset=dataset_id,
        description="EnergyModel description",
        override_parameters=[
            EnergyModelOverrideCreate(
                ref_dataset=dataset_id,
                component=component.component.name,
                region=None,
                region_to=None,
                attribute="yearly_limit",
                operation="set",
                value=366.6,
            ),
        ],
        optimization_parameters=EnergyModelOptimizationCreate(
            start_year=2020,
            end_year=2050,
            number_of_steps=3,
            years_per_step=10,
            CO2_reference=366.6,
            CO2_reduction_targets=[0, 25, 50, 100],
        ),
    )


def energy_model_create(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyModel:
    """
    Create an energy model with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    create_request = energy_model_create_request(db, current_user_header, dataset_id)
    return crud.energy_model.create(db=db, obj_in=create_request)


def create_example_model(db: Session, data_folder: str):
    """
    Create model from example dataset.
    """
    dataset = create_example_dataset(db, data_folder)

    create_request = EnergyModelCreate(
        name=f"Example_Model-{data_folder}-" + random_lower_string(),
        ref_dataset=dataset.id,
        description="Example_Model description",
        override_parameters=None,
        optimization_parameters=None,
    )
    return crud.energy_model.create(db=db, obj_in=create_request)
