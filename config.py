from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):    
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_USERNAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        # Construct the database URL for SQLAlchemy
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

App_Settings = AppSettings() 