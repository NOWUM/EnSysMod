from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask
from utils.utils import remove_file

from ensysmod import crud, model, schemas
from ensysmod.api import deps, permissions
from ensysmod.core.fine_esm import generate_esm_from_model, myopic_optimize_esm, optimize_esm

router = APIRouter()


@router.get("/{model_id}", response_model=schemas.EnergyModel)
def get_model(
    model_id: int,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Get an energy model by its id.
    """
    model = crud.energy_model.get(db, id=model_id)
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Energy Model {model_id} not found!")

    permissions.check_usage_permission(db=db, user=current_user, dataset_id=model.ref_dataset)

    return model


@router.get("/", response_model=list[schemas.EnergyModel])
def get_energy_model_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all energy models of a dataset.
    """
    permissions.check_usage_permission(db=db, user=current_user, dataset_id=dataset_id)
    return crud.energy_model.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)


@router.post("/", response_model=schemas.EnergyModel, responses={409: {"description": "EnergyModel with same name already exists."}})
def create_model(
    request: schemas.EnergyModelCreate,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Create a new energy model.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_usage_permission(db, user=current_user, dataset_id=request.ref_dataset)

    existing = crud.energy_model.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyModel {request.name} already for dataset {request.ref_dataset} exists!",
        )

    return crud.energy_model.create(db=db, obj_in=request)


@router.put("/{model_id}", response_model=schemas.EnergyModel)
def update_model(
    model_id: int,
    request: schemas.EnergyModelUpdate,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Update an energy model.
    """
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")
    permissions.check_usage_permission(db, user=current_user, dataset_id=energy_model.ref_dataset)
    return crud.energy_model.update(db=db, db_obj=energy_model, obj_in=request)


@router.delete("/{model_id}", response_model=schemas.EnergyModel)
def remove_model(
    model_id: int,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Delete an energy model.
    """
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")
    permissions.check_usage_permission(db, user=current_user, dataset_id=energy_model.ref_dataset)
    return crud.energy_model.remove(db=db, id=model_id)


@router.get("/{model_id}/esm", response_model=schemas.EnergyModel)
def validate_model(
    model_id: int,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Create FINE energy system model from model.

    Might take a while.
    And return errors if dataset is not valid.
    """
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")

    permissions.check_usage_permission(db, user=current_user, dataset_id=energy_model.ref_dataset)

    generate_esm_from_model(db=db, model=energy_model)
    return energy_model


@router.get("/{model_id}/optimize")
def optimize_model(
    model_id: int,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Create FINE energy system model from model and optimizes it.

    Might take a while.
    And return errors if dataset is not valid.
    """
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")

    permissions.check_usage_permission(db, user=current_user, dataset_id=energy_model.ref_dataset)

    esM = generate_esm_from_model(db=db, model=energy_model)
    result_file_path = optimize_esm(esM=esM)

    return FileResponse(
        path=result_file_path,
        media_type="application/vnd.openxmlformats-officedocument. spreadsheetml.sheet",
        filename=f"{energy_model.name}.xlsx",
        background=BackgroundTask(remove_file, result_file_path),
    )


@router.get("/{model_id}/myopic_optimize")
def myopic_optimize_model(
    model_id: int,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Create FINE energy system model from model and optimizes it based on myopic approach.
    """
    energy_model = crud.energy_model.get(db=db, id=model_id)
    if energy_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyModel {model_id} not found!")
    optimization_parameters = crud.energy_model_optimization.get_by_ref_model(db=db, ref_model=model_id)
    if optimization_parameters is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Optimization parameters for EnergyModel {model_id} not found!")

    permissions.check_usage_permission(db, user=current_user, dataset_id=energy_model.ref_dataset)

    esM = generate_esm_from_model(db=db, model=energy_model)
    zipped_result_file_path = myopic_optimize_esm(esM=esM, optimization_parameters=optimization_parameters)

    return FileResponse(
        path=zipped_result_file_path,
        media_type="application/zip",
        filename=f"{energy_model.name} {optimization_parameters.start_year}-{optimization_parameters.end_year}.zip",
        background=BackgroundTask(remove_file, zipped_result_file_path),
    )
