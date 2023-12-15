import zipfile
from io import BytesIO
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from ensysmod import crud, model, schemas
from ensysmod.api import deps, permissions
from ensysmod.core.file_download import export_data
from ensysmod.core.file_upload import process_dataset_zip_archive
from ensysmod.schemas import FileStatus
from ensysmod.utils.utils import remove_file

router = APIRouter()


@router.get("/", response_model=List[schemas.Dataset])
def get_all_datasets(db: Session = Depends(deps.get_db),
                     current: model.User = Depends(deps.get_current_user),
                     skip: int = 0,
                     limit: int = 100) -> List[schemas.Dataset]:
    """
    Retrieve all datasets.
    """
    return crud.dataset.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{dataset_id}", response_model=schemas.Dataset)
def get_dataset(dataset_id: int,
                db: Session = Depends(deps.get_db),
                current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a dataset.
    """
    return crud.dataset.get(db=db, id=dataset_id)


@router.post("/", response_model=schemas.Dataset,
             responses={409: {"description": "Dataset with same name already exists."}})
def create_dataset(request: schemas.DatasetCreate,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Create a new dataset.
    """
    existing_ds = crud.dataset.get_by_name(db=db, name=request.name)
    if existing_ds is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Dataset {request.name} already exists!"
                                                                         f"Please choose a different name.")
    request.ref_created_by = current.id
    return crud.dataset.create(db=db, obj_in=request)


@router.put("/{dataset_id}", response_model=schemas.Dataset)
def update_dataset(dataset_id: int,
                   request: schemas.DatasetUpdate,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Update a dataset.
    """
    dataset = crud.dataset.get(db=db, id=dataset_id)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} not found!")
    permissions.check_modification_permission(db=db, user=current, dataset_id=dataset_id)
    return crud.dataset.update(db=db, db_obj=dataset, obj_in=request)


@router.delete("/{dataset_id}", response_model=schemas.Dataset)
def remove_dataset(dataset_id: int,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Delete a dataset.
    """
    permissions.check_modification_permission(db=db, user=current, dataset_id=dataset_id)
    # TODO remove all components, commodities, regions, etc.
    return crud.dataset.remove(db=db, id=dataset_id)


@router.post("/{dataset_id}/upload", response_model=schemas.ZipArchiveUploadResult)
def upload_dataset_zip(dataset_id: int,
                       file: UploadFile = File(...),
                       db: Session = Depends(deps.get_db),
                       current: model.User = Depends(deps.get_current_user)):
    """
    Upload a dataset as zip.
    """
    if file.content_type not in ["application/x-zip-compressed", "application/zip", "application/zip-compressed"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"File must be a zip archive. You provided {file.content_type}!")

    dataset = crud.dataset.get(db=db, id=dataset_id)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} not found!")

    permissions.check_modification_permission(db=db, user=current, dataset_id=dataset_id)

    with zipfile.ZipFile(BytesIO(file.file.read()), 'r') as zip_archive:
        result = process_dataset_zip_archive(zip_archive, dataset_id, db)

        if result.status == FileStatus.ERROR:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(result))

        return result


@router.get("/{dataset_id}/download")
def download_dataset_zip(dataset_id: int,
                         db: Session = Depends(deps.get_db),
                         current: model.User = Depends(deps.get_current_user)):
    """
    Download a dataset as zip.
    """
    dataset = crud.dataset.get(db=db, id=dataset_id)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} not found!")

    permissions.check_usage_permission(db=db, user=current, dataset_id=dataset_id)

    zip_file_path = export_data(db=db, dataset_id=dataset.id)
    return FileResponse(
        path=zip_file_path,
        media_type="application/zip",
        filename=f"{dataset.name}.zip",
        background=BackgroundTask(remove_file, zip_file_path),
    )
