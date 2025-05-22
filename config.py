import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    ADMIN_IDS: list[int] = field(
        default_factory=lambda: [
            int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x
        ]
    )
    TELEGRAM_API_ID: int = int(os.getenv("TELEGRAM_API_ID", 0))
    TELEGRAM_API_HASH: str = os.getenv("TELEGRAM_API_HASH")
    TELEGRAM_PHONE: str = os.getenv("TELEGRAM_PHONE")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    EMAIL_FROM: str = os.getenv("EMAIL_FROM")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    
    DATA_DIR: str = "data"
    CONTACTS_FILE: str = os.path.join(DATA_DIR, "contacts.xlsx")
    BACKUP_DIR: str = os.path.join(DATA_DIR, "backups")

config = Config()
os.makedirs(config.DATA_DIR, exist_ok=True)
os.makedirs(config.BACKUP_DIR, exist_ok=True)