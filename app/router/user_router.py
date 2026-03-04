from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreateDTO, UserResponseDTO

router = APIRouter()
service = UserService()


@router.get("/users")
async def get_users(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    users = await service.get_users(db)
    return [
        UserResponseDTO.model_validate(u)
        for u in users
    ]

@router.post("/users")
async def create_user(
    user: UserCreateDTO,
    db: AsyncSession = Depends(get_db),
):
    
    created_user = await service.create_user(db, user)
    return UserResponseDTO.model_validate(created_user)