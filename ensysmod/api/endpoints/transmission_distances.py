from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from ensysmod import crud, model
from ensysmod.api import deps, permissions
from ensysmod.core.file_download import dump_excel_file
from ensysmod.core.file_upload import process_excel_file
from ensysmod.schemas import TransmissionDistance, TransmissionDistanceCreate
from ensysmod.schemas.file_upload import FileStatus, FileUploadResult
from ensysmod.utils.utils import create_temp_file, remove_file

router = APIRouter()


@router.get("/{entry_id}", response_model=TransmissionDistance)
def get_transmission_distance(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> TransmissionDistance:
    """
    Get a TransmissionDistance by its id.
    """
    entry = crud.transmission_distance.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TransmissionDistance {entry_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=entry.ref_dataset)

    return entry


@router.get("/dataset/{dataset_id}", response_model=list[TransmissionDistance])
def get_transmission_distance_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[TransmissionDistance]:
    """
    Get all TransmissionDistance of a dataset.
    """
    entry_list = crud.transmission_distance.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TransmissionDistance for dataset {dataset_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=dataset_id)

    return entry_list


@router.get("/component/{component_id}", response_model=list[TransmissionDistance])
def get_transmission_distance_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> list[TransmissionDistance] | None:
    """
    Get all TransmissionDistance of a component.
    """
    entry_list = crud.transmission_distance.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TransmissionDistance for component {component_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=entry_list[0].ref_dataset)

    return entry_list


@router.post("/", response_model=TransmissionDistance)
def create_transmission_distance(
    request: TransmissionDistanceCreate,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Create a new TransmissionDistance.
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

    region_to = crud.region.get_by_dataset_and_name(db=db, dataset_id=dataset.id, name=request.region_to)
    if region_to is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {request.region_to} not found in dataset {dataset.id}!")

    entry = crud.transmission_distance.get_by_component_and_2_regions(
        db=db,
        component_id=component.id,
        region_id=region.id,
        region_to_id=region_to.id,
    )
    if entry is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"TransmissionDistance for component {component.name} (id {component.id}) \
                from region {region.name} (id {region.id}) to region {region_to.name} (id {region_to.id}) \
                already exists with id {entry.id}!"
            ),
        )
    return crud.transmission_distance.create(db=db, obj_in=request)


@router.delete("/{entry_id}", response_model=TransmissionDistance)
def remove_transmission_distance(
    entry_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Remove a TransmissionDistance.
    """
    entry = crud.transmission_distance.get(db=db, id=entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TransmissionDistance {entry_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=entry.ref_dataset)

    return crud.transmission_distance.remove(db=db, id=entry_id)


@router.delete("/component/{component_id}", response_model=list[TransmissionDistance])
def remove_transmission_distance_by_component(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
):
    """
    Remove all TransmissionDistance of a component.
    """
    entry_list = crud.transmission_distance.get_multi_by_component(db=db, component_id=component_id)
    if len(entry_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TransmissionDistance for component {component_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=entry_list[0].ref_dataset)

    return crud.transmission_distance.remove_multi_by_component(db=db, component_id=component_id)


@router.post("/component/{component_id}/upload", response_model=FileUploadResult)
def upload_transmission_distance(
    component_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> FileUploadResult:
    """
    Upload TransmissionDistance of a component.
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
        crud_repo=crud.transmission_distance,
        create_schema=TransmissionDistanceCreate,
        as_list=False,
        as_matrix=True,
    )
    if result.status != FileStatus.OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(result))

    return result


@router.get("/component/{component_id}/download")
def download_transmission_distance(
    component_id: int,
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
) -> FileResponse:
    """
    Download TransmissionDistance of a component.
    """
    component = crud.energy_component.get(db=db, id=component_id)
    if component is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Component {component_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=component.ref_dataset)

    temp_file_path = create_temp_file(prefix="ensysmod_distances_", suffix=".xlsx")
    dump_excel_file(
        db=db,
        component_id=component.id,
        crud_repo=crud.transmission_distance,
        file_path=temp_file_path,
    )
    return FileResponse(
        path=temp_file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{component}-distances.xlsx",
        background=BackgroundTask(remove_file, temp_file_path),
    )
