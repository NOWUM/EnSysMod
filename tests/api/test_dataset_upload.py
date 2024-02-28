import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import EXAMPLE_DATASETS, get_dataset_zip, new_dataset


@pytest.mark.slow()
@pytest.mark.parametrize("example_dataset", EXAMPLE_DATASETS)
def test_upload_dataset_zip(db: Session, client: TestClient, user_header: dict[str, str], example_dataset: str):
    """
    Test uploading a dataset.
    """
    dataset = new_dataset(db, user_header)

    response = client.post(
        f"/datasets/{dataset.id}/upload",
        headers=user_header,
        files={"file": (f"{example_dataset}.zip", get_dataset_zip(example_dataset).open(mode="rb"), "application/zip")},
    )
    assert response.status_code == status.HTTP_200_OK

    # TODO Check that the dataset has been updated
