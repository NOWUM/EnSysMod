import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.energy_models import create_example_model


@pytest.mark.slow()
@pytest.mark.require_solver()
@pytest.mark.parametrize("data_folder", ["1node_Example", "Multi-regional_Example"])
def test_optimize_model(db: Session, client: TestClient, normal_user_headers: dict[str, str], data_folder: str):
    """
    Test optimizing an energy model.
    """
    example_model = create_example_model(db, data_folder)
    response = client.get(f"/models/{example_model.id}/optimize/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument. spreadsheetml.sheet"


# TODO Add test for myopic_optimize_model
