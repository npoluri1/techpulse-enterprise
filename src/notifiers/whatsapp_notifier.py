import logging
import time
import yaml
from pathlib import Path
from typing import Optional

logger = logging.getLogger("NewsAgent.WhatsApp")

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

class WhatsAppNotifier:
    def __init__(self, config: dict, env_vars: dict):
        self.config = config
        self.env = env_vars
        self.enabled = config.get("notifications", {}).get("whatsapp", {}).get("enabled", False)

    def _load_latest_config(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
                self.enabled = cfg.get("notifications", {}).get("whatsapp", {}).get("enabled", self.enabled)
        env = load_env_file(str(ENV_PATH))
        self.env.update(env)

    def send_twilio(self, phone: str, message: str) -> bool:
        account_sid = self.env.get("TWILIO_ACCOUNT_SID", "")
        auth_token = self.env.get("TWILIO_AUTH_TOKEN", "")
        twilio_from = self.env.get("TWILIO_WHATSAPP_NUMBER", "")
        if not account_sid or not auth_token or not twilio_from:
            return False
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)
            msg = client.messages.create(
                body=message,
                from_=f"whatsapp:{twilio_from}",
                to=f"whatsapp:{phone}"
            )
            logger.info(f"Twilio WhatsApp sent to {phone} (SID: {msg.sid})")
            return True
        except Exception as e:
            logger.error(f"Twilio WhatsApp failed: {e}")
            return False

    def send_pywhatkit(self, phone: str, message: str) -> bool:
        try:
            import pywhatkit
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=20,
                tab_close=True
            )
            logger.info(f"pywhatkit message sent to {phone}")
            return True
        except Exception as e:
            logger.warning(f"pywhatkit failed: {e}")
            return False

    def send(self, report_text: str) -> bool:
        self._load_latest_config()
        if not self.enabled:
            logger.info("WhatsApp notifier disabled in config")
            return False

        phone = self.env.get("WHATSAPP_PHONE_NUMBER", "")
        if not phone:
            logger.warning("WhatsApp phone number not configured")
            return False

        preview = report_text[:1500] if len(report_text) > 1500 else report_text
        preview = preview.replace("=" * 80, "\n" + "=" * 40 + "\n")

        if self.send_twilio(phone, preview):
            return True

        if self.send_pywhatkit(phone, preview):
            return True

        logger.info(f"\n{'='*40}\nWHATSAPP MESSAGE (copy to phone):\n{'='*40}\n{preview}\n{'='*40}\n")
        return False
