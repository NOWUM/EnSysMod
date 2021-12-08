from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyCommodity
from ensysmod.schemas import EnergyCommodityCreate
from tests.utils.data_generator.datasets import fixed_existing_dataset, random_existing_dataset
from tests.utils.utils import random_lower_string


def random_energy_commodity_create(db: Session) -> EnergyCommodityCreate:
    """
    Generate a random energy commodity create request.
    """
    dataset = random_existing_dataset(db)
    return EnergyCommodityCreate(name=f"EnergyCommodity-{dataset.id}-" + random_lower_string(),
                                 ref_dataset=dataset.id,
                                 description="EnergyCommodity description",
                                 unit="kWh")


def random_existing_energy_commodity(db: Session) -> EnergyCommodity:
    """
    Generate a random existing energy commodity.
    """
    create_request = random_energy_commodity_create(db)
    return crud.energy_commodity.create(db=db, obj_in=create_request)


def fixed_energy_commodity_create(db: Session) -> EnergyCommodityCreate:
    """
    Generate a fixed energy commodity create request.
    Will always return the same energy commodity.
    """
    dataset = fixed_existing_dataset(db)
    return EnergyCommodityCreate(name=f"EnergyCommodity-{dataset.id}-Fixed",
                                 ref_dataset=dataset.id,
                                 description="EnergyCommodity description",
                                 unit="kWh")


def fixed_existing_energy_commodity(db: Session) -> EnergyCommodity:
    """
    Generate a fixed existing energy commodity.
    Will always return the same energy commodity.
    """
    create_request = fixed_energy_commodity_create(db)
    commodity = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset,
                                                              name=create_request.name)
    if commodity is None:
        return crud.energy_commodity.create(db=db, obj_in=create_request)
    return commodity
