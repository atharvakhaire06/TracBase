import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def required(name: str) -> str:
    """Read required env var and fail fast when missing."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing value for: {name}")
    return value


def to_int(name: str, default: int) -> int:
    """Read optional integer env var with fallback."""
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def to_bool(name: str, default: bool) -> bool:
    """Read optional boolean env var with common truthy values."""
    value_str = os.getenv(name)
    if value_str is None:
        return default
    return value_str.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "smart_expenses")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = to_int("POSTGRES_PORT", 5432)

    # JWT settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-jwt-key-for-local-dev-12345")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = to_int("ACCESS_TOKEN_EXPIRE_MINUTES", 15)

    # Password settings
    PASSWORD_HASH_SCHEME: str = os.getenv("PASSWORD_HASH_SCHEME", "bcrypt")

    # CORS policy settings
    CORS_ALLOW_CREDENTIALS: bool = to_bool("CORS_ALLOW_CREDENTIALS", False)

    @property
    def db_url(self) -> str:
        """Build SQLAlchemy async DSN."""
        custom_url = os.getenv("DATABASE_URL")
        if custom_url:
            return custom_url

        use_sqlite = to_bool("USE_SQLITE", True)
        if use_sqlite:
            db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "smart_expenses.db")).replace("\\", "/")
            return f"sqlite+aiosqlite:///{db_file}"

        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
