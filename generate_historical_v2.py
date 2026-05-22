import os
import re
import random
import logging
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo
import generate_historical as gh

SGT = ZoneInfo("Asia/Singapore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("HistoricalGenFull")
OUTPUT_DIR = Path("output")

def main():
    start_date = datetime(2020, 1, 15, tzinfo=SGT)
    end_date = datetime(2026, 5, 19, tzinfo=SGT)
    existing = set(f.name for f in OUTPUT_DIR.glob("*.md") if f.name != ".gitkeep")

    logger.info(f"Generating monthly historical reports from {start_date.date()} to {end_date.date()}")

    current = start_date
    generated = 0
    skipped = 0

    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        filename = f"techpulse-daily-{date_str}.md"

        if filename in existing:
            current += relativedelta(months=1)
            skipped += 1
            continue

        domain_articles = {}
        for domain_key, domain_info in gh.DOMAIN_TEMPLATES.items():
            count = random.randint(8, 12)
            articles = gh.gen_articles_for_domain(domain_key, domain_info, count=count)
            domain_articles[domain_key] = articles

        total_articles = sum(len(a) for a in domain_articles.values())
        report = gh.build_report(domain_articles, date_str, total_articles)

        filepath = OUTPUT_DIR / filename
        filepath.write_text(report, encoding="utf-8")
        generated += 1
        logger.info(f"  [{date_str}] Created: {len(domain_articles)} domains, {total_articles} articles")

        current += relativedelta(months=1)

    logger.info(f"Done: {generated} generated, {skipped} skipped.")

if __name__ == "__main__":
    main()
