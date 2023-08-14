from typing import Dict
from zipfile import ZipFile

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import data_generator


@pytest.mark.slow
@pytest.mark.parametrize("data_folder", ["1node_Example", "Multi-regional_Example"])
def test_upload_dataset_zip(client: TestClient, db: Session, normal_user_headers: Dict[str, str], data_folder: str):
    """
    Test uploading a dataset.
    """
    # Create a dataset
    dataset = data_generator.random_existing_dataset(db)

    # Upload a zip file
    zip_file_path = data_generator.get_dataset_zip(data_folder)

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
    assert response.status_code == status.HTTP_200_OK

    # TODO Check that the dataset has been updated
