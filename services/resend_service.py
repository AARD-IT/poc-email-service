import os
import logging
import asyncio
from typing import Dict, Any

import resend

logger = logging.getLogger("email_service.resend")


class ResendService:
    def __init__(self, api_key: str, default_from: str):
        self.api_key = api_key
        self.default_from = default_from
        # initialize client to None by default
        self.client = None
        if not api_key:
            logger.warning("RESEND_API_KEY not provided — email sending is disabled")
            return
        try:
            # Try common client class names used by different resend package versions
            client_cls = None
            for name in ("Resend", "ResendClient", "Client"):
                client_cls = getattr(resend, name, None)
                if client_cls:
                    break

            if client_cls and callable(client_cls):
                try:
                    # prefer keyword argument if supported
                    self.client = client_cls(api_key=api_key)
                except TypeError:
                    self.client = client_cls(api_key)
            else:
                if hasattr(resend, "api_key"):
                    resend.api_key = api_key
                if hasattr(resend, "Emails") and callable(getattr(resend, "Emails")):
                    self.client = resend.Emails()
                elif hasattr(resend, "emails") and hasattr(resend.emails, "Emails") and callable(getattr(resend.emails, "Emails")):
                    self.client = resend.emails.Emails()
                else:
                    raise AttributeError("No compatible client class found in resend package")
        except Exception:
            logger.exception("Failed to initialize Resend client")
            self.client = None

    async def send_email(self, subject: str, recipient: str, html: str, variables: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Send an email using Resend. Runs sync client in thread executor."""
        def _sync_send():
            if not self.client:
                err = "Resend client not configured (missing API key)"
                logger.error(err)
                return {"ok": False, "error": err}
            try:
                if hasattr(self.client, "emails") and hasattr(self.client.emails, "send"):
                    resp = self.client.emails.send(
                        from_=self.default_from,
                        to=[recipient],
                        subject=subject,
                        html=html,
                    )
                elif hasattr(self.client, "send"):
                    resp = self.client.send(
                        params={
                            "from": self.default_from,
                            "to": [recipient],
                            "subject": subject,
                            "html": html,
                        }
                    )
                else:
                    raise AttributeError("Resend client does not expose a send method")
                return {"ok": True, "response": resp}
            except Exception as e:
                logger.exception("Failed to send email")
                return {"ok": False, "error": str(e)}

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _sync_send)
        return result


def init_resend_service_from_env() -> ResendService:
    api_key = os.getenv("RESEND_API_KEY")
    default_from = os.getenv("FROM_EMAIL")
    if not default_from:
        default_from = "rnd@analyticsavenue.in"
    return ResendService(api_key=api_key, default_from=default_from)
