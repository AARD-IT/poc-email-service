import os
import logging
from fastapi import APIRouter, HTTPException
from fastapi import status
from typing import Any

from services.resend_service import init_resend_service_from_env
from utils.template_loader import render_template
from models.email_models import (
    WelcomeEmail,
    AdminAlertEmail,
    AdminAlertEmailAuto,
    ApprovalEmail,
    RejectionEmail,
    AccessEmail,
    FullAccessEmail,
)

logger = logging.getLogger("email_service.routes")

router = APIRouter()

resend = init_resend_service_from_env()


@router.get("/debug-env")
async def debug_env(show_values: bool = False):
    """Return selected environment variables for debugging.

    By default, sensitive values (keys containing KEY/SECRET/PASSWORD/TOKEN) are masked.
    Set `show_values=true` to include non-sensitive values.
    """
    keys = [
        "RESEND_API_KEY",
        "FROM_EMAIL",
        "ADMIN_EMAIL",
        "WEBSITE_URL",
        "LOG_LEVEL",
    ]
    out = {}
    for k in keys:
        v = os.getenv(k)
        if v is None:
            out[k] = None
            continue
        up = k.upper()
        sensitive = any(s in up for s in ("KEY", "SECRET", "PASSWORD", "TOKEN"))
        if sensitive:
            out[k] = "***hidden***"
        else:
            out[k] = v if show_values else (v if k in ("FROM_EMAIL", "ADMIN_EMAIL", "WEBSITE_URL") else "***hidden***")

    # also include a presence map for all env names
    presence = {k: (os.getenv(k) is not None) for k in keys}
    return {"env": out, "present": presence}


@router.post("/send-welcome")
async def send_welcome(payload: WelcomeEmail):
    try:
        variables = {"name": payload.name or "User", "website_url": os.getenv("WEBSITE_URL")}
        if payload.variables:
            variables.update(payload.variables)
        html = render_template("welcome.html", variables)
        result = await resend.send_email(subject="Welcome to Analytics Avenue", recipient=str(payload.recipient), html=html, variables=variables)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        return {"ok": True}
    except Exception as e:
        logger.exception("Error in send_welcome")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-admin-alert")
async def send_admin_alert(payload: AdminAlertEmail):
    try:
        variables = {"user_email": payload.user_email, "user_name": payload.user_name or "User", "details": payload.details or {}}
        html = render_template("admin_alert.html", variables)
        result = await resend.send_email(subject="New Signup Alert", recipient=str(payload.admin_email), html=html)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        return {"ok": True}
    except Exception as e:
        logger.exception("Error in send_admin_alert")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-admin-alert-auto")
async def send_admin_alert_auto(payload: AdminAlertEmailAuto):
    """Send admin alert using ADMIN_EMAIL from environment. Perfect for new signup workflows."""
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        if not admin_email:
            raise HTTPException(status_code=500, detail="ADMIN_EMAIL not configured in environment")
        
        variables = {
            "user_email": payload.user_email, 
            "user_name": payload.user_name or "User", 
            "details": payload.details or {},
            "website_url": os.getenv("WEBSITE_URL")
        }
        html = render_template("admin_alert.html", variables)
        result = await resend.send_email(subject="New Signup Alert", recipient=admin_email, html=html)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        return {"ok": True, "sent_to": admin_email}
    except Exception as e:
        logger.exception("Error in send_admin_alert_auto")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-approval")
async def send_approval(payload: ApprovalEmail):
    try:
        variables = {"name": payload.name or "User", "approved_by": payload.approved_by or "Admin", "website_url": os.getenv("WEBSITE_URL")}
        if payload.variables:
            variables.update(payload.variables)
        html = render_template("approval.html", variables)
        result = await resend.send_email(subject="Your account has been approved", recipient=str(payload.recipient), html=html)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        return {"ok": True}
    except Exception as e:
        logger.exception("Error in send_approval")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-rejection")
async def send_rejection(payload: RejectionEmail):
    try:
        variables = {"name": payload.name or "User", "reason": payload.reason or "Not specified", "website_url": os.getenv("WEBSITE_URL")}
        if payload.variables:
            variables.update(payload.variables)
        html = render_template("rejection.html", variables)
        result = await resend.send_email(subject="Your account request was rejected", recipient=str(payload.recipient), html=html)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        return {"ok": True}
    except Exception as e:
        logger.exception("Error in send_rejection")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-access")
async def send_access(payload: AccessEmail):
    try:
        variables = {"name": payload.name or "User", "assigned_pocs": payload.assigned_pocs, "website_url": os.getenv("WEBSITE_URL")}
        if payload.variables:
            variables.update(payload.variables)
        html = render_template("access.html", variables)
        result = await resend.send_email(subject="You have been granted POC access", recipient=str(payload.recipient), html=html)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        return {"ok": True}
    except Exception as e:
        logger.exception("Error in send_access")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-full-access")
async def send_full_access(payload: FullAccessEmail):
    try:
        variables = {"name": payload.name or "User", "areas": payload.areas, "website_url": os.getenv("WEBSITE_URL")}
        if payload.variables:
            variables.update(payload.variables)
        html = render_template("full_access.html", variables)
        result = await resend.send_email(subject="Full platform access granted", recipient=str(payload.recipient), html=html)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        return {"ok": True}
    except Exception as e:
        logger.exception("Error in send_full_access")
        raise HTTPException(status_code=500, detail=str(e))
