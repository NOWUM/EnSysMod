from pathlib import Path
from shutil import make_archive
from tempfile import mkstemp
from zipfile import ZipFile

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.core.file_upload import process_dataset_zip_archive
from ensysmod.model import Dataset
from ensysmod.schemas import DatasetCreate, FileStatus
from tests.utils.utils import get_current_user_from_headers, get_project_root, random_lower_string


def dataset_create_request(db: Session, current_user_header: dict[str, str], user_id: int | None = None) -> DatasetCreate:
    """
    Generate a dataset create request with the specified user_id.
    If user_id is not specified, the current user is used.
    """
    if user_id is None:
        user_id = get_current_user_from_headers(db, current_user_header).id
    return DatasetCreate(
        name=f"Dataset-{random_lower_string()}",
        description="Dataset description",
        hours_per_time_step=1,
        number_of_time_steps=8760,
        cost_unit="1e9 Euro",
        length_unit="km",
        ref_created_by=user_id,
    )


def dataset_create(db: Session, current_user_header: dict[str, str], user_id: int | None = None) -> Dataset:
    """
    Create a dataset with the specified user_id.
    If user_id is not specified, the current user is used.
    """
    create_request = dataset_create_request(db, current_user_header, user_id)
    return crud.dataset.create(db=db, obj_in=create_request)


def get_dataset_zip(folder_name: str) -> str:
    """
    Create a zip archive from folder structure /examples/datasets/
    """
    root_dir = Path(get_project_root() / "examples" / "datasets" / folder_name)

    _, temp_file_path = mkstemp(prefix="ensysmod_dataset_", suffix=".zip")
    base_name = temp_file_path.removesuffix(".zip")
    return make_archive(base_name=base_name, format="zip", root_dir=root_dir)


def create_example_dataset(db: Session, data_folder: str):
    """
    Create dataset from examples folder.
    """
    # Create dataset
    dataset_name = f"DS-{data_folder}" + random_lower_string()
    dataset_description = "DS desc " + random_lower_string()
    create_request = DatasetCreate(
        name=dataset_name,
        description=dataset_description,
        hours_per_time_step=1,
        number_of_time_steps=8760,
        cost_unit="1e9 Euro",
        length_unit="km",
        ref_created_by=1,
    )
    dataset = crud.dataset.create(db=db, obj_in=create_request)

    # Zip and upload the example dataset from data_folder
    zip_file_path = get_dataset_zip(data_folder)

    with ZipFile(zip_file_path, "r") as zip_archive:
        result = process_dataset_zip_archive(zip_archive, dataset.id, db)
        assert result.status == FileStatus.OK

    return dataset
