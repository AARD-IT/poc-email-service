import os
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, dotenv_values

# Load .env from the current directory (try .env first, then .env.local)
base_path = Path(__file__).parent
env_path = base_path / ".env"
env_local_path = base_path / ".env.local"

# Try loading from .env, fallback to .env.local
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    values = dotenv_values(dotenv_path=env_path)
elif env_local_path.exists():
    load_dotenv(dotenv_path=env_local_path, override=True)
    values = dotenv_values(dotenv_path=env_local_path)
else:
    values = {}

# Ensure values from the file are present in os.environ (robust when using reloaders)
# Also strip BOM characters from keys if present
for k, v in values.items():
    clean_key = k.lstrip('\ufeff')  # Remove BOM character if present
    if v is not None and not os.getenv(clean_key):
        os.environ[clean_key] = v


class Settings:
    def __init__(self):
        self.resend_api_key = os.getenv("RESEND_API_KEY", "").strip()
        self.from_email = os.getenv("FROM_EMAIL", "rnd@analyticsavenue.in").strip()
        self.admin_email = os.getenv("ADMIN_EMAIL", "rnd@analyticsavenue.in").strip()
        self.website_url = os.getenv("WEBSITE_URL", "https://www.analyticsavenuerd.in/").strip()
        self.log_level = os.getenv("LOG_LEVEL", "INFO").strip()
        
        if not self.resend_api_key:
            raise ValueError(
                "RESEND_API_KEY is required but not set. "
                "Add it to your .env file (copy .env.example and fill in your key)."
            )
        if not self.website_url:
            raise ValueError("WEBSITE_URL is required but not set. "
                           "Add it to your .env file.")


settings = Settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO)
)

logger = logging.getLogger("email_service")

app = FastAPI(
    title="Analytics Avenue - Email Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "Backend Connected Successfully"}


@app.get("/health")
async def health():
    return {"status": "ok"}


from routes import email_routes as routes

app.include_router(
    routes.router,
    prefix="/api/email",
    tags=["email"]
)