from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps, permissions
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
    return crud.operation_rate_max.get(db, ts_id)


@router.post("/", response_model=schemas.OperationRateMax)
def create_operation_rate_max(request: schemas.OperationRateMaxCreate,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Create a new max operation rate.
    """
    component = crud.energy_component.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset,
                                                              name=request.component)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Component {request.component} not found in dataset {request.ref_dataset}!")

    permissions.check_modification_permission(db, user=current, dataset_id=request.ref_dataset)

    region = crud.region.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.region)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Region {request.region} not found in dataset {request.ref_dataset}!")

    ts = crud.operation_rate_max.get_by_component_and_region(db=db, component_id=component.id, region_id=region.id)
    if ts is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"OperationRateMax for component {component.name} (id {component.id}) and "
                                   f"region {region.name} (id {region.id}) already exists with id {ts.id}!")

    ts_in_base: Optional[List[OperationRateMax]] = crud.operation_rate_max.get_by_component(db=db,
                                                                                            component_id=component.id)
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
    ts = crud.operation_rate_max.get(db=db, id=ts_id)
    if ts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OperationRateMax {ts_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=ts.component.ref_dataset)
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
    permissions.check_modification_permission(db, user=current, dataset_id=ts.component.ref_dataset)
    return crud.operation_rate_max.remove(db=db, id=ts_id)
