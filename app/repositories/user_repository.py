from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.users import User


class UserRepository:

    async def get_by_email(self, db, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

    async def create(self, db: AsyncSession, name: str, email: str):
        user = User(name=name, email=email)
        db.add(user)
        await db.flush() 
        return user