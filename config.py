import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration."""

    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

    PAPER_MODE = os.getenv("PAPER_MODE", "True") == "True"


settings = Settings()
