from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr


class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # SQLAlchemy compatibility