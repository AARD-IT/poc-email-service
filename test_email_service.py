#!/usr/bin/env python
"""
Test script for Analytics Avenue Email Service

Usage:
    python test_email_service.py

This script tests all email endpoints including the new admin alert auto feature.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/email"

def test_debug_env():
    """Test the debug endpoint to verify environment variables"""
    print("=" * 60)
    print("TEST: Debug Environment Variables")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/debug-env?show_values=true")
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print("\nEnvironment Variables:")
    for key, value in data['env'].items():
        print(f"  {key}: {value}")
    
    print("\nEnvironment Present:")
    for key, present in data['present'].items():
        print(f"  {key}: {present}")
    print()


def test_admin_alert_auto():
    """Test the new admin alert auto endpoint - uses ADMIN_EMAIL from .env"""
    print("=" * 60)
    print("TEST: Admin Alert (Auto - uses ADMIN_EMAIL from env)")
    print("=" * 60)
    
    payload = {
        "user_email": "newuser@example.com",
        "user_name": "John Doe",
        "details": {
            "source": "web_signup",
            "signup_date": "2026-05-27",
            "company": "Example Corp"
        }
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/send-admin-alert-auto", json=payload)
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_welcome_email():
    """Test the welcome email endpoint"""
    print("=" * 60)
    print("TEST: Welcome Email")
    print("=" * 60)
    
    payload = {
        "recipient": "user@example.com",
        "name": "Jane Smith",
        "signup_source": "web"
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/send-welcome", json=payload)
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_admin_alert_manual():
    """Test the original admin alert endpoint - requires explicit admin_email"""
    print("=" * 60)
    print("TEST: Admin Alert (Manual - explicit admin_email)")
    print("=" * 60)
    
    payload = {
        "admin_email": "custom.admin@example.com",
        "user_email": "another.user@example.com",
        "user_name": "Alice Johnson",
        "details": {"reason": "API test"}
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/send-admin-alert", json=payload)
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


if __name__ == "__main__":
    try:
        print("\n🚀 Analytics Avenue Email Service Test Suite\n")
        
        # Test environment first
        test_debug_env()
        
        # Test new auto admin alert (recommended for signup workflows)
        test_admin_alert_auto()
        
        # Test welcome email
        test_welcome_email()
        
        # Test manual admin alert for comparison
        test_admin_alert_manual()
        
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure the email service is running:")
        print("  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
