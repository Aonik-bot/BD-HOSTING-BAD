import os

class Config:
    APP_NAME = "Aonik-Bot-Service"
    VERSION = "2.4.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    MAX_WORKERS = 4
