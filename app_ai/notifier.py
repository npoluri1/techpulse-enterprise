"""
NovaPulse AI - Notification Module
==================================
Email & WhatsApp notification sending for scheduled news fetches.
Reads config from .notifications.json file and sends via SMTP/Twilio.
"""

import os
import json
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger("NewsAI.Notifier")

NOTIF_CONFIG_PATH = Path(__file__).parent.parent / ".notifications.json"
SCHEDULE_CONFIG_PATH = Path(__file__).parent.parent / ".schedule.json"

DEFAULT_NOTIF_CONFIG = {
    "email": {
        "enabled": False,
        "from_email": "",
        "password": "",
        "to_email": "",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "subject_prefix": "[NovaPulse AI]"
    },
    "whatsapp": {
        "enabled": False,
        "account_sid": "",
        "auth_token": "",
        "from_number": "",
        "to_number": ""
    }
}

DEFAULT_SCHEDULE_CONFIG = {
    "enabled": False,
    "hour": 6,
    "minute": 0,
    "timezone": "UTC"
}


def load_notif_config() -> Dict[str, Any]:
    """Load notification configuration from JSON file."""
    if NOTIF_CONFIG_PATH.exists():
        try:
            with open(NOTIF_CONFIG_PATH, "r") as f:
                cfg = json.load(f)
                # Merge with defaults for any missing keys
                for section in DEFAULT_NOTIF_CONFIG:
                    if section not in cfg:
                        cfg[section] = DEFAULT_NOTIF_CONFIG[section].copy()
                    else:
                        for key in DEFAULT_NOTIF_CONFIG[section]:
                            if key not in cfg[section]:
                                cfg[section][key] = DEFAULT_NOTIF_CONFIG[section][key]
                return cfg
        except Exception as e:
            logger.warning(f"Failed to load notifications config: {e}")
    return DEFAULT_NOTIF_CONFIG.copy()


def save_notif_config(cfg: Dict[str, Any]) -> bool:
    """Save notification configuration to JSON file."""
    try:
        with open(NOTIF_CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)
        logger.info("Notification config saved")
        return True
    except Exception as e:
        logger.error(f"Failed to save notifications config: {e}")
        return False


def load_schedule_config() -> Dict[str, Any]:
    """Load schedule configuration from JSON file."""
    if SCHEDULE_CONFIG_PATH.exists():
        try:
            with open(SCHEDULE_CONFIG_PATH, "r") as f:
                cfg = json.load(f)
                for key in DEFAULT_SCHEDULE_CONFIG:
                    if key not in cfg:
                        cfg[key] = DEFAULT_SCHEDULE_CONFIG[key]
                return cfg
        except Exception as e:
            logger.warning(f"Failed to load schedule config: {e}")
    return DEFAULT_SCHEDULE_CONFIG.copy()


def save_schedule_config(cfg: Dict[str, Any]) -> bool:
    """Save schedule configuration to JSON file."""
    try:
        with open(SCHEDULE_CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)
        logger.info("Schedule config saved")
        return True
    except Exception as e:
        logger.error(f"Failed to save schedule config: {e}")
        return False


def send_email_notification(
    subject: str,
    body_text: str,
    config: Dict[str, Any] = None
) -> bool:
    """
    Send an email notification using SMTP.
    Returns True if successful, False otherwise.
    """
    if config is None:
        config = load_notif_config()

    email_cfg = config.get("email", {})
    if not email_cfg.get("enabled", False):
        logger.info("Email notifications disabled")
        return False

    from_email = email_cfg.get("from_email", "")
    to_email = email_cfg.get("to_email", "")
    password = email_cfg.get("password", "")
    smtp_server = email_cfg.get("smtp_server", "smtp.gmail.com")
    smtp_port = int(email_cfg.get("smtp_port", 587))
    prefix = email_cfg.get("subject_prefix", "[NovaPulse AI]")

    if not from_email or not to_email or not password:
        logger.warning("Email credentials not fully configured")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = f"{prefix} {subject}"

    # HTML version
    html = f"""<html><body style="font-family:-apple-system,sans-serif;padding:20px;background:#f5f5f7;">
    <div style="max-width:600px;margin:0 auto;background:white;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,0.08);">
    <h1 style="font-size:1.5rem;color:#1d1d1f;margin-bottom:8px;">{subject}</h1>
    <p style="color:#86868b;font-size:0.875rem;margin-bottom:16px;">From NovaPulse AI</p>
    <pre style="background:#f5f5f7;padding:16px;border-radius:8px;font-size:0.813rem;line-height:1.6;overflow-x:auto;font-family:Consolas,monospace;">
{body_text[:5000]}
    </pre>
    <hr style="border:none;border-top:1px solid #e8e8ed;margin:16px 0;">
    <p style="font-size:0.75rem;color:#86868b;">Sent by NovaPulse AI - Your intelligent news companion</p>
    </div></body></html>"""
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        logger.info(f"Email notification sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        return False


def send_whatsapp_notification(
    message: str,
    config: Dict[str, Any] = None
) -> bool:
    """
    Send a WhatsApp notification using Twilio.
    Returns True if successful, False otherwise.
    """
    if config is None:
        config = load_notif_config()

    wa_cfg = config.get("whatsapp", {})
    if not wa_cfg.get("enabled", False):
        logger.info("WhatsApp notifications disabled")
        return False

    account_sid = wa_cfg.get("account_sid", "")
    auth_token = wa_cfg.get("auth_token", "")
    from_number = wa_cfg.get("from_number", "")
    to_number = wa_cfg.get("to_number", "")

    if not account_sid or not auth_token or not from_number or not to_number:
        logger.warning("WhatsApp credentials not fully configured")
        return False

    try:
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=message[:1600],
            from_=f"whatsapp:{from_number}",
            to=f"whatsapp:{to_number}"
        )
        logger.info(f"WhatsApp notification sent (SID: {msg.sid})")
        return True
    except ImportError:
        logger.warning("twilio package not installed. Install with: pip install twilio")
        return False
    except Exception as e:
        logger.error(f"WhatsApp send failed: {e}")
        return False


def send_notifications(subject: str, body_text: str) -> Dict[str, bool]:
    """Send both email and WhatsApp notifications. Returns results dict."""
    config = load_notif_config()
    results = {
        "email": False,
        "whatsapp": False
    }

    if config.get("email", {}).get("enabled", False):
        results["email"] = send_email_notification(subject, body_text, config)

    if config.get("whatsapp", {}).get("enabled", False):
        results["whatsapp"] = send_whatsapp_notification(body_text, config)

    return results


def test_notification(channel: str) -> Dict[str, Any]:
    """Send a test notification for the given channel."""
    config = load_notif_config()
    test_msg = f"This is a test notification from NovaPulse AI.\n\nTimestamp: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    if channel == "email":
        success = send_email_notification("Test Notification", test_msg, config)
        return {"status": "ok" if success else "error", "message": "Test email sent" if success else "Email failed - check credentials"}
    elif channel == "whatsapp":
        success = send_whatsapp_notification(test_msg, config)
        return {"status": "ok" if success else "error", "message": "Test WhatsApp sent" if success else "WhatsApp failed - check credentials"}
    else:
        return {"status": "error", "message": f"Unknown channel: {channel}"}
