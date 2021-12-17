from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyConversion
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionFactorCreate
from tests.utils.data_generator.datasets import fixed_existing_dataset
from tests.utils.data_generator.energy_commodities import fixed_existing_energy_commodity
from tests.utils.utils import random_lower_string


def random_energy_conversion_create(db: Session) -> EnergyConversionCreate:
    """
    Generate a random EnergyConversionCreate object.
    """
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyConversionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyConversion-{dataset.id}-{random_lower_string()}",
        description="Description",
        commodity_unit=commodity.name,
        conversion_factors=[EnergyConversionFactorCreate(commodity=commodity.name, conversion_factor=1.0)]
    )


def random_existing_energy_conversion(db: Session) -> EnergyConversion:
    """
    Generate a random EnergyConversion object.
    """
    create_request = random_energy_conversion_create(db)
    return crud.energy_conversion.create(db=db, obj_in=create_request)


def fixed_energy_conversion_create(db: Session) -> EnergyConversionCreate:
    """
    Generate a fixed EnergyConversionCreate object.
    Will always return the same object.
    """
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyConversionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyConversion-{dataset.id}-Fixed",
        description="Description",
        commodity_unit=commodity.name,
        conversion_factors=[EnergyConversionFactorCreate(commodity=commodity.name, conversion_factor=1.0)]
    )


def fixed_existing_energy_conversion(db: Session) -> EnergyConversion:
    """
    Generate a fixed EnergyConversion object.
    Will always return the same object.
    """
    create_request = fixed_energy_conversion_create(db)
    conversion = crud.energy_conversion.get_by_dataset_and_name(db, dataset_id=create_request.ref_dataset,
                                                                name=create_request.name)
    if conversion is None:
        conversion = crud.energy_conversion.create(db=db, obj_in=create_request)
    return conversion
