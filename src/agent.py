import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Dict, List, Optional

from src.sources import SourceFetcher, NewsItem
from src.curator import CuratorAgent
from src.formatter import NotepadPPFormatter
from src.notifiers.email_notifier import EmailNotifier
from src.notifiers.whatsapp_notifier import WhatsAppNotifier
from src.utils import sanitize_filename, ensure_dir

logger = logging.getLogger("NewsAgent.Agent")

class NewsTechAgent:
    def __init__(self, config: dict, env_vars: dict):
        self.config = config
        self.env = env_vars
        self.fetcher = SourceFetcher(config)
        self.curator = CuratorAgent(config)
        self.formatter = NotepadPPFormatter(config)
        self.email_notifier = EmailNotifier(config, env_vars)
        self.whatsapp_notifier = WhatsAppNotifier(config, env_vars)
        self.results: Dict[str, Dict] = {}

    def run_domain(self, domain_name: str, domain_config: dict) -> Dict:
        logger.info(f"{'='*60}")
        logger.info(f"Processing domain: {domain_name}")
        logger.info(f"{'='*60}")

        if not domain_config.get("enabled", True):
            logger.info(f"Domain {domain_name} disabled, skipping")
            return {"items": [], "curated": []}

        keywords = domain_config.get("keywords", [])
        sources = domain_config.get("sources", [])
        max_src = self.config.get("agent", {}).get("max_sources_per_domain", 5)
        sources = sources[:max_src]

        all_items = self.fetcher.fetch_all(sources)
        curated = self.curator.curate(all_items, keywords)

        logger.info(f"Domain {domain_name}: {len(all_items)} fetched, {len(curated)} curated")
        return {"items": all_items, "curated": curated}

    def run_all(self, stop_event=None):
        domains = self.config.get("domains", {})
        for domain_name, domain_config in domains.items():
            if stop_event and stop_event.is_set():
                logger.info(f"Stop requested — cancelling after {domain_name}")
                break
            self.results[domain_name] = self.run_domain(domain_name, domain_config)
        return self.results

    def generate_report(self) -> str:
        report = self.formatter.build_full_report(self.results)
        return report

    def save_report(self, report: str) -> str:
        prefix = self.config.get("output", {}).get("filename_prefix", "techpulse-daily")
        save_dir = self.config.get("output", {}).get("save_path", "output")
        ensure_dir(save_dir)
        filename = f"{sanitize_filename(prefix)}.md"
        filepath = os.path.join(save_dir, filename)
        self.formatter.save_report(report, filepath)
        logger.info(f"Report saved: {filepath}")
        return filepath

    def notify(self, report: str, filepath: Optional[str] = None):
        self.email_notifier.send(report, filepath)
        self.whatsapp_notifier.send(report)

    def run_and_notify(self, stop_event=None):
        try:
            logger.info(f"{'='*60}")
            logger.info(f"AI-TECH-DAILY AGENT STARTED at {datetime.now(ZoneInfo('Asia/Singapore')).strftime('%Y-%m-%d %H:%M:%S SGT')}")
            logger.info(f"{'='*60}")
            self.run_all(stop_event)
            cancelled = stop_event and stop_event.is_set()
            if not cancelled:
                report = self.generate_report()
                filepath = self.save_report(report)
                self.notify(report, filepath)
                logger.info("Agent run complete successfully")
                return filepath
            else:
                logger.info("Agent run cancelled by user")
                return None
        except Exception as e:
            logger.error(f"Agent run failed: {e}", exc_info=True)
            return None
