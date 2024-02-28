import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import EXAMPLE_DATASETS, get_example_dataset


@pytest.mark.slow()
@pytest.mark.parametrize("example_dataset", EXAMPLE_DATASETS)
def test_download_dataset_zip(db: Session, client: TestClient, user_header: dict[str, str], example_dataset: str):
    """
    Test downloading a dataset.
    """
    dataset = get_example_dataset(db, user_header, example_dataset=example_dataset)

    response = client.get(f"/datasets/{dataset.id}/download", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["Content-Type"] == "application/zip"
