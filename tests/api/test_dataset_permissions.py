from fastapi import status
from fastapi.testclient import TestClient
from schemas.dataset_permission import DatasetPermissionUpdate
from sqlalchemy.orm import Session

from tests.utils.data_generator.datasets import dataset_permission_create_request, new_dataset, new_dataset_permission
from tests.utils.data_generator.users import new_user
from tests.utils.utils import clear_database, get_current_user_from_header


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

    permissions_list = response.json()
    assert len(permissions_list) == 2
    assert permissions_list[0]["dataset"]["id"] == dataset1.id
    assert permissions_list[0]["user"]["id"] == current_user.id
    assert permissions_list[1]["dataset"]["id"] == dataset2.id
    assert permissions_list[1]["user"]["id"] == current_user.id


def test_get_all_datasets_permissions_for_dataset(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving all datasets permissions for a specific dataset.
    """
    current_user = get_current_user_from_header(db, user_header)
    dataset = new_dataset(db, user_header, user_id=current_user.id)

    response = client.get("/datasets/permissions/", headers=user_header, params={"dataset_id": dataset.id})
    assert response.status_code == status.HTTP_200_OK

    permissions_list = response.json()
    assert len(permissions_list) == 1
    assert permissions_list[0]["dataset"]["id"] == dataset.id
    assert permissions_list[0]["user"]["id"] == current_user.id


def test_get_dataset_permission(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving a dataset permission.
    """
    current_user = get_current_user_from_header(db, user_header)
    dataset = new_dataset(db, user_header, user_id=current_user.id)

    response = client.get(f"/datasets/permissions/{dataset.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    retrieved_permission = response.json()
    assert retrieved_permission["dataset"]["id"] == dataset.id
    assert retrieved_permission["user"]["id"] == current_user.id


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

    created_permission = response.json()
    assert created_permission["dataset"]["id"] == create_request.ref_dataset
    assert created_permission["user"]["id"] == create_request.ref_user


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

    updated_permission = response.json()
    assert updated_permission["dataset"]["id"] == update_request.ref_dataset
    assert updated_permission["user"]["id"] == update_request.ref_user
    assert updated_permission["allow_usage"] == update_request.allow_usage


def test_remove_dataset_permission(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test deleting a dataset permission.
    """
    existing_permission = new_dataset_permission(db, user_header)
    response = client.delete(f"/datasets/permissions/{existing_permission.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    deleted_permission = response.json()
    assert deleted_permission["dataset"]["id"] == existing_permission.ref_dataset
    assert deleted_permission["user"]["id"] == existing_permission.ref_user
