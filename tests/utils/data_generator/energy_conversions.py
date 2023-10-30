from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyConversion
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionFactorCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.utils import random_lower_string


def conversion_create_request(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyConversionCreate:
    """
    Generate a conversion create request with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    if commodity_name is None:
        commodity_name = commodity_create(db, current_user_header, dataset_id).name
    return EnergyConversionCreate(
        ref_dataset=dataset_id,
        name=f"EnergyConversion-Dataset{dataset_id}-{random_lower_string()}",
        description="Description",
        commodity_unit=commodity_name,
        conversion_factors=[EnergyConversionFactorCreate(commodity=commodity_name, conversion_factor=1.0)],
    )


def conversion_create(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyConversion:
    """
    Create a conversion component with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    create_request = conversion_create_request(db, current_user_header, dataset_id, commodity_name)
    return crud.energy_conversion.create(db=db, obj_in=create_request)
