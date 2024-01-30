from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.data_generator.users import new_user
from tests.utils.utils import assert_response, clear_users_except_current_user, get_current_user_from_header


def test_get_all_users(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving all users.
    """
    clear_users_except_current_user(db, user_header)
    user1 = get_current_user_from_header(db, user_header)
    user2 = new_user(db)

    response = client.get("/users/", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert_response(response.json()[0], user1)
    assert_response(response.json()[1], user2)
