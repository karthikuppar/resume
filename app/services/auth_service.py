from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from fastapi import HTTPException, status

class AuthService:
    
    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
        # 1. Check if the user already exists in the database
        query = select(User).where(User.email == user_data.email)
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # 2. Securely hash the password so it's not saved as plain text
        hashed_password = get_password_hash(user_data.password)
        
        # 3. Create a new user database object
        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True
        )
        
        # 4. Save the user to the database session
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user

auth_service = AuthService()