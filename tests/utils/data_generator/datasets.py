import os
import tempfile
from zipfile import ZipFile

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.core.file_upload import process_dataset_zip_archive
from ensysmod.model import Dataset
from ensysmod.schemas import DatasetCreate, FileStatus
from tests.utils.utils import create_random_user, random_lower_string


def random_dataset_create() -> DatasetCreate:
    """
    Generates a random dataset create request.
    """
    dataset_name = "DS " + random_lower_string()
    dataset_description = "DS desc " + random_lower_string()
    return DatasetCreate(name=dataset_name, description=dataset_description,
                         hours_per_time_step=1, number_of_time_steps=8760,
                         cost_unit='1e9 Euro', length_unit='km',
                         ref_created_by=1)


def random_existing_dataset(db: Session) -> Dataset:
    """
    Generates a random existing dataset.
    """
    user = crud.user.get(db=db, id=1)
    if user is None:
        create_random_user(db=db)
    create_request = random_dataset_create()
    return crud.dataset.create(db=db, obj_in=create_request)


def fixed_dataset_create() -> DatasetCreate:
    """
    Generates a fixed dataset create request.
    Will always return the same create request.
    """
    return DatasetCreate(name="Fixed dataset", description="Fixed dataset description", ref_created_by=1)


def fixed_existing_dataset(db: Session) -> Dataset:
    """
    Generates a fixed existing dataset.
    Will always return the same dataset.
    """
    user = crud.user.get(db=db, id=1)
    if user is None:
        create_random_user(db=db)
    create_request = fixed_dataset_create()
    dataset = crud.dataset.get_by_name(db=db, name=create_request.name)
    if dataset is None:
        dataset = crud.dataset.create(db=db, obj_in=create_request)
    return dataset


def get_dataset_zip(folder_name: str) -> str:
    """
    Create a zip archive from folder structure /examples/datasets/
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # create a zip file from the directory
    zip_file_path = os.path.join(temp_dir, f"{folder_name}.zip")
    with ZipFile(zip_file_path, 'w') as zip_file:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        print(f"Project root: {project_root}")
        for root, dirs, files in os.walk(f"{project_root}/examples/datasets/{folder_name}/"):
            acr_path = os.path.relpath(root, f"{project_root}/examples/datasets/{folder_name}/")
            zip_file.write(root, acr_path)
            for file in files:
                zip_file.write(os.path.join(root, file), arcname=os.path.join(acr_path, file))
    return zip_file_path


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
        cost_unit='1e9 Euro',
        length_unit='km',
        ref_created_by=1
    )
    dataset = crud.dataset.create(db=db, obj_in=create_request)

    # Zip and upload the example dataset from data_folder
    zip_file_path = get_dataset_zip(data_folder)

    with ZipFile(zip_file_path, 'r') as zip_archive:
        result = process_dataset_zip_archive(zip_archive, dataset.id, db)
        assert result.status == FileStatus.OK

    return dataset
