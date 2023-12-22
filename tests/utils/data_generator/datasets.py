from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from shutil import make_archive
from zipfile import ZipFile

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.core.file_upload import process_dataset_zip_archive
from ensysmod.model import Dataset
from ensysmod.schemas import DatasetCreate, FileStatus
from ensysmod.utils.utils import create_temp_file, remove_file
from tests.utils.utils import get_current_user_from_headers, get_project_root, random_lower_string


def dataset_create_request(
    db: Session,
    current_user_header: dict[str, str],
    user_id: int | None = None,
    number_of_time_steps: int = 8760,
) -> DatasetCreate:
    """
    Generate a dataset create request with the specified user_id and number_of_time_steps.
    If user_id is not specified, the current user is used.
    """
    if user_id is None:
        user_id = get_current_user_from_headers(db, current_user_header).id
    return DatasetCreate(
        name=f"Dataset-{random_lower_string()}",
        description="Dataset description",
        hours_per_time_step=1,
        number_of_time_steps=number_of_time_steps,
        cost_unit="1e9 Euro",
        length_unit="km",
        ref_created_by=user_id,
    )


def dataset_create(
    db: Session,
    current_user_header: dict[str, str],
    user_id: int | None = None,
    number_of_time_steps: int = 8760,
) -> Dataset:
    """
    Create a dataset with the specified user_id and number_of_time_steps.
    If user_id is not specified, the current user is used.
    """
    create_request = dataset_create_request(
        db=db,
        current_user_header=current_user_header,
        user_id=user_id,
        number_of_time_steps=number_of_time_steps,
    )
    return crud.dataset.create(db=db, obj_in=create_request)


@contextmanager
def get_dataset_zip(folder_name: str) -> Generator[Path, None, None]:
    """
    Create a zip archive from folder structure /examples/datasets/
    """
    root_dir = Path(get_project_root() / "examples" / "datasets" / folder_name)

    temp_file_path = create_temp_file(prefix="ensysmod_dataset_", suffix=".zip")
    base_name = str(temp_file_path.with_suffix(""))
    zip_file_path = Path(make_archive(base_name=base_name, format="zip", root_dir=root_dir))
    try:
        yield zip_file_path
    finally:
        remove_file(zip_file_path)


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
    with get_dataset_zip(data_folder) as zip_file_path, ZipFile(zip_file_path, "r") as zip_archive:
        result = process_dataset_zip_archive(zip_archive, dataset.id, db)
        assert result.status == FileStatus.OK

    return dataset
