from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps
from ensysmod.core.fine_esm import generate_esm_from_model, optimize_esm

router = APIRouter()


@router.get("/", response_model=List[schemas.EnergyModel])
def all_models(db: Session = Depends(deps.get_db),
               current: model.User = Depends(deps.get_current_user),
               skip: int = 0,
               limit: int = 100,
               dataset: Union[None, int] = None) -> List[schemas.EnergyModel]:
    """
    Retrieve all energy models.
    """
    if dataset is None:
        return crud.energy_model.get_multi(db, skip=skip, limit=limit)
    else:
        return crud.energy_model.get_multi_by_dataset(db, dataset_id=dataset, skip=skip, limit=limit)


@router.get("/{model_id}", response_model=schemas.EnergyModel)
def get_model(model_id: int,
              db: Session = Depends(deps.get_db),
              current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a energy model.
    """
    # TODO Check if user has permission for dataset and model
    return crud.energy_model.get(db, id=model_id)


@router.post("/", response_model=schemas.EnergyModel,
             responses={409: {"description": "EnergyModel with same name already exists."}})
def create_model(request: schemas.EnergyModelCreate,
                 db: Session = Depends(deps.get_db),
                 current: model.User = Depends(deps.get_current_user)):
    """
    Create a new energy model.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    # TODO Check if user has permission for dataset

    existing = crud.energy_model.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"EnergyModel {request.name} already for dataset {request.ref_dataset} exists!")

    return crud.energy_model.create(db=db, obj_in=request)


@router.put("/{model_id}", response_model=schemas.EnergyModel)
def update_model(model_id: int,
                 request: schemas.EnergyModelUpdate,
                 db: Session = Depends(deps.get_db),
                 current: model.User = Depends(deps.get_current_user)):
    """
    Update a energy model.
    """
    # TODO Check if user has permission for model
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")
    return crud.energy_model.update(db=db, db_obj=energy_model, obj_in=request)


@router.delete("/{model_id}", response_model=schemas.EnergyModel)
def remove_model(model_id: int,
                 db: Session = Depends(deps.get_db),
                 current: model.User = Depends(deps.get_current_user)):
    """
    Delete a energy model.
    """
    # TODO Check if user has permission for dataset
    return crud.energy_model.remove(db=db, id=model_id)


@router.get("/{model_id}/esm", response_model=schemas.EnergyModel)
def validate_model(model_id: int,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Create FINE energy system model from model.

    Might take a while.
    And return errors if dataset is not valid.
    """
    # TODO Check if user has permission for dataset
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")

    # TODO Check if user has permission for dataset

    generate_esm_from_model(db=db, model=energy_model)
    return energy_model


@router.get("/{model_id}/optimize")
def optimize_model(model_id: int,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Create FINE energy system model from model and optimizes it.

    Might take a while.
    And return errors if dataset is not valid.
    """
    # TODO Check if user has permission for dataset
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")

    # TODO Check if user has permission for dataset

    esM = generate_esm_from_model(db=db, model=energy_model)
    result_file_path = optimize_esm(esM=esM)

    return FileResponse(result_file_path,
                        media_type="application/vnd.openxmlformats-officedocument. spreadsheetml.sheet",
                        filename=f"{energy_model.name}.xlsx")
