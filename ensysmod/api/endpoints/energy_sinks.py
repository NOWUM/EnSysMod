from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.EnergySink])
def all_energy_sinks(db: Session = Depends(deps.get_db),
                     current: model.User = Depends(deps.get_current_user),
                     skip: int = 0,
                     limit: int = 100) -> List[schemas.EnergySink]:
    """
    Retrieve all energy sinks.
    """
    return crud.energy_sink.get_multi(db, skip, limit)


@router.post("/", response_model=schemas.EnergySink,
             responses={409: {"description": "EnergySink with same name already exists."}})
def create_sink(request: schemas.EnergySinkCreate,
                db: Session = Depends(deps.get_db),
                current: model.User = Depends(deps.get_current_user)):
    """
    Create a new energy sink.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    # TODO Check if user has permission for dataset

    existing = crud.energy_sink.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"EnergySink {request.name} already for dataset {request.ref_dataset} exists!")

    # Check if energy commodity exists
    commodity = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset,
                                                              name=request.commodity)
    if commodity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"EnergyCommodity {request.commodity} in dataset {request.ref_dataset} not found!")

    return crud.energy_sink.create(db=db, obj_in=request)
