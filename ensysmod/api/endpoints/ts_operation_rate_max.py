from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps
from ensysmod.schemas import OperationRateMax

router = APIRouter()


@router.get("/", response_model=List[schemas.OperationRateMax])
def all_max_operation_rates(db: Session = Depends(deps.get_db),
                            current: model.User = Depends(deps.get_current_user),
                            skip: int = 0,
                            limit: int = 100) -> List[schemas.OperationRateMax]:
    """
    Retrieve all max operation rates.
    """
    return crud.operation_rate_max.get_multi(db, skip=skip, limit=limit)


@router.get("/{ts_id}", response_model=schemas.OperationRateMax)
def get_operation_rate_max(ts_id: int,
                           db: Session = Depends(deps.get_db),
                           current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a max operation rate.
    """
    # TODO Check if user has permission for dataset and OperationRateMax
    return crud.operation_rate_max.get(db, ts_id)


@router.post("/", response_model=schemas.OperationRateMax)
def create_operation_rate_max(request: schemas.OperationRateMaxCreate,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Create a new max operation rate.
    """
    component = crud.energy_component.get(db=db, id=request.ref_component)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Component {request.ref_component} not found!")

    # TODO Check if user has permission for dataset

    region = crud.region.get(db=db, id=request.ref_region)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Region {request.ref_region} not found!")

    if component.ref_dataset != region.ref_dataset:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Component (id {request.ref_component}, dataset {component.ref_dataset}) and "
                                   f"region (id {request.ref_region}, dataset {region.ref_dataset}) does not belong to "
                                   f"same dataset!")

    ts = crud.operation_rate_max.get_by_component_and_region(db=db, component_id=request.ref_component,
                                                             region_id=request.ref_region)
    if ts is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"OperationRateMax for component {component.name} (id {component.id}) and "
                                   f"region {region.name} (id {region.id}) already exists with id {ts.id}!")

    ts_in_base: Optional[List[OperationRateMax]] = crud.operation_rate_max.get_by_component(db=db,
                                                                                            component_id=request.ref_component)
    if ts_in_base is not None:
        # get maximum length max_operation_rates in ts_in_base
        max_length = 0
        for ts_in in ts_in_base:
            if ts_in.max_operation_rates is not None:
                max_length = max(max_length, len(ts_in.max_operation_rates))

        if max_length > 0 and max_length != len(request.max_operation_rates):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"OperationRateMax for component {component.name} (id {component.id}) has a "
                                       f"length of {max_length}. Your new time series has "
                                       f"{len(request.max_operation_rates)} elements.")

    return crud.operation_rate_max.create(db=db, obj_in=request)


@router.put("/{ts_id}", response_model=schemas.OperationRateMax)
def update_operation_rate_max(ts_id: int,
                              request: schemas.OperationRateMaxUpdate,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Update a max operation rate.
    """
    # TODO Check if user has permission for OperationRateMax
    ts = crud.operation_rate_max.get(db=db, id=ts_id)
    if ts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OperationRateMax {ts_id} not found!")
    return crud.operation_rate_max.update(db=db, db_obj=ts, obj_in=request)


@router.delete("/{ts_id}", response_model=schemas.OperationRateMax)
def remove_operation_rate_max(ts_id: int,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Delete a max operation rate.
    """
    ts = crud.operation_rate_max.get(db=db, id=ts_id)
    if ts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OperationRateMax {ts_id} not found!")
    # TODO Check if user has permission for dataset
    return crud.operation_rate_max.remove(db=db, id=ts_id)
