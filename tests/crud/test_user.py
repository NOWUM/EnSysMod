import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import UserCreate
from tests.utils.utils import random_lower_string


def test_create_user(db: Session) -> None:
    username = random_lower_string()
    user_in = UserCreate(username=username, password=random_lower_string())
    user = crud.user.create(db, obj_in=user_in)
    assert user.username == username
    assert hasattr(user, "hashed_password")


def test_create_user_twice(db: Session) -> None:
    user_in = UserCreate(username=random_lower_string(), password=random_lower_string())
    crud.user.create(db, obj_in=user_in)

    with pytest.raises(IntegrityError) as err:
        crud.user.create(db, obj_in=user_in)

    assert "username" in err.value.args[0]
