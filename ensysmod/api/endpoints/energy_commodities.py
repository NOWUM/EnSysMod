from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.api import deps, permissions
from ensysmod.model import User
from ensysmod.schemas import EnergyCommodityCreate, EnergyCommoditySchema, EnergyCommodityUpdate

router = APIRouter()


@router.get("/{commodity_id}", response_model=EnergyCommoditySchema)
def get_commodity(
    commodity_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get an energy commodity by its id.
    """
    commodity = crud.energy_commodity.get(db=db, id=commodity_id)
    if commodity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Commodity {commodity_id} not found!")

    permissions.check_usage_permission(db=db, user=current_user, dataset_id=commodity.ref_dataset)

    return commodity


@router.get("/", response_model=list[EnergyCommoditySchema])
def get_commodity_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all energy commodities of a dataset.
    """
    permissions.check_usage_permission(db=db, user=current_user, dataset_id=dataset_id)
    return crud.energy_commodity.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)


@router.post("/", response_model=EnergyCommoditySchema, responses={409: {"description": "EnergyCommodity with same name already exists."}})
def create_commodity(
    request: EnergyCommodityCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new energy commodity.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current_user, dataset_id=request.ref_dataset)

    existing = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyCommodity {request.name} already exists in dataset {request.ref_dataset}!",
        )

    return crud.energy_commodity.create(db=db, obj_in=request)


@router.put("/{commodity_id}", response_model=EnergyCommoditySchema)
def update_commodity(
    commodity_id: int,
    request: EnergyCommodityUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update an energy commodity.
    """
    commodity = crud.energy_commodity.get(db=db, id=commodity_id)
    if commodity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyCommodity {commodity_id} not found!")
    permissions.check_modification_permission(db, user=current_user, dataset_id=commodity.ref_dataset)
    return crud.energy_commodity.update(db=db, db_obj=commodity, obj_in=request)


@router.delete("/{commodity_id}", response_model=EnergyCommoditySchema)
def remove_commodity(
    commodity_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete an energy commodity.
    """
    commodity = crud.energy_commodity.get(db=db, id=commodity_id)
    if commodity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyCommodity {commodity_id} not found!")
    permissions.check_modification_permission(db, user=current_user, dataset_id=commodity.ref_dataset)
    return crud.energy_commodity.remove(db=db, id=commodity_id)
