from zipfile import ZipFile

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import dataset_create, get_dataset_zip


@pytest.mark.slow
@pytest.mark.parametrize("data_folder", ["1node_Example", "Multi-regional_Example"])
def test_upload_dataset_zip(db: Session, client: TestClient, normal_user_headers: dict[str, str], data_folder: str):
    """
    Test uploading a dataset.
    """
    dataset = dataset_create(db, normal_user_headers)

    with get_dataset_zip(data_folder) as zip_file_path:
        # print all the contents of the zip file
        print(f"Zip file contents of {zip_file_path}:")
        with ZipFile(zip_file_path, "r") as zip_file:
            for file in zip_file.namelist():
                print(file)

        response = client.post(
            f"/datasets/{dataset.id}/upload",
            headers=normal_user_headers,
            files={"file": ("dataset.zip", zip_file_path.open(mode="rb"), "application/zip")},
        )
        print(response.text)
        assert response.status_code == status.HTTP_200_OK

    # TODO Check that the dataset has been updated
