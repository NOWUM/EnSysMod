import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import EXAMPLE_DATASETS
from tests.utils.data_generator.energy_models import get_example_model


@pytest.mark.slow()
@pytest.mark.require_solver()
@pytest.mark.parametrize("example_dataset", EXAMPLE_DATASETS)
def test_optimize_model(db: Session, client: TestClient, user_header: dict[str, str], example_dataset: str):
    """
    Test optimizing an energy model.
    """
    model = get_example_model(db, user_header, example_dataset=example_dataset)
    response = client.get(f"/models/{model.id}/optimize/", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument. spreadsheetml.sheet"


# TODO Add test for myopic_optimize_model
