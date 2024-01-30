from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.api import deps, permissions
from ensysmod.model import User
from ensysmod.schemas import EnergyTransmissionCreate, EnergyTransmissionSchema

router = APIRouter()


@router.get("/", response_model=list[EnergyTransmissionSchema])
def get_energy_transmission_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all energy transmissions of a dataset.
    """
    permissions.check_usage_permission(db=db, user=current_user, dataset_id=dataset_id)
    return crud.energy_transmission.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)


@router.post("/", response_model=EnergyTransmissionSchema, responses={409: {"description": "EnergyTransmission with same name already exists."}})
def create_transmission(
    request: EnergyTransmissionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new energy transmission.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current_user, dataset_id=request.ref_dataset)

    existing = crud.energy_transmission.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyTransmission {request.name} already exists in dataset {request.ref_dataset}!",
        )

    # Check if energy commodity exists
    commodity = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.commodity)
    if commodity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EnergyCommodity {request.commodity} not found in dataset {request.ref_dataset}!",
        )

    return crud.energy_transmission.create(db=db, obj_in=request)
