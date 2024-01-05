import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import create_example_dataset


@pytest.mark.slow()
@pytest.mark.parametrize("data_folder", ["1node_Example", "Multi-regional_Example"])
def test_download_dataset_zip(db: Session, client: TestClient, normal_user_headers: dict[str, str], data_folder: str):
    """
    Test downloading a dataset.
    """
    dataset = create_example_dataset(db, data_folder)

    response = client.get(f"/datasets/{dataset.id}/download", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/zip"
