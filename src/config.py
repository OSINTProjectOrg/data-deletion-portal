# mft_Config.py
import os

class mft_Config:
    # Basic Flask settings
    OSINTPROJECT_KEY = os.getenv("OSINTPROJECT_KEY")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    #FIXME: SQLAlchemy – SQLite for quick dev, switch to Postgres/MySQL in prod
    SQLALCHEMY_DATABASE_URI = os.getenv("OSINTPROJECT_DATABASE")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask‑WTF (CSRF)
    WTF_CSRF_ENABLED = True

    # Email / token salt
    OSINTPROJECT_SECURITYSALT = os.getenv("OSINTPROJECT_SECURITYSALT")
