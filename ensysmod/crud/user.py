from datetime import timedelta
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod.core import security, settings
from ensysmod.crud.base import CRUDBase
from ensysmod.model import User
from ensysmod.schemas import Token, UserCreate, UserUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return db.execute(query).scalar_one_or_none()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(username=obj_in.username, hashed_password=security.get_password_hash(obj_in.password))
        return super().create(db, obj_in=db_obj)

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate | dict[str, Any]) -> User:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            update_data["hashed_password"] = security.get_password_hash(update_data["password"])
            del update_data["password"]
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Token:
        user = self.get_by_username(db, username=username)
        if (user is None) or (not security.verify_password(plain_password=password, hashed_password=user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password!")

        return Token(
            access_token=security.create_access_token(
                subject=user.id,
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            ),
            token_type="bearer",
        )


user = CRUDUser(User)
