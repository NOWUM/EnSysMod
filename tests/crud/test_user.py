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
    username = random_lower_string()
    user_in = UserCreate(username=username, password=random_lower_string())
    user_one = crud.user.create(db, obj_in=user_in)
    assert user_one.username == username
    assert hasattr(user_one, "hashed_password")

    try:
        crud.user.create(db, obj_in=user_in)
    except IntegrityError as err:
        assert "username" in err.args[0]
        return

    raise Exception("User two should fail with IntegrityError")
