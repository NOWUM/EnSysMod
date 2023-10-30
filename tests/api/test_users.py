from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.utils import (
    clear_users_except_current_user,
    create_random_user,
    get_current_user_from_headers,
)


def test_get_all_users(db: Session, client: TestClient, normal_user_headers: dict[str, str]):
    """
    Test retrieving all users.
    """
    clear_users_except_current_user(db, normal_user_headers)
    user1 = get_current_user_from_headers(db, normal_user_headers)
    user2 = create_random_user(db)

    response = client.get("/users/", headers=normal_user_headers)
    assert response.status_code == status.HTTP_200_OK

    users_list = response.json()
    assert len(users_list) == 2
    assert users_list[0]["username"] == user1.username
    assert users_list[0]["id"] == user1.id
    assert users_list[1]["username"] == user2.username
    assert users_list[1]["id"] == user2.id
