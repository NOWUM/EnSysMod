from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod.schemas import DatasetPermissionUpdate
from tests.utils.data_generator.datasets import dataset_permission_create_request, new_dataset, new_dataset_permission
from tests.utils.data_generator.users import new_user
from tests.utils.utils import assert_response, clear_database, get_current_user_from_header


def test_get_all_datasets_permissions_for_current_user(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving all datasets permissions for the current user.
    """
    clear_database(db)
    current_user = get_current_user_from_header(db, user_header)
    dataset1 = new_dataset(db, user_header, user_id=current_user.id)
    dataset2 = new_dataset(db, user_header, user_id=current_user.id)

    response = client.get("/datasets/permissions/", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert_response(response.json()[0], dataset1.permissions[0])
    assert_response(response.json()[1], dataset2.permissions[0])


def test_get_all_datasets_permissions_for_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving all datasets permissions for a specific dataset.
    """
    current_user = get_current_user_from_header(db, user_header)
    dataset = new_dataset(db, user_header, user_id=current_user.id)

    response = client.get("/datasets/permissions/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert_response(response.json()[0], dataset.permissions[0])


def test_get_dataset_permission(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a dataset permission.
    """
    current_user = get_current_user_from_header(db, user_header)
    dataset = new_dataset(db, user_header, user_id=current_user.id)

    response = client.get(f"/datasets/permissions/{dataset.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), dataset.permissions[0])


def test_get_dataset_permission_not_found(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a dataset permission, with invalid dataset_id.
    """
    other_user = new_user(db)
    dataset = new_dataset(db, user_header, user_id=other_user.id)

    response = client.get(f"/datasets/permissions/{dataset.id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_dataset_permission(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating a new dataset permission for another user.
    """
    other_user = new_user(db)
    create_request = dataset_permission_create_request(db, user_header, ref_user=other_user.id)

    response = client.post("/datasets/permissions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), create_request)


def test_create_existing_dataset_permission(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test creating an existing dataset permission.
    """
    other_user = new_user(db)
    create_request = dataset_permission_create_request(db, user_header, ref_user=other_user.id)

    response = client.post("/datasets/permissions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/datasets/permissions/", headers=user_header, content=create_request.model_dump_json())
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_dataset_permission(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test updating a dataset permission.
    """
    existing_permission = new_dataset_permission(db, user_header)

    update_request = DatasetPermissionUpdate(
        ref_dataset=existing_permission.ref_dataset,
        ref_user=existing_permission.ref_user,
        allow_usage=False,
        allow_modification=False,
        allow_permission_grant=False,
        allow_permission_revoke=False,
    )

    response = client.put("/datasets/permissions/", headers=user_header, content=update_request.model_dump_json())
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), update_request)


def test_remove_dataset_permission(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting a dataset permission.
    """
    existing_permission = new_dataset_permission(db, user_header)
    response = client.delete(f"/datasets/permissions/{existing_permission.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert_response(response.json(), existing_permission)
