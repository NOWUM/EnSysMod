from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.core import security
from ensysmod.crud.base import CRUDBase
from ensysmod.model import User
from ensysmod.schemas import UserCreate, UserUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            hashed_password=security.get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, username: str, password: str):
        user_obj = self.get_by_username(db, username=username)
        if not user_obj:
            return None
        if not security.verify_password(plain_password=password, hashed_password=user_obj.hashed_password):
            return None
        return user_obj


user = CRUDUser(User)
