import smtplib
import logging
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional

logger = logging.getLogger("NewsAgent.Email")

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.yaml"
ENV_PATH = Path(__file__).parent.parent.parent / ".env"

def load_env_file(filepath):
    env = {}
    if Path(filepath).exists():
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip()
    return env

class EmailNotifier:
    def __init__(self, config: dict, env_vars: dict):
        self.config = config
        self.env = env_vars
        self.enabled = config.get("notifications", {}).get("email", {}).get("enabled", False)

    def _load_latest_config(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
                self.enabled = cfg.get("notifications", {}).get("email", {}).get("enabled", self.enabled)
        env = load_env_file(str(ENV_PATH))
        self.env.update(env)

    def send(self, report_text: str, report_file: Optional[str] = None) -> bool:
        self._load_latest_config()
        if not self.enabled:
            logger.info("Email notifier disabled in config")
            return False

        email_from = self.env.get("EMAIL_FROM", "")
        email_to = self.env.get("EMAIL_TO", "")
        password = self.env.get("EMAIL_PASSWORD", "")
        smtp_server = self.env.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(self.env.get("SMTP_PORT", "587"))
        prefix = self.config.get("notifications", {}).get("email", {}).get("subject_prefix", "[AI-TECH]")

        if not email_from or not email_to or not password:
            logger.warning("Email credentials not configured")
            return False

        msg = MIMEMultipart("alternative")
        msg["From"] = email_from
        msg["To"] = email_to
        msg["Subject"] = f"{prefix} Daily AI-Tech Report"

        html = f"""<html><body style="font-family:-apple-system,sans-serif;padding:20px;background:#f5f5f7;">
        <div style="max-width:600px;margin:0 auto;background:white;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <h1 style="font-size:1.5rem;color:#1d1d1f;margin-bottom:8px;">AI-TECH-DAILY Report</h1>
        <p style="color:#86868b;font-size:0.875rem;margin-bottom:16px;">Your daily AI technology news summary</p>
        <pre style="background:#f5f5f7;padding:16px;border-radius:8px;font-size:0.813rem;line-height:1.6;overflow-x:auto;font-family:Consolas,monospace;">
{report_text}
        </pre>
        </div></body></html>"""
        msg.attach(MIMEText(html, "html"))

        if report_file:
            with open(report_file, "r", encoding="utf-8") as f:
                attachment = MIMEText(f.read())
                attachment.add_header("Content-Disposition", "attachment", filename=Path(report_file).name)
                msg.attach(attachment)

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_from, password)
            server.send_message(msg)
            server.quit()
            logger.info(f"Email sent to {email_to}")
            return True
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False
