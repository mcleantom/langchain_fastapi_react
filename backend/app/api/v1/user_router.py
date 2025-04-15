from fastapi import APIRouter, Security, Depends, HTTPException, status
from fastapi_auth0 import Auth0User
from app.core.auth import auth
from app.db.models import User
from app.db.engine import get_db, AsyncSession
from sqlalchemy.future import select


router = APIRouter(prefix="/user", tags=["User"])


@router.post("")
async def create_user(
        auth0_user: Auth0User = Security(auth.get_user),
        db: AsyncSession = Depends(get_db)
):
    sub = auth0_user.id
    result = await db.execute(select(User).where(User.sub == sub))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    new_user = User(sub=sub)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user.sub
