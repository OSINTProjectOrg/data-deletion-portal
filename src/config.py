# mft_Config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class mft_Config:
    # Basic Flask settings
    SECRET_KEY = os.getenv("OSINTPROJECT_KEY")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    #FIXME: SQLAlchemy – SQLite for quick dev, switch to Postgres/MySQL in prod
    # SQLALCHEMY_DATABASE_URI = os.getenv("OSINTPROJECT_DATABASE")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask‑WTF (CSRF)
    WTF_CSRF_ENABLED = True

    # Email / token salt
    SECURITY_SALT = os.getenv("OSINTPROJECT_SECURITYSALT")
