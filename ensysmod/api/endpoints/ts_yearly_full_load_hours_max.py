from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud, model, schemas
from ensysmod.api import deps, permissions

router = APIRouter()


@router.get("/", response_model=List[schemas.YearlyFullLoadHourMax])
def get_all_max_yearly_full_load_hours(db: Session = Depends(deps.get_db),
                                       current: model.User = Depends(deps.get_current_user),
                                       skip: int = 0,
                                       limit: int = 100) -> List[schemas.YearlyFullLoadHourMax]:
    """
    Retrieve all YearlyFullLoadHourMax entries.
    """
    return crud.yearly_full_load_hour_max.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{ts_id}", response_model=schemas.YearlyFullLoadHourMax)
def get_max_yearly_full_load_hour(ts_id: int,
                                  db: Session = Depends(deps.get_db),
                                  current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a YearlyFullLoadHourMax entry.
    """
    # TODO Check if user has permission for dataset and YearlyFullLoadHourMax
    return crud.yearly_full_load_hour_max.get(db, ts_id)


@router.post("/", response_model=schemas.YearlyFullLoadHourMax)
def create_max_yearly_full_load_hour(request: schemas.YearlyFullLoadHourMaxCreate,
                                     db: Session = Depends(deps.get_db),
                                     current: model.User = Depends(deps.get_current_user)):
    """
    Create a new YearlyFullLoadHourMax entry.
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

    ts = crud.yearly_full_load_hour_max.get_by_component_and_region(db=db, component_id=component.id, region_id=region.id)
    if ts is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"YearlyFullLoadHourMax for component {component.name} (id {component.id}) and "
                                   f"region {region.name} (id {region.id}) already exists with id {ts.id}!")

    ts_in_base: Optional[List[model.YearlyFullLoadHourMax]] = crud.yearly_full_load_hour_max.get_by_component(db=db, component_id=component.id)
    if ts_in_base is not None:
        # get maximum length max_yearly_full_load_hours in ts_in_base
        max_length = 0
        for ts_in in ts_in_base:
            if ts_in.max_yearly_full_load_hour is not None:
                max_length = max(max_length, len(ts_in.max_yearly_full_load_hour))

        if max_length > 0 and max_length != len(request.max_yearly_full_load_hour):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"YearlyFullLoadHourMax for component {component.name} (id {component.id}) has a length "
                                       f"of {max_length}. Your new time series has {len(request.max_yearly_full_load_hour)} "
                                       f"elements.")

    return crud.yearly_full_load_hour_max.create(db=db, obj_in=request)


@router.put("/{ts_id}", response_model=schemas.YearlyFullLoadHourMax)
def update_max_yearly_full_load_hour(ts_id: int,
                                     request: schemas.YearlyFullLoadHourMaxUpdate,
                                     db: Session = Depends(deps.get_db),
                                     current: model.User = Depends(deps.get_current_user)):
    """
    Update a YearlyFullLoadHourMax entry.
    """
    ts = crud.yearly_full_load_hour_max.get(db=db, id=ts_id)
    if ts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"YearlyFullLoadHourMax {ts_id} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=ts.component.ref_dataset)
    return crud.yearly_full_load_hour_max.update(db=db, db_obj=ts, obj_in=request)


@router.delete("/{ts_id}", response_model=schemas.YearlyFullLoadHourMax)
def remove_max_yearly_full_load_hour(ts_id: int,
                                     db: Session = Depends(deps.get_db),
                                     current: model.User = Depends(deps.get_current_user)):
    """
    Delete a YearlyFullLoadHourMax entry.
    """
    ts = crud.yearly_full_load_hour_max.get(db=db, id=ts_id)
    if ts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"YearlyFullLoadHourMax {ts_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=ts.component.ref_dataset)
    return crud.yearly_full_load_hour_max.remove(db=db, id=ts_id)
