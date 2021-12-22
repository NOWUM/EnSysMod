from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyTransmission
from ensysmod.schemas import EnergyTransmissionCreate
from ensysmod.schemas.energy_transmission_distance import EnergyTransmissionDistanceCreate
from tests.utils.data_generator import fixed_existing_dataset, fixed_existing_energy_commodity
from tests.utils.data_generator.regions import fixed_existing_region, fixed_alternative_existing_region, \
    fixed_alternative_alternative_existing_region
from tests.utils.utils import random_lower_string


def random_energy_transmission_create(db: Session) -> EnergyTransmissionCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    region = fixed_existing_region(db)
    region_to = fixed_alternative_existing_region(db)
    region_to_alt = fixed_alternative_alternative_existing_region(db)
    return EnergyTransmissionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyTransmission-{dataset.id}-{random_lower_string()}",
        description="Description",
        commodity=commodity.name,
        loss_per_unit=0.000001,
        distances=[
            EnergyTransmissionDistanceCreate(
                distance=42.3,
                ref_region_from=region.id,
                region_to=region_to.name,
            ),
            EnergyTransmissionDistanceCreate(
                distance=44.3,
                region_from=region.name,
                ref_region_to=region_to_alt.id,
            )
        ]
    )


def random_existing_energy_transmission(db: Session) -> EnergyTransmission:
    create_request = random_energy_transmission_create(db)
    return crud.energy_transmission.create(db=db, obj_in=create_request)


def fixed_energy_transmission_create(db: Session) -> EnergyTransmissionCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    region = fixed_existing_region(db)
    region_to = fixed_existing_region(db)
    return EnergyTransmissionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyTransmission-{dataset.id}-Fixed",
        description="Description",
        commodity=commodity.name,
        distances=[
            EnergyTransmissionDistanceCreate(
                distance=42.3,
                ref_region_from=region.id,
                ref_region_to=region_to.id,
            )
        ]
    )


def fixed_existing_energy_transmission(db: Session) -> EnergyTransmission:
    create_request = fixed_energy_transmission_create(db)
    transmission = crud.energy_transmission.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset,
                                                                    name=create_request.name)
    if transmission is None:
        transmission = crud.energy_transmission.create(db=db, obj_in=create_request)
    return transmission
