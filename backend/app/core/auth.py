from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings


class VerifyToken:

    def __init__(self):
        jwks_url = f"https://{settings.auth.domain}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(
            self,
            security_scopes: SecurityScopes,
            token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
    ):
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.auth.algorithms,
                audience=settings.auth.api_audience,
                issuer=settings.auth.issuer
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return payload


auth = VerifyToken()
