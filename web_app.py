#!/usr/bin/env python3
"""
AI-TECH-DAILY WEB DASHBOARD
============================
Flask-based UI for triggering news fetch and scheduling daily runs.

Usage:
    python web_app.py              # Start web server on port 5000
    python web_app.py --port 8080  # Start on custom port
"""

import os
import sys
import json
import re
import logging
import threading
from pathlib import Path
from datetime import datetime

import yaml
from flask import Flask, render_template, jsonify, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo

from src.agent import NewsTechAgent
from src.chat import ChatEngine
from src.utils import setup_logging, load_env_file

app = Flask(__name__)

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ENV_PATH = Path(__file__).parent / ".env"
SCHEDULE_FILE = Path(__file__).parent / ".schedule.json"
OUTPUT_DIR = Path(__file__).parent / "output"
NOTIF_CONFIG_FILE = Path(__file__).parent / ".notifications.json"

logger = logging.getLogger("NewsAgent.Web")

SINGAPORE_TZ = ZoneInfo("Asia/Singapore")
scheduler = BackgroundScheduler(timezone=SINGAPORE_TZ)
config_cache = None
env_cache = None
is_running = threading.Event()
stop_requested = threading.Event()
last_run_status = {
    "status": "idle", 
    "message": "No runs yet", 
    "time": None,
    "previous_run": None,
    "previous_run_status": None
}


# Custom Jinja filters
def extract_date_from_filename(filename: str) -> str:
    """Extract YYYY-MM-DD date from filename like 'techpulse-daily-2026-05-19.md'"""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", filename)
    if m:
        year, month, day = m.groups()
        return f"{day}/{month}/{year}"
    return "N/A"

def format_date_readable(date_str: str) -> str:
    """Convert YYYY-MM-DD to readable format DD Mon YYYY"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except:
        return date_str

app.jinja_env.filters['extract_date'] = extract_date_from_filename
app.jinja_env.filters['format_date'] = format_date_readable


def load_config():
    global config_cache
    if config_cache is None:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config_cache = yaml.safe_load(f)
    return config_cache


def load_env():
    global env_cache
    if env_cache is None:
        env_cache = load_env_file(str(ENV_PATH))
    return env_cache


def load_schedule_config():
    if SCHEDULE_FILE.exists():
        return json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
    return {"enabled": True, "hour": "00", "minute": "00"}


def save_schedule_config(cfg):
    SCHEDULE_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def load_notifications_config():
    cfg = load_config()
    notif_cfg = cfg.get("notifications", {})
    env = load_env()
    return {
        "email": {
            "enabled": notif_cfg.get("email", {}).get("enabled", False),
            "from": env.get("EMAIL_FROM", ""),
            "password": env.get("EMAIL_PASSWORD", ""),
            "to": env.get("EMAIL_TO", ""),
            "smtp_server": env.get("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": env.get("SMTP_PORT", "587"),
            "subject_prefix": notif_cfg.get("email", {}).get("subject_prefix", "[AI-TECH-DAILY]"),
        },
        "whatsapp": {
            "enabled": notif_cfg.get("whatsapp", {}).get("enabled", False),
            "phone": env.get("WHATSAPP_PHONE_NUMBER", ""),
        }
    }


def save_notifications_config(data):
    cfg = load_config()
    env = load_env_file(str(ENV_PATH))

    channel = data.get("channel")
    if channel == "email":
        enabled = data.get("enabled", False)
        cfg.setdefault("notifications", {}).setdefault("email", {})["enabled"] = enabled
        cfg["notifications"]["email"]["subject_prefix"] = data.get("subject_prefix", "[AI-TECH-DAILY]")
        if data.get("from"): env["EMAIL_FROM"] = data["from"]
        if data.get("password"): env["EMAIL_PASSWORD"] = data["password"]
        if data.get("to"): env["EMAIL_TO"] = data["to"]
        if data.get("smtp_server"): env["SMTP_SERVER"] = data["smtp_server"]
        if data.get("smtp_port"): env["SMTP_PORT"] = data["smtp_port"]
    elif channel == "whatsapp":
        enabled = data.get("enabled", False)
        cfg.setdefault("notifications", {}).setdefault("whatsapp", {})["enabled"] = enabled
        if data.get("phone"): env["WHATSAPP_PHONE_NUMBER"] = data["phone"]

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False, allow_unicode=True, width=1000)

    env_lines = []
    if ENV_PATH.exists():
        existing_keys = {}
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key = line.split("=", 1)[0]
                    existing_keys[key] = line
                else:
                    env_lines.append(line)
    for key, value in env.items():
        env_lines.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(env_lines) + "\n", encoding="utf-8")

    global config_cache, env_cache
    config_cache = None
    env_cache = None


def run_news_agent(selected_domains=None):
    global last_run_status
    if is_running.is_set():
        return None
    stop_requested.clear()
    is_running.set()
    try:
        # Store previous run info before updating
        if last_run_status["time"] is not None:
            last_run_status["previous_run"] = last_run_status["time"]
            last_run_status["previous_run_status"] = last_run_status["status"]
        
        cfg = load_config()
        if selected_domains:
            for name in cfg.get("domains", {}):
                cfg["domains"][name]["enabled"] = name in selected_domains
        env = load_env()
        agent = NewsTechAgent(cfg, env)
        
        last_run_status["status"] = "running"
        last_run_status["message"] = "Agent is active..."
        last_run_status["time"] = datetime.now(SINGAPORE_TZ).strftime("%Y-%m-%d %H:%M:%S SGT")
        
        filepath = agent.run_and_notify(stop_event=stop_requested)
        if stop_requested.is_set():
            last_run_status["status"] = "cancelled"
            last_run_status["message"] = "Fetch cancelled by user"
            last_run_status["time"] = datetime.now(SINGAPORE_TZ).strftime("%Y-%m-%d %H:%M:%S SGT")
            logger.info("News fetch cancelled by user")
            return None
        if filepath:
            last_run_status["status"] = "success"
            last_run_status["message"] = f"Report saved: {Path(filepath).name}"
            last_run_status["time"] = datetime.now(SINGAPORE_TZ).strftime("%Y-%m-%d %H:%M:%S SGT")
            logger.info(f"News fetch complete: {filepath}")
        else:
            last_run_status["status"] = "error"
            last_run_status["message"] = "Agent returned no output"
            last_run_status["time"] = datetime.now(SINGAPORE_TZ).strftime("%Y-%m-%d %H:%M:%S SGT")
        return filepath
    except Exception as e:
        last_run_status["status"] = "error"
        last_run_status["message"] = str(e)
        last_run_status["time"] = datetime.now(SINGAPORE_TZ).strftime("%Y-%m-%d %H:%M:%S SGT")
        logger.error(f"News fetch failed: {e}", exc_info=True)
        return None
    finally:
        is_running.clear()
        stop_requested.clear()


def init_scheduler():
    sched_cfg = load_schedule_config()
    if sched_cfg.get("enabled", False):
        hour = int(sched_cfg.get("hour", "08"))
        minute = int(sched_cfg.get("minute", "30"))
        schedule_time = f"{hour:02d}:{minute:02d}"
        trigger = CronTrigger(hour=hour, minute=minute, timezone=SINGAPORE_TZ)
        scheduler.add_job(run_news_agent, trigger, id="daily_news", replace_existing=True)
        logger.info(f"Scheduler started: daily at {schedule_time} (Asia/Singapore)")
        return True, schedule_time
    return False, None


def parse_summary_from_content(content, max_items=5):
    summary = {"domains": [], "generated": None, "total_items": 0}
    match = re.search(r"Generated:\s*(.+?)\s*\|", content)
    if match:
        summary["generated"] = match.group(1).strip()
    domain_pattern = re.compile(r"([A-Z_]+)\s*[-]{2}\s*LATEST NEWS", re.IGNORECASE)
    pos = 0
    while True:
        m = domain_pattern.search(content, pos)
        if not m:
            break
        domain_key = m.group(1)
        domain_name = domain_key.replace("_", " ").title()
        block_start = m.end()
        next_m = domain_pattern.search(content, block_start)
        block_end = next_m.start() if next_m else len(content)
        block = content[block_start:block_end]
        article_titles = re.findall(r"^###\s+\d+\.\s*(.+?)$", block, re.MULTILINE)
        sources = re.findall(r"\*\*Source:\*\*\s*(.+)", block)
        urls = re.findall(r"\*\*URL:\*\*\s*(.+)", block)
        summaries = re.findall(r"\*\*Summary:\*\*\s*(.+)", block)
        items = []
        for i, t in enumerate(article_titles):
            if max_items > 0 and i >= max_items:
                break
            src = sources[i] if i < len(sources) else ""
            url = urls[i] if i < len(urls) else ""
            summ = summaries[i] if i < len(summaries) else ""
            t = t.strip()
            if t and len(t) > 5:
                items.append({"title": t, "source": src, "url": url, "summary": summ})
        if items:
            summary["domains"].append({
                "name": domain_name,
                "count": len(article_titles),
                "highlights": items
            })
            summary["total_items"] += len(article_titles)
        pos = block_end
    return summary if summary["domains"] else None


def parse_latest_summary(filepath=None, max_items=5):
    if not filepath:
        reports = get_reports()
        if not reports:
            return None
        filepath = OUTPUT_DIR / reports[0]["name"]
    if isinstance(filepath, str):
        filepath = Path(filepath)
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding="utf-8")
    return parse_summary_from_content(content, max_items=max_items)


def parse_historical_summary():
    reports = get_reports()
    if len(reports) < 2:
        return None
    combined = {"domains": [], "total_items": 0}
    seen_domains = {}
    for r in reports[1:]:
        content = get_report_content(r["name"])
        if not content:
            continue
        domain_pattern = re.compile(r"([A-Z_]+)\s*[-]{2}\s*LATEST NEWS", re.IGNORECASE)
        pos = 0
        while True:
            m = domain_pattern.search(content, pos)
            if not m:
                break
            domain_key = m.group(1)
            domain_name = domain_key.replace("_", " ").title()
            block_start = m.end()
            next_m = domain_pattern.search(content, block_start)
            block_end = next_m.start() if next_m else len(content)
            block = content[block_start:block_end]
            article_titles = re.findall(r"^###\s+\d+\.\s*(.+?)$", block, re.MULTILINE)
            sources = re.findall(r"\*\*Source:\*\*\s*(.+)", block)
            urls = re.findall(r"\*\*URL:\*\*\s*(.+)", block)
            summaries = re.findall(r"\*\*Summary:\*\*\s*(.+)", block)
            items = []
            for i, t in enumerate(article_titles[:5]):
                src = sources[i] if i < len(sources) else ""
                url = urls[i] if i < len(urls) else ""
                summ = summaries[i] if i < len(summaries) else ""
                t = t.strip()
                if t and len(t) > 5:
                    items.append({"title": t, "source": src, "url": url, "summary": summ})
            if items:
                if domain_name not in seen_domains:
                    seen_domains[domain_name] = {"name": domain_name, "count": 0, "highlights": []}
                    combined["domains"].append(seen_domains[domain_name])
                seen_domains[domain_name]["count"] += len(article_titles)
                existing_titles = {h["title"] for h in seen_domains[domain_name]["highlights"]}
                for item in items:
                    if item["title"] not in existing_titles and len(seen_domains[domain_name]["highlights"]) < 5:
                        seen_domains[domain_name]["highlights"].append(item)
                        existing_titles.add(item["title"])
                combined["total_items"] += len(article_titles)
            pos = block_end
    return combined if combined["domains"] else None


def _extract_date(filename):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    if m:
        return m.group(1)
    return "0000-00-00"


def get_reports():
    if not OUTPUT_DIR.exists():
        return []
    # Sort files by the date embedded in the filename, descending (newest first)
    files = sorted(OUTPUT_DIR.glob("*.md"), key=lambda f: _extract_date(f.name), reverse=True)
    reports = []
    for f in files:
        if f.name == ".gitkeep": continue
        date_str = _extract_date(f.name)
        # Only include reports from 2024 onward
        if date_str < "2024-01-01":
            continue
        stat = f.stat()
        reports.append({
            "name": f.name,
            "path": str(f),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime, SINGAPORE_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        })
    return reports


def get_report_content(filename):
    filepath = OUTPUT_DIR / filename
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    return None


@app.route("/")
def index():
    latest_summary = parse_latest_summary()
    latest_full_summary = parse_latest_summary(max_items=0)

    can_fetch = not is_running.is_set()
    lock_reason = ""
    if is_running.is_set():
        sched_cfg = load_schedule_config()
        if sched_cfg.get("enabled", False):
            sched_hour = int(sched_cfg.get("hour", "08"))
            sched_min = int(sched_cfg.get("minute", "30"))
            lock_reason = f"Scheduled batch running — manual fetch locked until complete"

    return render_template("dashboard.html",
                          reports=get_reports(),
                          schedule=load_schedule_config(),
                          notifications=load_notifications_config(),
                          domains=load_config().get("domains", {}),
                          status=last_run_status,
                          is_running=is_running.is_set(),
                          latest_summary=latest_summary,
                          latest_full_summary=latest_full_summary,
                          historical_summary=parse_historical_summary(),
                          can_fetch=can_fetch,
                          lock_reason=lock_reason)


@app.route("/api/status")
def api_status():
    can_fetch = not is_running.is_set()
    lock_reason = ""
    if is_running.is_set():
        sched_cfg = load_schedule_config()
        if sched_cfg.get("enabled", False):
            sched_hour = int(sched_cfg.get("hour", "08"))
            sched_min = int(sched_cfg.get("minute", "30"))
            lock_reason = f"Scheduled batch running — manual fetch locked until complete"

    return jsonify({
        "status": last_run_status["status"],
        "message": last_run_status["message"],
        "time": last_run_status["time"],
        "previous_run": last_run_status.get("previous_run"),
        "previous_run_status": last_run_status.get("previous_run_status"),
        "is_running": is_running.is_set(),
        "can_fetch": can_fetch,
        "lock_reason": lock_reason,
    })


@app.route("/api/trigger", methods=["POST"])
def api_trigger():
    if is_running.is_set():
        return jsonify({"status": "error", "message": "Scheduled batch is running — wait for it to complete"}), 423

    data = request.json or {}
    selected_domains = data.get("domains", None)

    thread = threading.Thread(target=run_news_agent, args=(selected_domains,))
    thread.start()
    msg = f"Fetching {len(selected_domains)} domains" if selected_domains else "News fetch started"
    return jsonify({"status": "started", "message": msg})


@app.route("/api/cancel", methods=["POST"])
def api_cancel():
    if not is_running.is_set():
        return jsonify({"status": "error", "message": "Nothing is running"}), 400
    stop_requested.set()
    logger.info("Cancel requested — agent will stop after current domain")
    return jsonify({"status": "ok", "message": "Cancelling fetch..."})


@app.route("/api/progress")
def api_progress():
    return jsonify({"running": is_running.is_set()})


@app.route("/api/schedule", methods=["GET"])
def api_schedule_get():
    sched_cfg = load_schedule_config()
    job = scheduler.get_job("daily_news")
    sched_cfg["active"] = job is not None
    
    # Only show next_run if it's valid and in the future
    if job and job.next_run_time:
        sg_time = job.next_run_time.astimezone(SINGAPORE_TZ)
        now = datetime.now(SINGAPORE_TZ)
        # Only include next_run if it's in the future
        if sg_time > now:
            sched_cfg["next_run"] = sg_time.isoformat()
            sched_cfg["next_run_display"] = sg_time.strftime("%d/%m/%Y, %I:%M %p SGT")
        else:
            # If scheduler is enabled but next_run is in the past, show scheduled time based on config
            hour = int(sched_cfg.get("hour", "08"))
            minute = int(sched_cfg.get("minute", "30"))
            sched_cfg["next_run_display"] = ""  # Empty if expired
    elif sched_cfg.get("enabled", False):
        # If enabled but no job, show empty
        sched_cfg["next_run_display"] = ""
    
    # Add previous run time from last_run_status
    if last_run_status.get("time"):
        sched_cfg["last_run"] = last_run_status["time"]
        sched_cfg["last_run_status"] = last_run_status["status"]
    
    return jsonify(sched_cfg)


@app.route("/api/schedule", methods=["POST"])
def api_schedule_set():
    data = request.json
    enabled = data.get("enabled", False)
    hour = int(data.get("hour", "08"))
    minute = int(data.get("minute", "30"))

    sched_cfg = {"enabled": enabled, "hour": str(hour), "minute": str(minute)}
    save_schedule_config(sched_cfg)

    if enabled:
        trigger = CronTrigger(hour=hour, minute=minute, timezone=SINGAPORE_TZ)
        scheduler.add_job(run_news_agent, trigger, id="daily_news", replace_existing=True)
        schedule_time = f"{hour:02d}:{minute:02d}"
        logger.info(f"Schedule updated: daily at {schedule_time} (Asia/Singapore)")
        return jsonify({"status": "ok", "message": f"Daily schedule set to {schedule_time}", "active": True})
    else:
        job = scheduler.get_job("daily_news")
        if job:
            job.remove()
            logger.info("Scheduler disabled")
        return jsonify({"status": "ok", "message": "Schedule disabled", "active": False})


@app.route("/api/reports")
def api_reports():
    return jsonify(get_reports())


@app.route("/api/report-articles/<filename>")
def api_report_articles(filename):
    content = get_report_content(filename)
    if not content:
        return jsonify({"error": "Report not found"}), 404
    summary = parse_summary_from_content(content, max_items=0)
    if not summary:
        return jsonify({"domains": [], "total_items": 0, "generated": None})
    return jsonify(summary)


@app.route("/api/reports/<filename>")
def api_report_view(filename):
    content = get_report_content(filename)
    if content:
        return jsonify({"name": filename, "content": content})
    return jsonify({"error": "Report not found"}), 404


@app.route("/api/reports/<filename>/download")
def api_report_download(filename):
    filepath = OUTPUT_DIR / filename
    if filepath.exists():
        from flask import send_file
        return send_file(filepath, as_attachment=True)
    return jsonify({"error": "Report not found"}), 404


@app.route("/api/summary")
def api_summary():
    reports = get_reports()
    if not reports:
        return jsonify({"error": "No reports found"}), 404
    summary = parse_latest_summary(OUTPUT_DIR / reports[0]["name"])
    if summary:
        summary["filename"] = reports[0]["name"]
        return jsonify(summary)
    return jsonify({"error": "Could not parse summary"}), 404


@app.route("/api/summary/<path:filename>")
def api_summary_for(filename):
    content = get_report_content(filename)
    if not content:
        return jsonify({"error": "Report not found"}), 404
    summary = parse_summary_from_content(content, max_items=999)
    if summary:
        summary["filename"] = filename
        return jsonify(summary)
    return jsonify({"error": "Could not parse summary"}), 404


@app.route("/api/notifications", methods=["GET"])
def api_notifications_get():
    return jsonify(load_notifications_config())


@app.route("/api/notifications", methods=["POST"])
def api_notifications_set():
    data = request.json
    channel = data.get("channel")
    if channel not in ("email", "whatsapp"):
        return jsonify({"status": "error", "message": "Invalid channel"}), 400

    save_notifications_config(data)
    enabled = data.get("enabled", False)
    logger.info(f"Notification {channel} {'enabled' if enabled else 'disabled'}")
    return jsonify({"status": "ok", "message": f"{channel.capitalize()} notifications {'enabled' if enabled else 'disabled'}"})


@app.route("/api/domains", methods=["GET"])
def api_domains_get():
    cfg = load_config()
    domains = cfg.get("domains", {})
    result = []
    for name, config in domains.items():
        result.append({
            "name": name,
            "enabled": config.get("enabled", True),
            "keywords": config.get("keywords", [])[:3],
            "source_count": len(config.get("sources", [])),
        })
    return jsonify(result)


@app.route("/api/domains", methods=["POST"])
def api_domains_set():
    data = request.json
    domain_name = data.get("name")
    enabled = data.get("enabled", True)
    cfg = load_config()
    if domain_name in cfg.get("domains", {}):
        cfg["domains"][domain_name]["enabled"] = enabled
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(cfg, f, default_flow_style=False, allow_unicode=True, width=1000)
        global config_cache
        config_cache = None
        logger.info(f"Domain {domain_name} {'enabled' if enabled else 'disabled'}")
        return jsonify({"status": "ok", "message": f"{domain_name} {'enabled' if enabled else 'disabled'}"})
    return jsonify({"status": "error", "message": "Domain not found"}), 404


@app.route("/api/domains/batch", methods=["POST"])
def api_domains_batch():
    data = request.json
    enabled_names = set(data.get("domains", []))
    cfg = load_config()
    for name in cfg.get("domains", {}):
        cfg["domains"][name]["enabled"] = name in enabled_names
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False, allow_unicode=True, width=1000)
    global config_cache
    config_cache = None
    logger.info(f"Domains updated: {len(enabled_names)} enabled")
    return jsonify({"status": "ok"})


@app.route("/api/notifications/test", methods=["POST"])
def api_notifications_test():
    data = request.json
    channel = data.get("channel", "email")

    cfg = load_config()
    env = load_env()
    agent = NewsTechAgent(cfg, env)

    test_msg = f"AI-TECH-DAILY Test Notification\n\nThis is a test message from your AI-TECH-DAILY dashboard.\n\nIf you receive this, notifications are working correctly.\n\nTimestamp: {datetime.now(SINGAPORE_TZ).strftime('%Y-%m-%d %H:%M:%S')} SGT"

    if channel == "email":
        ok = agent.email_notifier.send(test_msg, None)
        return jsonify({"status": "ok" if ok else "error", "message": "Test email sent" if ok else "Email send failed — check credentials and logs"})
    elif channel == "whatsapp":
        ok = agent.whatsapp_notifier.send(test_msg)
        return jsonify({"status": "ok" if ok else "error", "message": "Test WhatsApp sent" if ok else "WhatsApp send failed — check credentials and logs"})

    return jsonify({"status": "error", "message": "Invalid channel"}), 400


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Question is required"}), 400

    mode = data.get("mode", "report")
    history = data.get("history", [])

    content = ""
    if mode == "report":
        reports = get_reports()
        if reports:
            content = get_report_content(reports[0]["name"]) or ""

    cfg = load_config()
    env = load_env()
    engine = ChatEngine(cfg, env)
    result = engine.ask(question, report_content=content, mode=mode, history=history)
    return jsonify(result)


@app.route("/view-report/<path:filename>")
def view_report_page(filename):
    content = get_report_content(filename)
    if content:
        report_data = parse_summary_from_content(content, max_items=999)
        reports = get_reports()
        prev_report = None
        next_report = None
        for i, r in enumerate(reports):
            if r["name"] == filename:
                if i < len(reports) - 1:
                    prev_report = reports[i + 1]
                if i > 0:
                    next_report = reports[i - 1]
                break
        return render_template("report_view.html", filename=filename, content=content, report_data=report_data, reports=reports, prev_report=prev_report, next_report=next_report)
    return "Report not found", 404


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI-TECH-DAILY Web Dashboard")
    parser.add_argument("--port", type=int, default=5000, help="Port to run on (default: 5000)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    args = parser.parse_args()

    setup_logging(str(Path(__file__).parent / "news_agent.log"))

    logger.info("Starting AI-TECH-DAILY Web Dashboard")
    init_scheduler()

    print(f"\n{'='*50}")
    print(f"AI-TECH-DAILY Web Dashboard")
    print(f"{'='*50}")
    print(f"Server: http://localhost:{args.port}")
    print(f"Press Ctrl+C to stop\n")

    scheduler.start()

    try:
        app.run(host=args.host, port=args.port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
