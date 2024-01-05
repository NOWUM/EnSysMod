from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ensysmod import crud, model, schemas
from ensysmod.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.User])
def get_all_users(
    db: Session = Depends(deps.get_db),
    current: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.User]:
    """
    Retrieve all users.
    """
    return crud.user.get_multi(db=db, skip=skip, limit=limit)
