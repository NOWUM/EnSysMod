from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_conversions import conversion_create_request, new_conversion
from tests.utils.utils import assert_response


def test_get_energy_conversion_by_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test getting all energy conversions of a dataset.
    """
    dataset = new_dataset(db, user_header)
    conversion1 = new_conversion(db, user_header, dataset_id=dataset.id)
    conversion2 = new_conversion(db, user_header, dataset_id=dataset.id)

    response = client.get("/conversions/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert_response(response.json()[0], conversion1)
    assert_response(response.json()[1], conversion2)


def test_create_conversion(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy conversion.
    """
    create_request = conversion_create_request(db, user_header)
    response = client.post("/conversions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_existing_conversion(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing energy conversion.
    """
    create_request = conversion_create_request(db, user_header)
    response = client.post("/conversions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/conversions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_conversion_unknown_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy conversion.
    """
    create_request = conversion_create_request(db, user_header)
    create_request.ref_dataset = 132456  # ungültige Anfrage
    response = client.post("/conversions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_conversion_unknown_commodity(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an energy conversion.
    """
    create_request = conversion_create_request(db, user_header)
    create_request.physical_unit = "0"  # ungültige Anfrage
    response = client.post("/conversions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_404_NOT_FOUND


# TODO Add more test cases
