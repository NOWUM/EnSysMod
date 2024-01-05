from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud, model, schemas
from ensysmod.api import deps, permissions

router = APIRouter()


@router.get("/", response_model=list[schemas.EnergyTransmission])
def get_all_energy_transmissions(
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.EnergyTransmission]:
    """
    Retrieve all energy transmissions.
    """
    return crud.energy_transmission.get_multi(db=db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.EnergyTransmission, responses={409: {"description": "EnergyTransmission with same name already exists."}})
def create_transmission(
    request: schemas.EnergyTransmissionCreate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Create a new energy transmission.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=request.ref_dataset)

    existing = crud.energy_transmission.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyTransmission {request.name} already for dataset {request.ref_dataset} exists!",
        )

    # Check if energy commodity exists
    commodity = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.commodity)
    if commodity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EnergyCommodity {request.commodity} in dataset {request.ref_dataset} not found!",
        )

    return crud.energy_transmission.create(db=db, obj_in=request)
