from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils import data_generator


@pytest.mark.slow
@pytest.mark.parametrize("data_folder", ["1node_Example", "Multi-regional_Example"])
def test_optimize_model(client: TestClient, normal_user_headers: Dict[str, str], db: Session, data_folder: str):
    """
    Test optimizing an energy model.
    """
    example_model = data_generator.create_example_model(db, data_folder)
    response = client.get(f"/models/{example_model.id}/optimize/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument. spreadsheetml.sheet"

# TODO Add test for myopic_optimize_model
