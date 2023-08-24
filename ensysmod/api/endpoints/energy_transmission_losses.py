from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud, model
from ensysmod.api import deps, permissions
from ensysmod.schemas import (
    EnergyTransmissionLoss,
    EnergyTransmissionLossCreate,
    EnergyTransmissionLossUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[EnergyTransmissionLoss])
def get_all_transmission_losses(
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> List[EnergyTransmissionLoss]:
    """
    Retrieve all transmission losses.
    """
    return crud.energy_transmission_loss.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{loss_id}", response_model=EnergyTransmissionLoss)
def get_transmission_loss(
    loss_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Retrieve a transmission loss.
    """
    # TODO Check if user has permission for dataset and EnergyTransmissionLoss
    return crud.energy_transmission_loss.get(db=db, id=loss_id)


@router.get("/component/{component_id}", response_model=List[EnergyTransmissionLoss])
def get_transmission_losses_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> Optional[List[EnergyTransmissionLoss]]:
    """
    Retrieve all transmission losses for a given component.
    """
    # TODO Check if user has permission for dataset and EnergyTransmissionLoss
    return crud.energy_transmission_loss.get_by_component(db=db, component_id=component_id)


@router.post("/", response_model=EnergyTransmissionLoss)
def create_transmission_loss(
    request: EnergyTransmissionLossCreate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Create a new transmission loss.
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

    loss_entry = crud.energy_transmission_loss.get_by_component_and_two_regions(
        db=db,
        component_id=component.id,
        region_from_id=region_from.id,
        region_to_id=region_to.id,
    )
    if loss_entry is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyTransmissionLoss for component {component.name} (id {component.id}) from region {region_from.name} (id {region_from.id}) to region {region_to.name} (id {region_to.id}) already exists with id {loss_entry.id}!",  # noqa: E501
        )

    return crud.energy_transmission_loss.create(db=db, obj_in=request)


@router.put("/{loss_id}", response_model=EnergyTransmissionLoss)
def update_transmission_loss(
    loss_id: int,
    request: EnergyTransmissionLossUpdate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Update a transmission loss.
    """
    loss = crud.energy_transmission_loss.get(db=db, id=loss_id)
    if loss is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyTransmissionLoss {loss_id} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=loss.transmission.component.ref_dataset)
    return crud.energy_transmission_loss.update(db=db, db_obj=loss, obj_in=request)


@router.delete("/{loss_id}", response_model=EnergyTransmissionLoss)
def remove_transmission_loss(
    loss_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Delete a transmission loss.
    """
    loss = crud.energy_transmission_loss.get(db=db, id=loss_id)
    if loss is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyTransmissionLoss {loss_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=loss.transmission.component.ref_dataset)
    return crud.energy_transmission_loss.remove(db=db, id=loss_id)


@router.delete("/component/{component_id}", response_model=List[EnergyTransmissionLoss])
def remove_transmission_losses_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Delete all transmission losses for a given component.
    """
    losses = crud.energy_transmission_loss.get_by_component(db=db, component_id=component_id)
    if losses is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyTransmissionLoss for component {component_id} not found!")

    # TODO Check if user has permission for dataset and EnergyTransmissionLoss
    return crud.energy_transmission_loss.remove_by_component(db=db, component_id=component_id)
