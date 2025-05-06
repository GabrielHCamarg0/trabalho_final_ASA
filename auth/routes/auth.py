from fastapi import APIRouter, Depends, HTTPException, Header,Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from schemas.user import UserCreate, UserResponse
from schemas.session import SessionValidationResponse, TokenResponse, LoginRequest
from models.user import User
from models.session import Session
from dependencies.database import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"  
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 30


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register", response_model= UserResponse)
def register(user:UserCreate, db: Session = Depends(get_db)):
    db_user = db.query( User).filter(User.email == user.email).first()
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
def login(request_login:LoginRequest, db: Session = Depends(get_db),request: Request = None):
    user = db.query(User).filter(User.email == request_login.email).first()
    if not user or not verify_password(request_login.password, user.password_hash):
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
def logout(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    session = db.query(Session).filter(Session.token == token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Logout successful"}

@router.get("/validate_session", response_model=SessionValidationResponse)
def validate_session(authorization: Optional[str] = Header(None), db: Session = Depends(get_db),request: Request = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    session = db.query(Session).filter(Session.token == token).first()
    
    if not session:
        return {"valid": False, "message": "Session not found"}
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (session.expires_at > datetime.utcnow() and 
            session.ip_address == get_client_ip(request)):
            return {"valid": True}
        return {"valid": False, "message": "Session expired or invalid IP"}
    except JWTError:
        return {"valid": False, "message": "Invalid token"}