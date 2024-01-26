from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import UserCreate
from tests.utils.utils import clear_users_except_current_user, get_current_user_from_header, random_string


def test_get_all_users(db: Session, client: TestClient, user_header: dict[str, str]):
    """
    Test retrieving all users.
    """
    clear_users_except_current_user(db, user_header)
    user1 = get_current_user_from_header(db, user_header)
    user2 = crud.user.create(db=db, obj_in=UserCreate(username=random_string(), password=random_string()))

    response = client.get("/users/", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    users_list = response.json()
    assert len(users_list) == 2
    assert users_list[0]["username"] == user1.username
    assert users_list[0]["id"] == user1.id
    assert users_list[1]["username"] == user2.username
    assert users_list[1]["id"] == user2.id
