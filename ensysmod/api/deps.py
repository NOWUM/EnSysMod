from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ensysmod import crud, model, schemas
from ensysmod.core import security, settings
from ensysmod.database.session import SessionLocal


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_current_user(
    db: Session = Depends(get_db),  # noqa: B008
    token: str = Depends(oauth2_scheme),
) -> model.User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials") from exc
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return user
