from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateDTO
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
class UserService:

    def __init__(self):
        self.repository = UserRepository()

    async def get_users(self, db):
        return await self.repository.get_all(db)

    # transactional
    async def create_user(self, db, user_dto):
        try:
            existing = await self.repository.get_by_email(db, user_dto.email)
            if existing:
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists"
                )
            user = await self.repository.create(
                db,
                name=user_dto.name,
                email=user_dto.email,
            )
            await db.commit()
            await db.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )
    



