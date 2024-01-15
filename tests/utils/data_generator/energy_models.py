from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyModel
from ensysmod.model.energy_model_override import EnergyModelOverrideAttribute, EnergyModelOverrideOperation
from ensysmod.schemas import EnergyModelCreate, EnergyModelOptimizationCreate, EnergyModelOverrideCreate
from tests.utils.data_generator.datasets import get_example_dataset, new_dataset
from tests.utils.data_generator.energy_sinks import new_sink
from tests.utils.utils import random_string


def energy_model_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
) -> EnergyModelCreate:
    """
    Generate an energy model create request with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header).id
    component = new_sink(db, user_header, dataset_id=dataset_id)
    return EnergyModelCreate(
        name=f"EnergyModel-Dataset{dataset_id}-{random_string()}",
        ref_dataset=dataset_id,
        description=None,
        override_parameters=[
            EnergyModelOverrideCreate(
                ref_dataset=dataset_id,
                component=component.component.name,
                region=None,
                region_to=None,
                attribute=EnergyModelOverrideAttribute.yearlyLimit,
                operation=EnergyModelOverrideOperation.set,
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


def new_energy_model(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
) -> EnergyModel:
    """
    Create an energy model with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    create_request = energy_model_create_request(db, user_header, dataset_id=dataset_id)
    return crud.energy_model.create(db=db, obj_in=create_request)


def get_example_model(db: Session, user_header: dict[str, str], *, example_dataset: str) -> EnergyModel:
    """
    Return example model entry in db if it exists, otherwise create it.
    """
    dataset = get_example_dataset(db, user_header, example_dataset=example_dataset)
    model = crud.energy_model.get_by_dataset_and_name(db, dataset_id=dataset.id, name=dataset.name)
    if model is None:
        create_request = EnergyModelCreate(
            name=example_dataset,
            ref_dataset=dataset.id,
            description=None,
            override_parameters=None,
            optimization_parameters=None,
        )
        model = crud.energy_model.create(db=db, obj_in=create_request)
    return model
