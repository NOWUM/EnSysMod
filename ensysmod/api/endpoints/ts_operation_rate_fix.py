from pathlib import Path
from tempfile import mkstemp

from core.file_download import dump_excel_file
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ensysmod import crud, model
from ensysmod.api import deps, permissions
from ensysmod.core.file_upload import process_excel_file
from ensysmod.model.energy_component import EnergyComponentType
from ensysmod.schemas import (
    OperationRateFix,
    OperationRateFixCreate,
)
from ensysmod.schemas.file_upload import FileUploadResult

router = APIRouter()


@router.get("/{entry_id}", response_model=OperationRateFix)
def get_fix_operation_rate(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> OperationRateFix:
    """
    Get a fix operation rate by its id.
    """
    entry = crud.operation_rate_fix.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fix operation rate {entry_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=entry.component.ref_dataset)

    return entry


@router.get("/dataset/{dataset_id}", response_model=list[OperationRateFix])
def get_fix_operation_rate_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[OperationRateFix]:
    """
    Get all fix operation rates of a dataset.
    """
    entry_list = crud.operation_rate_fix.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fix operation rate for dataset {dataset_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=dataset_id)

    return entry_list


@router.get("/component/{component_id}", response_model=list[OperationRateFix])
def get_fix_operation_rate_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> list[OperationRateFix] | None:
    """
    Get all fix operation rates of a component.
    """
    entry_list = crud.operation_rate_fix.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fix operation rate for component {component_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=entry_list[0].component.ref_dataset)

    return entry_list


@router.post("/", response_model=OperationRateFix)
def create_fix_operation_rate(
    request: OperationRateFixCreate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Create a new fix operation rate.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=dataset.id)

    component = crud.energy_component.get_by_dataset_and_name(db=db, dataset_id=dataset.id, name=request.component)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {request.component} not found in dataset {dataset.id}!")

    region = crud.region.get_by_dataset_and_name(db=db, dataset_id=dataset.id, name=request.region)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {request.region} not found in dataset {dataset.id}!")

    if len(request.fix_operation_rates) != dataset.number_of_time_steps:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Length of OperationRateFix must match the number of time steps of the dataset. \
                Expected: {dataset.number_of_time_steps}, given: {len(request.fix_operation_rates)}."
            ),
        )

    entry = crud.operation_rate_fix.get_by_component_and_region(db=db, component_id=component.id, region_id=region.id)
    if entry is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"OperationRateFix for component {component.name} (id {component.id}) \
                and region {region.name} (id {region.id}) already exists with id {entry.id}!"
            ),
        )
    return crud.operation_rate_fix.create(db=db, obj_in=request)


@router.delete("/{entry_id}", response_model=OperationRateFix)
def remove_fix_operation_rate(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Remove a fix operation rate.
    """
    entry = crud.operation_rate_fix.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fix operation rate {entry_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=entry.component.ref_dataset)

    return crud.operation_rate_fix.remove(db=db, id=entry_id)


@router.delete("/component/{component_id}", response_model=list[OperationRateFix])
def remove_fix_operation_rate_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Remove all fix operation rates of a component.
    """
    entry_list = crud.operation_rate_fix.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fix operation rate for component {component_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=entry_list[0].component.ref_dataset)

    return crud.operation_rate_fix.remove_multi_by_component(db=db, component_id=component_id)


@router.post("/component/{component_id}/upload", response_model=FileUploadResult)
def upload_fix_operation_rate(
    component_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> FileUploadResult:
    """
    Upload fix operation rates of a component.
    """
    component = crud.energy_component.get(db=db, id=component_id)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {component_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=component.ref_dataset)

    return process_excel_file(
        file=file,
        db=db,
        dataset_id=component.ref_dataset,
        component_name=component.name,
        crud_repo=crud.operation_rate_fix,
        create_schema=OperationRateFixCreate,
        as_list=True,
        as_matrix=(component.type == EnergyComponentType.CONVERSION),
    )


@router.get("/component/{component_id}/download")
def download_fix_operation_rate(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> FileResponse:
    """
    Download fix operation rates of a component.
    """
    component = crud.energy_component.get(db=db, id=component_id)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {component_id} not found!")

    operation_rates = crud.operation_rate_fix.get_multi_by_component(db, component_id=component_id)
    region_ids = [operation_rate.ref_region for operation_rate in operation_rates]

    _, temp_file_path = mkstemp(prefix="ensysmod_operationRateFix_", suffix=".xlsx")
    dump_excel_file(
        db=db,
        component_id=component.id,
        region_ids=region_ids,
        crud_repo=crud.operation_rate_fix,
        file_path=Path(temp_file_path),
    )
    return FileResponse(
        path=Path(temp_file_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{component}-operationRateFix.xlsx",
    )
