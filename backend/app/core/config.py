from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthZeroSettings(BaseSettings):
    domain: str
    api_audience: str
    issuer: str
    algorithms: str

    model_config = SettingsConfigDict(env_prefix="AUTH0_", case_sensitive=False)


class Settings(BaseSettings):
    postgres_database_uri: PostgresDsn = Field(..., env="SQL_ALCHEMY_DATABASE_URI")
    auth: AuthZeroSettings = AuthZeroSettings()

    model_config = SettingsConfigDict(case_sensitive=False)


settings = Settings()
