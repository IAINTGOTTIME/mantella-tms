from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    PUBLIC: str
    PRIVATE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def sync_database_url(self):
        return (f"postgresql+psycopg2://"
                f"{self.DB_USER}:{self.DB_PASS}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    @property
    def async_database_url(self):
        return (f"postgresql+asyncpg://"
                f"{self.DB_USER}:{self.DB_PASS}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    @property
    def private_jwt(self):
        return self.PRIVATE

    @property
    def public_jwt(self):
        return self.PUBLIC

    model_config = SettingsConfigDict(env_file=".env")
