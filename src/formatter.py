from datetime import datetime, timezone
from typing import List, Dict
from zoneinfo import ZoneInfo
from src.sources import NewsItem
from src.curator import CuratorAgent

SGT = ZoneInfo("Asia/Singapore")

def format_date_for_report(dt: datetime = None) -> str:
    """Format date as YYYY-MM-DD HH:MM SGT (includes year, month, day, hour, minute)"""
    if dt is None:
        dt = datetime.now(SGT)
    return dt.strftime("%Y-%m-%d %H:%M SGT")

def format_date_readable(dt: datetime = None) -> str:
    """Format date as readable: 'DD Mon YYYY HH:MM SGT' (e.g., '19 May 2026 11:29 SGT')"""
    if dt is None:
        dt = datetime.now(SGT)
    return dt.strftime("%d %b %Y %H:%M SGT")

class NotepadPPFormatter:
    def __init__(self, config: dict):
        self.config = config

    def format_section(self, title: str, items: List[NewsItem]) -> str:
        if not items:
            return ""
        max_items = self.config.get("output", {}).get("max_items_per_section", 25)
        items = items[:max_items]

        lines = []
        lines.append(f"## {title}")
        lines.append("")

        for idx, item in enumerate(items, 1):
            title_text = item.title.replace("\n", " ").replace("\r", "")
            summary_text = item.summary.replace("\n", " ").replace("\r", "") if item.summary else ""
            lines.append(f"### {idx}. {title_text}")
            lines.append(f"- **Source:** {item.source}")
            lines.append(f"- **URL:** {item.url if item.url else 'N/A'}")
            if summary_text:
                lines.append(f"- **Summary:** {summary_text}")
            lines.append("")

        return "\n".join(lines)

    def build_full_report(self, domain_data: Dict[str, Dict]) -> str:
        now = datetime.now(SGT).strftime("%Y-%m-%d %H:%M SGT")
        lines = []
        title = "TechPulse Daily -- Comprehensive Tech & Industry Digest"
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"> **Generated:** {now} | **Sources:** RSS + Web | **Mode:** AI-Curated")
        lines.append("")

        total_items = 0
        for domain_name, data in domain_data.items():
            curated = data.get("curated", [])
            if curated:
                section_title = f"{domain_name.upper()} -- LATEST NEWS"
                section = self.format_section(section_title, curated)
                lines.append(section)
                total_items += len(curated)

        lines.append("---")
        lines.append(f"**Total Articles:** {total_items}")
        lines.append(f"*End of Report — TechPulse Daily*")
        return "\n".join(lines)

    def save_report(self, report: str, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        return filepath
