import os
import tempfile
import zipfile
import pytest
from typing import Dict
from zipfile import ZipFile

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import data_generator


def get_dataset_zip(folder_name: str) -> str:
    """
    Creates a zip archive from folder structure ../../examples/dataset-1/
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # create a zip file from the directory
    zip_file_path = os.path.join(temp_dir, f"{folder_name}.zip")
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        print(f"Project root: {project_root}")
        for root, dirs, files in os.walk(f"{project_root}/examples/data/{folder_name}/"):
            acr_path = os.path.relpath(root, f"{project_root}/examples/data/{folder_name}/")
            zip_file.write(root, acr_path)
            for file in files:
                zip_file.write(os.path.join(root, file), arcname=os.path.join(acr_path, file))
    return zip_file_path


@pytest.mark.parametrize("data_folder", ["dataset-1", "dataset-2"])
def test_upload_dataset(client: TestClient, db: Session, normal_user_headers: Dict[str, str], data_folder: str):
    """
    Test creating a dataset.
    """
    # Create a dataset
    dataset = data_generator.random_existing_dataset(db)

    # Upload a zip file
    zip_file_path = get_dataset_zip(data_folder)

    # print all the contents of the zip file
    print(f"Zip file contents of {zip_file_path}:")
    with ZipFile(zip_file_path, 'r') as zip_file:
        for file in zip_file.namelist():
            print(file)

    response = client.post(
        f"/datasets/{dataset.id}/upload",
        headers=normal_user_headers,
        files={"file": ("dataset.zip", open(zip_file_path, "rb"), "application/zip")},
    )
    print(response.text)
    assert response.status_code == 200

    # TODO Check that the dataset has been updated
