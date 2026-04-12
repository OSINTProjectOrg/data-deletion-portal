# auth/utils.py
import secrets
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def mft_GenerateToken(email: str, expires_sec: int = 3600) -> str:
    """Create a signed token (e.g., for email-verification or password reset)."""
    s = URLSafeTimedSerializer(current_app.mft_Config["OSINTPROJECT_KEY"])
    return s.dumps(email, salt=current_app.mft_Config.get("OSINTPROJECT_SECURITYSALT"))


def mft_VerifyGenerateToken(token: str, max_age: int = 3600) -> str | None:
    """Validate a token - returns the e-mail if OK, else None."""
    s = URLSafeTimedSerializer(current_app.mft_Config["OSINTPROJECT_KEY"])
    try:
        email = s.loads(token, salt=current_app.mft_Config.get("OSINTPROJECT_SECURITYSALT"), max_age=max_age)
        return email
    except Exception:
        return None
