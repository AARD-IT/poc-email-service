from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any


class EmailBase(BaseModel):
    recipient: EmailStr
    name: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None


class WelcomeEmail(EmailBase):
    signup_source: Optional[str] = None


class AdminAlertEmail(BaseModel):
    admin_email: EmailStr
    user_email: EmailStr
    user_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class AdminAlertEmailAuto(BaseModel):
    """Admin alert email using ADMIN_EMAIL from environment"""
    user_email: EmailStr
    user_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ApprovalEmail(EmailBase):
    approved_by: Optional[str] = None


class RejectionEmail(EmailBase):
    reason: Optional[str] = None


class AccessEmail(EmailBase):
    assigned_pocs: List[str] = Field(default_factory=list)


class FullAccessEmail(EmailBase):
    areas: List[str] = Field(default_factory=list)
