from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from ensysmod import crud
from ensysmod.api import deps, permissions
from ensysmod.core.file_download import dump_excel_file
from ensysmod.core.file_upload import process_excel_file
from ensysmod.model import EnergyComponentType, User
from ensysmod.schemas import FileStatus, FileUploadResult, YearlyFullLoadHoursMinCreate, YearlyFullLoadHoursMinSchema
from ensysmod.utils.utils import create_temp_file, remove_file

router = APIRouter()


@router.get("/{entry_id}", response_model=YearlyFullLoadHoursMinSchema)
def get_yearly_full_load_hours_min(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get a YearlyFullLoadHoursMin by its id.
    """
    entry = crud.yearly_full_load_hours_min.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"YearlyFullLoadHoursMin {entry_id} not found!")

    permissions.check_usage_permission(db=db, user=current_user, dataset_id=entry.ref_dataset)

    return entry


@router.get("/dataset/{dataset_id}", response_model=list[YearlyFullLoadHoursMinSchema])
def get_yearly_full_load_hours_min_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all YearlyFullLoadHoursMin of a dataset.
    """
    entry_list = crud.yearly_full_load_hours_min.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"YearlyFullLoadHoursMin for dataset {dataset_id} not found!")

    permissions.check_usage_permission(db=db, user=current_user, dataset_id=dataset_id)

    return entry_list


@router.get("/component/{component_id}", response_model=list[YearlyFullLoadHoursMinSchema])
def get_yearly_full_load_hours_min_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get all YearlyFullLoadHoursMin of a component.
    """
    entry_list = crud.yearly_full_load_hours_min.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"YearlyFullLoadHoursMin for component {component_id} not found!")

    permissions.check_usage_permission(db=db, user=current_user, dataset_id=entry_list[0].ref_dataset)

    return entry_list


@router.post("/", response_model=YearlyFullLoadHoursMinSchema)
def create_yearly_full_load_hours_min(
    request: YearlyFullLoadHoursMinCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new YearlyFullLoadHoursMin.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db=db, user=current_user, dataset_id=dataset.id)

    component = crud.energy_component.get_by_dataset_and_name(db=db, dataset_id=dataset.id, name=request.component_name)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {request.component_name} not found in dataset {dataset.id}!")

    region = crud.region.get_by_dataset_and_name(db=db, dataset_id=dataset.id, name=request.region_name)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {request.region_name} not found in dataset {dataset.id}!")

    entry = crud.yearly_full_load_hours_min.get_by_component_and_region(db=db, component_id=component.id, region_id=region.id)
    if entry is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"YearlyFullLoadHoursMin for component {component.name} (id {component.id}) \
                and region {region.name} (id {region.id}) already exists with id {entry.id}!"
            ),
        )
    return crud.yearly_full_load_hours_min.create(db=db, obj_in=request)


@router.delete("/{entry_id}", response_model=YearlyFullLoadHoursMinSchema)
def remove_yearly_full_load_hours_min(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Remove a YearlyFullLoadHoursMin.
    """
    entry = crud.yearly_full_load_hours_min.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"YearlyFullLoadHoursMin {entry_id} not found!")

    permissions.check_modification_permission(db=db, user=current_user, dataset_id=entry.ref_dataset)

    return crud.yearly_full_load_hours_min.remove(db=db, id=entry_id)


@router.delete("/component/{component_id}", response_model=list[YearlyFullLoadHoursMinSchema])
def remove_yearly_full_load_hours_min_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Remove all YearlyFullLoadHoursMin of a component.
    """
    entry_list = crud.yearly_full_load_hours_min.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"YearlyFullLoadHoursMin for component {component_id} not found!")

    permissions.check_modification_permission(db=db, user=current_user, dataset_id=entry_list[0].ref_dataset)

    return crud.yearly_full_load_hours_min.remove_multi_by_component(db=db, component_id=component_id)


@router.post("/component/{component_id}/upload", response_model=FileUploadResult)
def upload_yearly_full_load_hours_min(
    component_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Upload YearlyFullLoadHoursMin of a component.
    """
    component = crud.energy_component.get(db=db, id=component_id)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {component_id} not found!")

    permissions.check_modification_permission(db=db, user=current_user, dataset_id=component.ref_dataset)

    result = process_excel_file(
        file=file,
        db=db,
        dataset_id=component.ref_dataset,
        component_name=component.name,
        crud_repo=crud.yearly_full_load_hours_min,
        create_schema=YearlyFullLoadHoursMinCreate,
        as_list=False,
        as_matrix=(component.type == EnergyComponentType.TRANSMISSION),
    )
    if result.status != FileStatus.OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(result))

    return result


@router.get("/component/{component_id}/download")
def download_yearly_full_load_hours_min(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Download YearlyFullLoadHoursMin of a component.
    """
    component = crud.energy_component.get(db=db, id=component_id)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {component_id} not found!")

    permissions.check_usage_permission(db=db, user=current_user, dataset_id=component.ref_dataset)

    temp_file_path = create_temp_file(prefix="ensysmod_yearlyFullLoadHoursMin_", suffix=".xlsx")
    dump_excel_file(
        db=db,
        component_id=component.id,
        crud_repo=crud.yearly_full_load_hours_min,
        file_path=temp_file_path,
    )
    return FileResponse(
        path=temp_file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{component}-yearlyFullLoadHoursMin.xlsx",
        background=BackgroundTask(remove_file, temp_file_path),
    )
