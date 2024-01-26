from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.api import deps
from ensysmod.model import User
from ensysmod.schemas import Token, UserCreate, UserSchema

router = APIRouter()


@router.post("/login", response_model=Token)
def login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    return crud.user.authenticate(db, username=form_data.username, password=form_data.password)


@router.post("/register", response_model=UserSchema, responses={409: {"description": "User with same name already exists."}})
def register(request: UserCreate, db: Session = Depends(deps.get_db)):
    """
    Create a new user
    """
    user = crud.user.get_by_username(db, username=request.username)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with that username already exists!")
    return crud.user.create(db, obj_in=request)


@router.get("/test-token", response_model=UserSchema)
def test_token(current_user: User = Depends(deps.get_current_user)):
    """
    Test access token
    """
    return current_user
