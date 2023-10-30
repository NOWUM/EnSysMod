from typing import Any

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import (
    EnergyTransmission,
    EnergyTransmissionDistance,
    EnergyTransmissionLoss,
)
from ensysmod.schemas import (
    EnergyTransmissionCreate,
    EnergyTransmissionDistanceCreate,
    EnergyTransmissionLossCreate,
)
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.data_generator.regions import region_create
from tests.utils.utils import random_lower_string


def transmission_create_request(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyTransmissionCreate:
    """
    Generate a transmission create request with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    if commodity_name is None:
        commodity_name = commodity_create(db, current_user_header, dataset_id).name
    return EnergyTransmissionCreate(
        ref_dataset=dataset_id,
        name=f"EnergyTransmission-Dataset{dataset_id}-{random_lower_string()}",
        description="Description",
        commodity=commodity_name,
    )


def transmission_create(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyTransmission:
    """
    Create a transmission component with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    create_request = transmission_create_request(db, current_user_header, dataset_id, commodity_name)
    return crud.energy_transmission.create(db=db, obj_in=create_request)


def transmission_distance_create_request(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyTransmissionDistanceCreate:
    """
    Generate a transmission distance create request with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    commodity_name = commodity_create(db, current_user_header, dataset_id=dataset_id).name
    region_from = region_create(db, current_user_header, dataset_id=dataset_id)
    region_to = region_create(db, current_user_header, dataset_id=dataset_id)
    transmission = transmission_create(db, current_user_header, dataset_id, commodity_name)
    return EnergyTransmissionDistanceCreate(
        distance=1000,
        ref_dataset=dataset_id,
        component=transmission.component.name,
        region_from=region_from.name,
        region_to=region_to.name,
    )


def transmission_distance_create(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyTransmissionDistance:
    """
    Create a transmission distance with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    create_request = transmission_distance_create_request(db, current_user_header, dataset_id)
    return crud.energy_transmission_distance.create(db=db, obj_in=create_request)


def transmission_loss_create_request(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyTransmissionLossCreate:
    """
    Generate a transmission loss create request with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    commodity_name = commodity_create(db, current_user_header, dataset_id=dataset_id).name
    region_from = region_create(db, current_user_header, dataset_id=dataset_id)
    region_to = region_create(db, current_user_header, dataset_id=dataset_id)
    transmission = transmission_create(db, current_user_header, dataset_id, commodity_name)
    return EnergyTransmissionLossCreate(
        loss=0.00001,
        ref_dataset=dataset_id,
        component=transmission.component.name,
        region_from=region_from.name,
        region_to=region_to.name,
    )


def transmission_loss_create(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyTransmissionLoss:
    """
    Create a transmission loss with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    create_request = transmission_loss_create_request(db, current_user_header, dataset_id)
    return crud.energy_transmission_loss.create(db=db, obj_in=create_request)


def create_transmission_scenario(db: Session, current_user_header: dict[str, str]) -> dict[str, Any]:
    """
    Generate a dataset, a commodity, two regions and two transmission components in the same dataset,
    then add entries of transmission distances and losses between the regions.

    Return a dictionary of the dataset, list of transmission components, list of transmission distances and losses.
    """
    dataset = dataset_create(db, current_user_header)
    commodity = commodity_create(db, current_user_header, dataset_id=dataset.id)
    region1 = region_create(db, current_user_header, dataset_id=dataset.id)
    region2 = region_create(db, current_user_header, dataset_id=dataset.id)
    transmission1 = transmission_create(db, current_user_header, dataset_id=dataset.id, commodity_name=commodity.name)
    transmission2 = transmission_create(db, current_user_header, dataset_id=dataset.id, commodity_name=commodity.name)

    def create_distance_entry(transmission, region_from, region_to, distance):
        return crud.energy_transmission_distance.create(
            db=db,
            obj_in=EnergyTransmissionDistanceCreate(
                distance=distance,
                ref_dataset=dataset.id,
                component=transmission.component.name,
                region_from=region_from.name,
                region_to=region_to.name,
            ),
        )

    def create_loss_entry(transmission, region_from, region_to, loss):
        return crud.energy_transmission_loss.create(
            db=db,
            obj_in=EnergyTransmissionLossCreate(
                loss=loss,
                ref_dataset=dataset.id,
                component=transmission.component.name,
                region_from=region_from.name,
                region_to=region_to.name,
            ),
        )

    distances = [
        create_distance_entry(transmission1, region1, region2, 1000),
        create_distance_entry(transmission1, region2, region1, 2000),
        create_distance_entry(transmission2, region1, region2, 3000),
        create_distance_entry(transmission2, region2, region1, 4000),
    ]
    losses = [
        create_loss_entry(transmission1, region1, region2, 0.00001),
        create_loss_entry(transmission1, region2, region1, 0.00002),
        create_loss_entry(transmission2, region1, region2, 0.00003),
        create_loss_entry(transmission2, region2, region1, 0.00004),
    ]

    return {
        "dataset": dataset,
        "transmissions": [transmission1, transmission2],
        "distances": distances,
        "losses": losses,
    }
