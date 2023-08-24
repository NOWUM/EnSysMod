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
    RegionCreate,
)
from tests.utils.data_generator import (
    fixed_existing_dataset,
    fixed_existing_energy_commodity,
    random_energy_commodity_create,
    random_existing_dataset,
)
from tests.utils.data_generator.regions import (
    fixed_existing_region,
    fixed_existing_region_alternative,
)
from tests.utils.utils import random_lower_string


def random_energy_transmission_create(db: Session) -> EnergyTransmissionCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyTransmissionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyTransmission-{dataset.id}-{random_lower_string()}",
        description="Description",
        commodity=commodity.name,
    )


def random_existing_energy_transmission(db: Session) -> EnergyTransmission:
    create_request = random_energy_transmission_create(db)
    return crud.energy_transmission.create(db=db, obj_in=create_request)


def fixed_energy_transmission_create(db: Session) -> EnergyTransmissionCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyTransmissionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyTransmission-{dataset.id}-Fixed",
        description="Description",
        commodity=commodity.name,
    )


def fixed_existing_energy_transmission(db: Session) -> EnergyTransmission:
    create_request = fixed_energy_transmission_create(db)
    transmission = crud.energy_transmission.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset, name=create_request.name)
    if transmission is None:
        transmission = crud.energy_transmission.create(db=db, obj_in=create_request)
    return transmission


def fixed_transmission_distance_create(db: Session) -> EnergyTransmissionDistanceCreate:
    dataset = fixed_existing_dataset(db)
    transmission = fixed_existing_energy_transmission(db)
    region_from = fixed_existing_region(db)
    region_to = fixed_existing_region_alternative(db)
    return EnergyTransmissionDistanceCreate(
        distance=1000,
        ref_dataset=dataset.id,
        component=transmission.component.name,
        region_from=region_from.name,
        region_to=region_to.name,
    )


def fixed_existing_transmission_distance(db: Session) -> EnergyTransmissionDistance:
    create_request = fixed_transmission_distance_create(db)
    distance = crud.energy_transmission_distance.get_by_dataset_id_component_region_names(
        db=db,
        dataset_id=create_request.ref_dataset,
        component_name=create_request.component,
        region_from_name=create_request.region_from,
        region_to_name=create_request.region_to,
    )
    if distance is None:
        distance = crud.energy_transmission_distance.create(db=db, obj_in=create_request)
    return distance


def fixed_transmission_loss_create(db: Session) -> EnergyTransmissionLossCreate:
    dataset = fixed_existing_dataset(db)
    transmission = fixed_existing_energy_transmission(db)
    region_from = fixed_existing_region(db)
    region_to = fixed_existing_region_alternative(db)
    return EnergyTransmissionLossCreate(
        loss=0.00001,
        ref_dataset=dataset.id,
        component=transmission.component.name,
        region_from=region_from.name,
        region_to=region_to.name,
    )


def fixed_existing_transmission_loss(db: Session) -> EnergyTransmissionLoss:
    create_request = fixed_transmission_loss_create(db)
    loss = crud.energy_transmission_loss.get_by_dataset_id_component_region_names(
        db=db,
        dataset_id=create_request.ref_dataset,
        component_name=create_request.component,
        region_from_name=create_request.region_from,
        region_to_name=create_request.region_to,
    )
    if loss is None:
        loss = crud.energy_transmission_loss.create(db=db, obj_in=create_request)
    return loss


def create_transmission_scenario(db: Session) -> dict[str, Any]:
    """
    Creates a random dataset, commodity, two transmission components and two regions in the same dataset,
    then add entries of transmission distances and losses between those regions.

    Returns a dictionary of the dataset, list of transmission components, list of transmission distances and losses.
    """
    dataset = random_existing_dataset(db)
    commodity_request = random_energy_commodity_create(db)
    commodity_request.ref_dataset = dataset.id
    commodity = crud.energy_commodity.create(db=db, obj_in=commodity_request)

    transmission1_request = random_energy_transmission_create(db)
    transmission1_request.ref_dataset = dataset.id
    transmission1_request.commodity = commodity.name
    transmission1 = crud.energy_transmission.create(db=db, obj_in=transmission1_request)

    transmission2_request = random_energy_transmission_create(db)
    transmission2_request.ref_dataset = dataset.id
    transmission2_request.commodity = commodity.name
    transmission2 = crud.energy_transmission.create(db=db, obj_in=transmission2_request)

    region1 = crud.region.create(db=db, obj_in=RegionCreate(name=f"Region1-{random_lower_string()}", ref_dataset=dataset.id))
    region2 = crud.region.create(db=db, obj_in=RegionCreate(name=f"Region2-{random_lower_string()}", ref_dataset=dataset.id))

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
