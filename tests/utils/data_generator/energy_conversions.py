from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyCommodity, EnergyConversion
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionFactorCreate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import new_commodity
from tests.utils.utils import random_string


def conversion_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergyConversionCreate:
    """
    Generate a conversion create request with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header).id
    if commodity is None:
        commodity = new_commodity(db, user_header, dataset_id=dataset_id)
    return EnergyConversionCreate(
        ref_dataset=dataset_id,
        name=f"EnergyConversion-Dataset{dataset_id}-{random_string()}",
        description=None,
        physical_unit=commodity.unit,
        conversion_factors=[EnergyConversionFactorCreate(commodity_name=commodity.name, conversion_factor=1.0)],
    )


def new_conversion(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergyConversion:
    """
    Create a conversion component with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    create_request = conversion_create_request(db, user_header, dataset_id=dataset_id, commodity=commodity)
    return crud.energy_conversion.create(db=db, obj_in=create_request)
