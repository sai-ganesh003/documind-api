from pydantic import BaseModel, ConfigDict

from pydantic import BaseModel, ConfigDict, field_validator

class RegisterRequest(BaseModel):
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def password_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("password must not be empty")
        return v

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str