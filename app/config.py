from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    database_path: Path


def get_settings() -> Settings:
    config_dir = Path(__file__).resolve().parent
    default_database = config_dir / "database" / "wallet.sqlite3"
    return Settings(Path(os.getenv("BANK_DATABASE_PATH", default_database)))