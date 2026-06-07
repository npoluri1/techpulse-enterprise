"""
NovaPulse AI - Newsletter Generator
====================================
Generates and sends formatted HTML email newsletters
with top articles, trending topics, and AI summaries.
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

logger = logging.getLogger("NewsAI.Newsletter")

NEWSLETTER_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
<table width="100%%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f7;">
<tr><td style="padding:20px 10px;">
<table width="600" cellpadding="0" cellspacing="0" style="margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
<tr><td style="padding:32px 32px 20px;background:linear-gradient(135deg,#000000,#1a1a2e,#16213e);">
<table width="100%%" cellpadding="0" cellspacing="0">
<tr><td style="text-align:center;">
<div style="width:48px;height:48px;background:linear-gradient(135deg,#0071e3,#40a9ff);border-radius:14px;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-size:20px;font-weight:800;margin-bottom:12px;">N</div>
<h1 style="color:#ffffff;font-size:24px;font-weight:700;margin:0 0 4px;letter-spacing:-0.02em;">NovaPulse AI</h1>
<p style="color:rgba(255,255,255,0.6);font-size:14px;margin:0;">{SUBJECT}</p>
<p style="color:rgba(255,255,255,0.4);font-size:12px;margin:8px 0 0;">{DATE}</p>
</td></tr></table>
</td></tr>
<tr><td style="padding:24px 32px 8px;">
<h2 style="font-size:18px;font-weight:700;color:#1d1d1f;margin:0 0 4px;letter-spacing:-0.02em;">{HEADLINE}</h2>
<p style="font-size:14px;color:#86868b;margin:0 0 16px;line-height:1.5;">{SUMMARY_TEXT}</p>
</td></tr>
<tr><td style="padding:0 32px;">
<table width="100%%" cellpadding="0" cellspacing="0">
{ARTICLES_HTML}
</table>
</td></tr>
<tr><td style="padding:16px 32px 8px;">
<table width="100%%" cellpadding="0" cellspacing="0">
<tr><td style="background:#f5f5f7;border-radius:12px;padding:16px;">
<h3 style="font-size:14px;font-weight:700;color:#1d1d1f;margin:0 0 8px;">🔥 Trending Topics</h3>
<p style="font-size:13px;color:#86868b;line-height:1.6;margin:0;">{TRENDING_TOPICS}</p>
</td></tr></table>
</td></tr>
<tr><td style="padding:24px 32px;">
<table width="100%%" cellpadding="0" cellspacing="0">
<tr><td style="text-align:center;">
<a href="{PORTAL_URL}" style="display:inline-block;padding:12px 28px;background:#0071e3;color:#ffffff;text-decoration:none;border-radius:12px;font-size:14px;font-weight:600;">Read Full News Portal →</a>
</td></tr></table>
</td></tr>
<tr><td style="padding:16px 32px 24px;border-top:1px solid #e8e8ed;">
<p style="font-size:11px;color:#aeaeb2;text-align:center;margin:0;line-height:1.5;">
Sent by NovaPulse AI · Your intelligent news companion<br>
{UNSUBSCRIBE}<br>
© {YEAR} NovaPulse AI
</p>
</td></tr></table>
</td></tr></table>
</body>
</html>"""


def generate_newsletter_html(
    articles: List[Dict[str, Any]],
    trending_topics: List[str],
    frequency: str = "weekly",
    portal_url: str = "http://localhost:8000",
    unsubscribe_token: str = ""
) -> str:
    """Generate a formatted HTML newsletter from articles."""
    subject = f"Your {frequency.title()} AI News Digest"
    headline = f"Your {frequency.title()} AI News Digest"
    
    date_str = datetime.now().strftime("%d %B %Y")
    article_count = len(articles)
    summary_text = f"Here are the top {article_count} AI and tech stories curated for you this {frequency}. Stay ahead with the latest breakthroughs, tools, and industry insights."

    # Build articles HTML
    articles_html_parts = []
    for i, a in enumerate(articles[:10]):
        title = a.get("title", "Untitled")
        source = a.get("source", "Unknown")
        summary = (a.get("summary") or a.get("content", "") or "")[:200]
        url = a.get("url", "#")
        category = a.get("category", "General").replace("_", " ").title()
        score = a.get("score", 0)
        
        articles_html_parts.append(f"""
<tr><td style="padding:12px 0;border-bottom:1px solid #e8e8ed;">
<table width="100%%" cellpadding="0" cellspacing="0">
<tr><td>
<span style="font-size:11px;color:#0071e3;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;">{category}</span>
<h3 style="font-size:15px;font-weight:600;color:#1d1d1f;margin:4px 0;line-height:1.4;"><a href="{url}" style="color:#1d1d1f;text-decoration:none;">{title}</a></h3>
<p style="font-size:13px;color:#86868b;margin:4px 0;line-height:1.5;">{summary}</p>
<p style="font-size:12px;color:#aeaeb2;margin:4px 0 0;">📰 {source} · ⭐ {score}</p>
</td></tr></table>
</td></tr>""")

    articles_html = "\n".join(articles_html_parts)
    
    trending_text = ", ".join(trending_topics[:8]) if trending_topics else "No trending topics this period"
    
    unsubscribe_html = ""
    if unsubscribe_token:
        unsubscribe_html = f'<a href="{portal_url}/unsubscribe?token={unsubscribe_token}" style="color:#aeaeb2;text-decoration:underline;">Unsubscribe</a>'
    
    return NEWSLETTER_HTML_TEMPLATE.format(
        SUBJECT=subject,
        DATE=date_str,
        HEADLINE=headline,
        SUMMARY_TEXT=summary_text,
        ARTICLES_HTML=articles_html,
        TRENDING_TOPICS=trending_text,
        PORTAL_URL=portal_url,
        UNSUBSCRIBE=unsubscribe_html,
        YEAR=datetime.now().year
    )


def generate_newsletter(
    db: Session,
    user_email: str,
    frequency: str = "weekly",
    categories: List[str] = None
) -> Dict[str, Any]:
    """Generate newsletter content from database articles."""
    from app_ai.database import NewsArticle
    
    query = db.query(NewsArticle).order_by(NewsArticle.score.desc())
    
    if categories:
        query = query.filter(NewsArticle.category.in_(categories))
    
    articles = query.limit(10).all()
    
    articles_data = [{
        "title": a.title,
        "url": a.url,
        "source": a.source,
        "category": a.category,
        "summary": (a.summary or "")[:300],
        "content": (a.content or "")[:500],
        "score": round(a.score, 1)
    } for a in articles]

    # Get trending topics from article titles
    all_text = " ".join([a.get("title", "") for a in articles_data])
    trending = []
    for a in articles_data[:5]:
        title = a.get("title", "")
        if title:
            words = title.split()[:3]
            trending.append(" ".join(words))

    html = generate_newsletter_html(
        articles=articles_data,
        trending_topics=trending,
        frequency=frequency
    )

    return {
        "subject": f"Your {frequency.title()} AI News Digest",
        "html": html,
        "plain_text": "\n\n".join([f"• {a['title']} ({a['source']})" for a in articles_data]),
        "articles_count": len(articles_data)
    }
