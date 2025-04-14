from fastapi import APIRouter, Security
from fastapi_auth0 import Auth0User
from app.core.auth import auth


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/secure-data")
def secure_data(user: Auth0User = Security(auth.get_user)):
    return {"user": user}
