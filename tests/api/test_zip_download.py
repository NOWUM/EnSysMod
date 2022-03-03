from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.api.test_zip_upload import get_dataset_zip
from tests.utils import data_generator


@pytest.mark.parametrize("data_folder", ["dataset-1", "dataset-2"])
def test_download_dataset(client: TestClient, db: Session, normal_user_headers: Dict[str, str], data_folder: str):
    """
    Test creating a dataset.
    """
    # Create a dataset
    dataset = data_generator.random_existing_dataset(db)

    # Upload a zip file
    zip_file_path = get_dataset_zip(data_folder)

    response = client.post(
        f"/datasets/{dataset.id}/upload",
        headers=normal_user_headers,
        files={"file": ("dataset.zip", open(zip_file_path, "rb"), "application/zip")},
    )
    assert response.status_code == 200

    response = client.get(f"/datasets/{dataset.id}/download", headers=normal_user_headers)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"
