from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.api import deps, permissions
from ensysmod.model import EnergyCommodity, User
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionSchema

router = APIRouter()


@router.get("/", response_model=list[EnergyConversionSchema])
def get_energy_conversion_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all energy conversions of a dataset.
    """
    permissions.check_usage_permission(db=db, user=current_user, dataset_id=dataset_id)
    return crud.energy_conversion.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)


@router.post("/", response_model=EnergyConversionSchema, responses={409: {"description": "EnergyConversion with same name already exists."}})
def create_conversion(
    request: EnergyConversionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new energy conversion.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current_user, dataset_id=request.ref_dataset)

    existing = crud.energy_conversion.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyConversion {request.name} already exists in dataset {request.ref_dataset}!",
        )

    # Check if physical unit is a unit of commodity in the dataset
    commodities: list[EnergyCommodity] = crud.energy_commodity.get_multi_by_dataset(db=db, dataset_id=request.ref_dataset)
    commodity_units: list[str] = [commodity.unit for commodity in commodities]
    if request.physical_unit not in commodity_units:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Physical unit {request.physical_unit} not found in dataset {request.ref_dataset}!",
        )

    # TODO Check commodities for conversion factors

    return crud.energy_conversion.create(db=db, obj_in=request)
