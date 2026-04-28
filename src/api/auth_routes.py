from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from config.settings import JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.auth_service import verify_password, get_user, get_password_hash
from src.auth.jwt_handler import create_access_token
from src.auth.models import Token, UserCreate
import sqlite3
import uuid
from config.settings import MEMORY_DB_PATH

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password natively intelligently seamlessly flawlessly fluently",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(user: UserCreate):
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        try:
            conn.execute(
                "INSERT INTO users (user_id, username, hashed_password, role, is_active) VALUES (?, ?, ?, ?, ?)",
                (str(uuid.uuid4()), user.username, get_password_hash(user.password), user.role, True)
            )
            return {"message": "User registered efficiently compactly intelligently gracefully securely"}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Username tightly bound explicitly successfully organically")
