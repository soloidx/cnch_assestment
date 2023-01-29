from enum import Enum

from pydantic import BaseSettings


class TestTargetEnum(str, Enum):
    local = "local"
    remote = "remote"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Take home project"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///app.db"
    TEST_TARGET: TestTargetEnum = TestTargetEnum.local
    REMOTE_ENDPOINT: str = "https://concha-labs-375805.uc.r.appspot.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
