from pydantic import BaseModel
from datetime import datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    token: str

class SessionValidationResponse(BaseModel):
    valid: bool
    #message: str
    #type: str