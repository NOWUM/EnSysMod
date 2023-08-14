from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyModel
from ensysmod.schemas import (
    EnergyModelCreate,
    EnergyModelOptimizationCreate,
    EnergyModelOverrideCreate,
)
from tests.utils.data_generator.datasets import (
    create_example_dataset,
    fixed_existing_dataset,
)
from tests.utils.data_generator.energy_sources import fixed_existing_energy_source
from tests.utils.utils import random_lower_string


def random_energy_model_create(db: Session) -> EnergyModelCreate:
    """
    Generate a random energy model create request.
    """
    dataset = fixed_existing_dataset(db)
    component_1 = fixed_existing_energy_source(db)
    return EnergyModelCreate(
        name=f"EnergyModel-{dataset.id}-" + random_lower_string(),
        ref_dataset=dataset.id,
        description="EnergyModel description",
        override_parameters=[
            EnergyModelOverrideCreate(
                component=component_1.component.name,
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
            CO2_reduction_targets=[0, 25, 50, 100]
        )
    )


def random_existing_energy_model(db: Session) -> EnergyModel:
    """
    Generate a random existing energy model.
    """
    create_request = random_energy_model_create(db)
    return crud.energy_model.create(db=db, obj_in=create_request)


def fixed_energy_model_create(db: Session) -> EnergyModelCreate:
    """
    Generate a fixed energy model create request.
    Will always return the same energy model.
    """
    dataset = fixed_existing_dataset(db)
    return EnergyModelCreate(
        name=f"EnergyModel-{dataset.id}-Fixed",
        ref_dataset=dataset.id,
        description="EnergyModel description",
    )


def fixed_existing_energy_model(db: Session) -> EnergyModel:
    """
    Generate a fixed existing energy model.
    Will always return the same energy model.
    """
    create_request = fixed_energy_model_create(db)
    model = crud.energy_model.get_by_dataset_and_name(
        db=db, dataset_id=create_request.ref_dataset, name=create_request.name
    )
    if model is None:
        return crud.energy_model.create(db=db, obj_in=create_request)
    return model


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
        optimization_parameters=None
    )
    model = crud.energy_model.create(db=db, obj_in=create_request)

    return model
