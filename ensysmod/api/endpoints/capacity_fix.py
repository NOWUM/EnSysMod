from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from ensysmod import crud, model
from ensysmod.api import deps, permissions
from ensysmod.core.file_download import dump_excel_file
from ensysmod.core.file_upload import process_excel_file
from ensysmod.model.energy_component import EnergyComponentType
from ensysmod.schemas import (
    CapacityFix,
    CapacityFixCreate,
)
from ensysmod.schemas.file_upload import FileStatus, FileUploadResult
from ensysmod.utils.utils import create_temp_file, remove_file

router = APIRouter()


@router.get("/{entry_id}", response_model=CapacityFix)
def get_capacity_fix(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> CapacityFix:
    """
    Get a CapacityFix by its id.
    """
    entry = crud.capacity_fix.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CapacityFix {entry_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=entry.ref_dataset)

    return entry


@router.get("/dataset/{dataset_id}", response_model=list[CapacityFix])
def get_capacity_fix_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[CapacityFix]:
    """
    Get all CapacityFix of a dataset.
    """
    entry_list = crud.capacity_fix.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CapacityFix for dataset {dataset_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=dataset_id)

    return entry_list


@router.get("/component/{component_id}", response_model=list[CapacityFix])
def get_capacity_fix_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> list[CapacityFix] | None:
    """
    Get all CapacityFix of a component.
    """
    entry_list = crud.capacity_fix.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CapacityFix for component {component_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=entry_list[0].ref_dataset)

    return entry_list


@router.post("/", response_model=CapacityFix)
def create_capacity_fix(
    request: CapacityFixCreate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Create a new CapacityFix.
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

    entry = crud.capacity_fix.get_by_component_and_region(db=db, component_id=component.id, region_id=region.id)
    if entry is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"CapacityFix for component {component.name} (id {component.id}) \
                and region {region.name} (id {region.id}) already exists with id {entry.id}!"
            ),
        )
    return crud.capacity_fix.create(db=db, obj_in=request)


@router.delete("/{entry_id}", response_model=CapacityFix)
def remove_capacity_fix(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Remove a CapacityFix.
    """
    entry = crud.capacity_fix.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CapacityFix {entry_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=entry.ref_dataset)

    return crud.capacity_fix.remove(db=db, id=entry_id)


@router.delete("/component/{component_id}", response_model=list[CapacityFix])
def remove_capacity_fix_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Remove all CapacityFix of a component.
    """
    entry_list = crud.capacity_fix.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CapacityFix for component {component_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=entry_list[0].ref_dataset)

    return crud.capacity_fix.remove_multi_by_component(db=db, component_id=component_id)


@router.post("/component/{component_id}/upload", response_model=FileUploadResult)
def upload_capacity_fix(
    component_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> FileUploadResult:
    """
    Upload CapacityFix of a component.
    """
    component = crud.energy_component.get(db=db, id=component_id)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {component_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=component.ref_dataset)

    result = process_excel_file(
        file=file,
        db=db,
        dataset_id=component.ref_dataset,
        component_name=component.name,
        crud_repo=crud.capacity_fix,
        create_schema=CapacityFixCreate,
        as_list=False,
        as_matrix=(component.type == EnergyComponentType.TRANSMISSION),
    )
    if result.status != FileStatus.OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(result))

    return result


@router.get("/component/{component_id}/download")
def download_capacity_fix(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> FileResponse:
    """
    Download CapacityFix of a component.
    """
    component = crud.energy_component.get(db=db, id=component_id)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {component_id} not found!")

    temp_file_path = create_temp_file(prefix="ensysmod_capacityFix_", suffix=".xlsx")
    dump_excel_file(
        db=db,
        component_id=component.id,
        crud_repo=crud.capacity_fix,
        file_path=temp_file_path,
    )
    return FileResponse(
        path=temp_file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{component}-capacityFix.xlsx",
        background=BackgroundTask(remove_file, temp_file_path),
    )
