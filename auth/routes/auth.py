from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from schemas.session import  SessionValidationResponse, LoginRequest, TokenResponse
from schemas.user import UserCreate, UserResponse
from models.user import User
from models.session import Session

from dependencies.database import get_db
from dependencies.auth import get_current_user, require_role
security = HTTPBearer()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secure-secret-key"  # Deve ser igual ao auth.py
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        user_type=user.user_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db), request: Request = None):
    user = db.query(User).filter(User.email == login_request.email).first()
    if not user or not verify_password(login_request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    session = Session(
        user_id=user.id,
        token=token,
        ip_address=get_client_ip(request),
        expires_at=datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    )
    db.add(session)
    db.commit()
    return {"token": token}

@router.post("/logout")
def logout(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(Session).filter(Session.user_id == user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Logout successful"}

@router.get("/validate_session", response_model=SessionValidationResponse)
def validate_session(user: User = Depends(get_current_user)):
    return {"valid": True}

@router.get("/me", response_model=UserResponse)
def get_user(user: User = Depends(get_current_user)):
    return user

@router.get("/admin-only", response_model=UserResponse)
def admin_only(user: User = Depends(require_role("admin"))):
    return user