from pathlib import Path
from dotenv import find_dotenv, dotenv_values, load_dotenv
import os

# Discover .env
env_path = Path(__file__).parent.parent / ".env"
if not env_path.exists():
    found = find_dotenv(usecwd=True)
    if found:
        env_path = Path(found)

if env_path and env_path.exists():
    load_dotenv(dotenv_path=env_path)
    # populate os.environ with dotenv_values for robustness
    values = dotenv_values(dotenv_path=env_path)
    for k, v in values.items():
        if v is not None and os.getenv(k) in (None, ""):
            os.environ[k] = v

KEYS = ["RESEND_API_KEY", "FROM_EMAIL", "ADMIN_EMAIL", "WEBSITE_URL", "LOG_LEVEL"]

SENSITIVE_PATTERNS = ("KEY", "SECRET", "PASSWORD", "TOKEN")


def mask_value(k: str, v: str) -> str:
    up = k.upper()
    if any(p in up for p in SENSITIVE_PATTERNS):
        return "***hidden***"
    return v


if __name__ == "__main__":
    print(f"Using .env: {env_path if env_path.exists() else 'none found'}")
    for k in KEYS:
        v = os.getenv(k)
        if v is None:
            print(f"{k}: <not set>")
        else:
            print(f"{k}: {mask_value(k, v)}")
