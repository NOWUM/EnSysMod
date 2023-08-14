from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import data_generator


@pytest.mark.slow
@pytest.mark.parametrize("data_folder", ["1node_Example", "Multi-regional_Example"])
def test_download_dataset_zip(client: TestClient, db: Session, normal_user_headers: Dict[str, str], data_folder: str):
    """
    Test downloading a dataset.
    """
    dataset = data_generator.create_example_dataset(db, data_folder)

    response = client.get(f"/datasets/{dataset.id}/download", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/zip"
