import string

import numpy as np
from sqlalchemy import delete
from sqlalchemy.orm import Session

from ensysmod.api.deps import get_current_user
from ensysmod.database.base_class import Base
from ensysmod.model import User


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
