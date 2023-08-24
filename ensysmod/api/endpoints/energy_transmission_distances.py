from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud, model
from ensysmod.api import deps, permissions
from ensysmod.schemas import (
    EnergyTransmissionDistance,
    EnergyTransmissionDistanceCreate,
    EnergyTransmissionDistanceUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[EnergyTransmissionDistance])
def get_all_transmission_distances(
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> List[EnergyTransmissionDistance]:
    """
    Retrieve all transmission distances.
    """
    return crud.energy_transmission_distance.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{distance_id}", response_model=EnergyTransmissionDistance)
def get_transmission_distance(
    distance_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Retrieve a transmission distance.
    """
    # TODO Check if user has permission for dataset and EnergyTransmissionDistance
    return crud.energy_transmission_distance.get(db=db, id=distance_id)


@router.get("/component/{component_id}", response_model=List[EnergyTransmissionDistance])
def get_transmission_distances_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> Optional[List[EnergyTransmissionDistance]]:
    """
    Retrieve all transmission distances for a given component.
    """
    # TODO Check if user has permission for dataset and EnergyTransmissionDistance
    return crud.energy_transmission_distance.get_by_component(db=db, component_id=component_id)


@router.post("/", response_model=EnergyTransmissionDistance)
def create_transmission_distance(
    request: EnergyTransmissionDistanceCreate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Create a new transmission distance.
    """
    permissions.check_modification_permission(db, user=current, dataset_id=request.ref_dataset)

    component = crud.energy_component.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.component)
    if component is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {request.component} not found in dataset {request.ref_dataset}!"
        )

    region_from = crud.region.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.region_from)
    if region_from is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {request.region_from} not found in dataset {request.ref_dataset}!")

    region_to = crud.region.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.region_to)
    if region_to is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {request.region_to} not found in dataset {request.ref_dataset}!")

    distance_entry = crud.energy_transmission_distance.get_by_component_and_two_regions(
        db=db,
        component_id=component.id,
        region_from_id=region_from.id,
        region_to_id=region_to.id,
    )
    if distance_entry is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyTransmissionDistance for component {component.name} (id {component.id}) from region {region_from.name} (id {region_from.id}) to region {region_to.name} (id {region_to.id}) already exists with id {distance_entry.id}!",  # noqa: E501
        )

    return crud.energy_transmission_distance.create(db=db, obj_in=request)


@router.put("/{distance_id}", response_model=EnergyTransmissionDistance)
def update_transmission_distance(
    distance_id: int,
    request: EnergyTransmissionDistanceUpdate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Update a transmission distance.
    """
    distance = crud.energy_transmission_distance.get(db=db, id=distance_id)
    if distance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyTransmissionDistance {distance_id} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=distance.transmission.component.ref_dataset)
    return crud.energy_transmission_distance.update(db=db, db_obj=distance, obj_in=request)


@router.delete("/{distance_id}", response_model=EnergyTransmissionDistance)
def remove_transmission_distance(
    distance_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Delete a transmission distance.
    """
    distance = crud.energy_transmission_distance.get(db=db, id=distance_id)
    if distance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyTransmissionDistance {distance_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=distance.transmission.component.ref_dataset)
    return crud.energy_transmission_distance.remove(db=db, id=distance_id)


@router.delete("/component/{component_id}", response_model=List[EnergyTransmissionDistance])
def remove_transmission_distances_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Delete all transmission distances for a given component.
    """
    distances = crud.energy_transmission_distance.get_by_component(db=db, component_id=component_id)
    if distances is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyTransmissionDistance for component {component_id} not found!")

    # TODO Check if user has permission for dataset and EnergyTransmissionDistance
    return crud.energy_transmission_distance.remove_by_component(db=db, component_id=component_id)
