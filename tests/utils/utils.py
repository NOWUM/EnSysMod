import string
from enum import Enum
from typing import Any

import numpy as np
from sqlalchemy import delete
from sqlalchemy.orm import Session

from ensysmod.api.deps import get_current_user
from ensysmod.database.base_class import Base
from ensysmod.model import User
from ensysmod.schemas.base_schema import CreateSchema, UpdateSchema


def random_string(length: int = 10) -> str:
    return "".join(np.random.default_rng().choice(list(string.ascii_letters + string.digits), size=length))


def random_float_number(size: int | tuple[int, int] | None = None):
    result = np.random.default_rng().uniform(size=size)
    return result.tolist() if isinstance(size, int) else result


def get_current_user_from_header(db: Session, header: dict[str, str]) -> User:
    auth_token = header["Authorization"].split()[1]
    return get_current_user(db=db, token=auth_token)


def clear_database(db: Session) -> None:
    """
    Clear entries in the database but keep the database structure intact.
    """
    for table in Base.metadata.sorted_tables:
        if table.name != "user":
            db.execute(delete(table))


def clear_users_except_current_user(db: Session, user_header: dict[str, str]) -> None:
    """
    Delete all users except the current user.
    """
    current_user = get_current_user_from_header(db, user_header)
    db.execute(delete(User).where(User.id != current_user.id))


def assert_response(response_json: dict[str, Any], expected: Base | CreateSchema | UpdateSchema) -> None:
    """
    Assert that the response JSON attributes from the API matches the attributes of the given database object or create/update schema.
    If the response is a dictionary or a list, it is recursively checked for the same attributes.
    """
    response_json_attributes = set(response_json.keys())
    expected_attributes = set(expected.__table__.columns.keys()) if isinstance(expected, Base) else set(expected.model_fields.keys())

    for attribute in set.intersection(response_json_attributes, expected_attributes):
        response_json_value = response_json[attribute]
        expected_value = getattr(expected, attribute)

        if isinstance(response_json_value, dict):
            # if the response json value is a dict, recursively check it against the expected value
            assert_response(response_json_value, expected_value)
        elif isinstance(response_json_value, list):
            # if the response json value is a list, check that it has the same length as the expected value
            assert len(response_json_value) == len(expected_value)
        elif isinstance(expected_value, Enum):
            # if the expected value is an enum, check that the response json value is the same as the enum value
            assert response_json_value == expected_value.value
        else:
            assert response_json_value == expected_value
