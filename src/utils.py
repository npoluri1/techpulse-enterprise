import os
import re
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

def setup_logging(log_file="news_agent.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("NewsAgent")

def sanitize_filename(prefix: str) -> str:
    date_str = datetime.now(ZoneInfo("Asia/Singapore")).strftime("%Y-%m-%d")
    clean = re.sub(r"[^\w\-]", "", prefix.replace(" ", "-"))
    return f"{clean}-{date_str}"

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def load_env_file(env_path=".env"):
    env_file = Path(env_path)
    if not env_file.exists():
        return {}
    envs = {}
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        envs[key.strip()] = val.strip()
    return envs

def truncate(text: str, max_len: int = 100) -> str:
    return text[:max_len] + "..." if len(text) > max_len else text
