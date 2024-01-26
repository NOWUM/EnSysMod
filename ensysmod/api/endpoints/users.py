from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.api import deps
from ensysmod.schemas import UserSchema

router = APIRouter()


@router.get("/", response_model=list[UserSchema])
def get_all_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all users.
    """
    return crud.user.get_multi(db=db, skip=skip, limit=limit)
