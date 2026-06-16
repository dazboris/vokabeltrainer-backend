from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import traceback # Yeni eklenen satır
import logging # Yeni eklenen satır
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserRead

SECRET_KEY = "vokabeltrainer-super-secret-key"  # Gerçek projelerde bu .env dosyasında saklanır
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # Token 1 hafta geçerli olsun

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # encoding="utf-8" kaldırıldı

logger = logging.getLogger(__name__) # Yeni eklenen satır
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    user = db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == user_in.email))
    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    try:
        hashed_password = pwd_context.hash(user_in.password)
        db_user = User(email=user_in.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        logger.error(f"Error during user registration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred during user registration.")


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    if len(form_data.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    user = db.scalar(select(User).where(User.email == form_data.username))
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = jwt.encode({"sub": str(user.id), "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=access_token, token_type="bearer")