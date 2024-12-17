from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class PostgresConfig(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


class MinioConfig(BaseSettings):
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str
    MINIO_USE_SSL: bool

    @property
    def minio_endpoint_url(self) -> str:
        return f"{self.MINIO_HOST}:{self.MINIO_PORT}"


postgres_config = PostgresConfig()
minio_config = MinioConfig()


class Config:
    postgres_config = postgres_config
    minio_config = minio_config


application_config = Config()
