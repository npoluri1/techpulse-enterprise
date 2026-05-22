#!/usr/bin/env python3
"""
AI-TECH-DAILY NEWS AGENT
========================
Automated daily news aggregator for AI Agents, Quantum Computing, and Robotics.
Fetches from RSS + web sources, curates via keyword relevance, outputs in
Notepad++ tabular format, and sends via Email / WhatsApp.

Usage:
    python main.py              # Run once immediately
    python main.py --schedule   # Run on daily schedule (configurable in config.yaml)
    python main.py --test       # Quick test mode (1 source per domain)
"""

import os
import sys
import argparse
import logging
import time
from pathlib import Path

import yaml
import schedule

from src.agent import NewsTechAgent
from src.utils import setup_logging, load_env_file

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ENV_PATH = Path(__file__).parent / ".env"

logger = logging.getLogger("NewsAgent")

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config file not found: {CONFIG_PATH}")
        print("Creating default config.yaml...")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_agent(config: dict, env_vars: dict):
    agent = NewsTechAgent(config, env_vars)
    filepath = agent.run_and_notify()
    if filepath:
        print(f"\nReport saved: {os.path.abspath(filepath)}")
    return filepath

def run_scheduled(config: dict, env_vars: dict):
    schedule_hour = os.environ.get("SCHEDULE_HOUR",
                    env_vars.get("SCHEDULE_HOUR", "08"))
    schedule_min = os.environ.get("SCHEDULE_MINUTE",
                    env_vars.get("SCHEDULE_MINUTE", "00"))

    schedule_time = f"{schedule_hour}:{schedule_min}"
    schedule.every().day.at(schedule_time).do(run_agent, config, env_vars)

    logger.info(f"Scheduler started. Next run daily at {schedule_time}")
    print(f"Scheduler started. Will run daily at {schedule_time}")
    print("Press Ctrl+C to stop.")

    run_agent(config, env_vars)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

def main():
    parser = argparse.ArgumentParser(
        description="AI-TECH-DAILY News Agent — AI Agents + Quantum + Robotics"
    )
    parser.add_argument("--schedule", action="store_true",
                        help="Run on daily schedule")
    parser.add_argument("--test", action="store_true",
                        help="Quick test mode (reduced sources)")
    parser.add_argument("--init-env", action="store_true",
                        help="Create .env file from .env.example")
    args = parser.parse_args()

    if args.init_env:
        example = Path(__file__).parent / ".env.example"
        env_file = Path(__file__).parent / ".env"
        if example.exists() and not env_file.exists():
            env_file.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"Created .env from .env.example — edit it with your credentials")
        elif env_file.exists():
            print(f".env already exists")
        return

    log_file = Path(__file__).parent / "news_agent.log"
    setup_logging(str(log_file))

    config = load_config()

    if args.test:
        for domain in config.get("domains", {}).values():
            if domain.get("sources"):
                domain["sources"] = domain["sources"][:1]
        logger.info("TEST MODE: 1 source per domain")

    env_vars = load_env_file(str(ENV_PATH))

    if args.schedule:
        run_scheduled(config, env_vars)
    else:
        run_agent(config, env_vars)

if __name__ == "__main__":
    main()
