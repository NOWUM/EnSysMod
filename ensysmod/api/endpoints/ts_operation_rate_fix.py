from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps, permissions
from ensysmod.schemas import OperationRateFix

router = APIRouter()


@router.get("/", response_model=List[schemas.OperationRateFix])
def all_fix_operation_rates(db: Session = Depends(deps.get_db),
                            current: model.User = Depends(deps.get_current_user),
                            skip: int = 0,
                            limit: int = 100) -> List[schemas.OperationRateFix]:
    """
    Retrieve all fix operation rates.
    """
    return crud.operation_rate_fix.get_multi(db, skip=skip, limit=limit)


@router.get("/{ts_id}", response_model=schemas.OperationRateFix)
def get_operation_rate_fix(ts_id: int,
                           db: Session = Depends(deps.get_db),
                           current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a fix operation rate.
    """
    return crud.operation_rate_fix.get(db, ts_id)


@router.post("/", response_model=schemas.OperationRateFix)
def create_operation_rate_fix(request: schemas.OperationRateFixCreate,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Create a new fix operation rate.
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

    ts = crud.operation_rate_fix.get_by_component_and_region(db=db, component_id=component.id, region_id=region.id)
    if ts is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"OperationRateFix for component {component.name} (id {component.id}) and "
                                   f"region {region.name} (id {region.id}) already exists with id {ts.id}!")

    ts_in_base: Optional[List[OperationRateFix]] = crud.operation_rate_fix.get_by_component(db=db,
                                                                                            component_id=component.id)
    if ts_in_base is not None:
        # get maximum length fix_operation_rates in ts_in_base
        max_length = 0
        for ts_in in ts_in_base:
            if ts_in.fix_operation_rates is not None:
                max_length = max(max_length, len(ts_in.fix_operation_rates))

        if max_length > 0 and max_length != len(request.fix_operation_rates):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"OperationRateFix for component {component.name} (id {component.id}) has a "
                                       f"length of {max_length}. Your new time series has "
                                       f"{len(request.fix_operation_rates)} elements.")

    return crud.operation_rate_fix.create(db=db, obj_in=request)


@router.put("/{ts_id}", response_model=schemas.OperationRateFix)
def update_operation_rate_fix(ts_id: int,
                              request: schemas.OperationRateFixUpdate,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Update a fix operation rate.
    """
    ts = crud.operation_rate_fix.get(db=db, id=ts_id)
    if ts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OperationRateFix {ts_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=ts.component.ref_dataset)
    return crud.operation_rate_fix.update(db=db, db_obj=ts, obj_in=request)


@router.delete("/{ts_id}", response_model=schemas.OperationRateFix)
def remove_operation_rate_fix(ts_id: int,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Delete a fix operation rate.
    """
    ts = crud.operation_rate_fix.get(db=db, id=ts_id)
    if ts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OperationRateFix {ts_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=ts.component.ref_dataset)
    return crud.operation_rate_fix.remove(db=db, id=ts_id)
