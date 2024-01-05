from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud, model, schemas
from ensysmod.api import deps, permissions

router = APIRouter()


@router.get("/", response_model=list[schemas.EnergySource])
def get_all_energy_sources(
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.EnergySource]:
    """
    Retrieve all energy sources.
    """
    return crud.energy_source.get_multi(db=db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.EnergySource, responses={409: {"description": "EnergySource with same name already exists."}})
def create_source(
    request: schemas.EnergySourceCreate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Create a new energy source.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=request.ref_dataset)

    existing = crud.energy_source.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergySource {request.name} already for dataset {request.ref_dataset} exists!",
        )

    # Check if energy commodity exists
    commodity = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.commodity)
    if commodity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EnergyCommodity {request.commodity} in dataset {request.ref_dataset} not found!",
        )

    return crud.energy_source.create(db=db, obj_in=request)
