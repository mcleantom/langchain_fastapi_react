from fastapi_auth0 import Auth0
from app.core.config import settings


auth = Auth0(
    domain=settings.auth.domain,
    api_audience=settings.auth.api_audience,
    scopes={}
)