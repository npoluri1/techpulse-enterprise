import os, sys, json, time
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="TechPulse Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/npoluri1/techpulse-enterprise",
        "Report a bug": "https://github.com/npoluri1/techpulse-enterprise/issues",
        "About": "TechPulse Enterprise v2.0 — 100% Free & Open Source",
    },
)

from enterprise_engine.config import config
from enterprise_engine.pipeline import EnterprisePipeline
from enterprise_engine.models import init_db, get_session, get_top_articles, get_articles_by_industry, get_alerts, get_pipeline_stats
from enterprise_engine.industry_categories import get_all_industries, INDUSTRY_CATEGORIES

init_db()
pipeline = EnterprisePipeline()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d0d24 50%, #0a0a1a 100%);
        color: #e0e0e0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d24 0%, #12122a 100%);
        border-right: 1px solid #1a1a3e;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #c0c0d0;
    }

    /* Cards */
    .card {
        background: linear-gradient(135deg, #141430 0%, #1a1a38 100%);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 10px 0;
        border: 1px solid #2a2a5a;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
    }
    .card:hover {
        border-color: #00d4aa55;
        box-shadow: 0 4px 30px rgba(0,212,170,0.1);
        transform: translateY(-1px);
    }
    .card-glow {
        background: linear-gradient(135deg, #141430 0%, #1a1a38 100%);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #00d4aa33;
        box-shadow: 0 0 30px rgba(0,212,170,0.05);
    }
    .metric-glow {
        background: linear-gradient(135deg, #141430 0%, #1a1a38 100%);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        border: 1px solid #2a2a5a;
        transition: all 0.2s ease;
    }
    .metric-glow:hover {
        border-color: #00d4aa55;
    }

    /* Alerts */
    .alert-critical { border-left: 4px solid #ff4444; background: linear-gradient(135deg, #1a0a0a 0%, #2a1010 100%); }
    .alert-high { border-left: 4px solid #ff8800; background: linear-gradient(135deg, #1a1408 0%, #2a1c0a 100%); }
    .alert-medium { border-left: 4px solid #ffbb33; background: linear-gradient(135deg, #1a1808 0%, #2a220a 100%); }
    .alert-low { border-left: 4px solid #00d4aa; background: linear-gradient(135deg, #081a14 0%, #0a2a20 100%); }

    /* Chat */
    .chat-bubble {
        background: #141430;
        border-radius: 16px;
        padding: 14px 18px;
        margin: 8px 0;
        border: 1px solid #2a2a5a;
    }
    .chat-bubble.user {
        background: linear-gradient(135deg, #00d4aa15 0%, #00d4aa08 100%);
        border-color: #00d4aa44;
        margin-left: 40px;
    }
    .chat-bubble.assistant {
        margin-right: 40px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(0,212,170,0.3) !important;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background: #141430 !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a2a5a !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00d4aa !important;
        box-shadow: 0 0 0 2px rgba(0,212,170,0.15) !important;
    }
    .stSelectbox > div > div > select {
        background: #141430 !important;
        color: #e0e0e0 !important;
        border-color: #2a2a5a !important;
        border-radius: 10px !important;
    }

    /* Headers */
    h1 { font-size: 2.2rem !important; font-weight: 800 !important;
         background: linear-gradient(135deg, #00d4aa, #00f5c8);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2 { color: #00d4aa !important; font-weight: 700 !important; }
    h3 { color: #00d4aa !important; font-weight: 600 !important; }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #141430;
        border-radius: 14px;
        padding: 16px;
        border: 1px solid #2a2a5a;
    }
    [data-testid="stMetric"] > div {
        color: #00d4aa !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #141430;
        border-radius: 14px;
        padding: 6px;
        border: 1px solid #2a2a5a;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 8px 20px !important;
        color: #888 !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4aa22, #00d4aa11) !important;
        color: #00d4aa !important;
        font-weight: 700 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a1a; }
    ::-webkit-scrollbar-thumb { background: #2a2a5a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3a3a6a; }

    /* Info/Warning/Error boxes */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        background: #141430 !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #141430 !important;
        border-radius: 12px !important;
        border: 1px solid #2a2a5a !important;
    }

    a { color: #00d4aa !important; text-decoration: none !important; }
    a:hover { color: #00f5c8 !important; text-decoration: underline !important; }

    hr { border-color: #2a2a5a !important; }
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pipeline_running" not in st.session_state:
    st.session_state.pipeline_running = False
if "results" not in st.session_state:
    st.session_state.results = None

total_industries = sum(len(v["sub_industries"]) for v in INDUSTRY_CATEGORIES.values())

# === SIDEBAR ===
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 5px 0;">
        <div style="font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #00d4aa, #00f5c8);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px;">
            TechPulse</div>
        <div style="color: #666; font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase; margin-top: -4px;">
            Enterprise Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Run Pipeline", width='stretch'):
            st.session_state.pipeline_running = True
            with st.spinner("Running intelligence pipeline..."):
                result = pipeline.run_full()
                st.session_state.results = result
                st.session_state.pipeline_running = False
            st.rerun()
    with col2:
        if st.button("🔄 Refresh", width='stretch'):
            st.rerun()

    try:
        session = get_session()
        stats = get_pipeline_stats(session)
        session.close()
        st.markdown(f"""
        <div class="metric-glow">
            <div style="font-size: 2rem; font-weight: 800; color: #00d4aa;">{stats['total_articles']}</div>
            <div style="color: #888; font-size: 0.8rem;">Articles Indexed</div>
        </div>
        <div class="metric-glow" style="margin-top: 8px;">
            <div style="font-size: 2rem; font-weight: 800; color: #f0a030;">{stats['total_alerts']}</div>
            <div style="color: #888; font-size: 0.8rem;">Active Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"DB: {e}")

    st.markdown("---")
    st.markdown("### Tech Stack")
    for label, value in [
        ("LLM", "Gemini 2.5 Flash"),
        ("Vector DB", "ChromaDB"),
        ("Embeddings", "MiniLM-L6-v2"),
        ("Database", "SQLite"),
        ("Sources", "NewsAPI + RSS"),
    ]:
        st.markdown(f"**{label}** `{value}`")

    st.markdown("---")
    st.markdown(f"### Industry Coverage")
    st.markdown(f"**{total_industries}** sub-industries across **{len(INDUSTRY_CATEGORIES)}** sectors")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #444; font-size: 0.7rem; padding: 8px 0;">
        Built with Free & Open Source<br>
        <span style="color: #00d4aa;">$0 infrastructure</span>
    </div>
    """, unsafe_allow_html=True)


# === MAIN CONTENT ===
tabs = st.tabs(["📊 Dashboard", "🎯 Insights", "🚨 Alerts", "💬 Chat", "📈 Analytics", "⚙️ Sources"])

# ===================== TAB 1: DASHBOARD =====================
with tabs[0]:
    st.markdown("# Global Intelligence Brief")
    st.markdown(f"<div style='color: #888; margin-top: -10px;'>Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>", unsafe_allow_html=True)

    if st.session_state.results:
        r = st.session_state.results
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Articles Fetched", r.get("fetched", 0))
        c2.metric("Curated & Scored", r.get("curated", 0))
        c3.metric("Alerts Generated", r.get("alerts", 0))
        c4.metric("Pipeline Status", r.get("status", "—").title())

        if r.get("markdown_report"):
            with st.expander("Executive Report", expanded=True):
                st.markdown(f'<div class="card-glow">{r.get("markdown_report", "")}</div>', unsafe_allow_html=True)

        if r.get("mobile_brief"):
            st.markdown("### Mobile Brief")
            st.info(r.get("mobile_brief"))
    else:
        st.warning("Click **▶ Run Pipeline** in the sidebar to start the intelligence engine.")

    st.markdown("---")

    try:
        session = get_session()
        articles = get_top_articles(session, limit=15)
        session.close()
        if articles:
            st.markdown("### Top Articles by Relevance")
            for a in articles[:8]:
                score = a.final_score or 0
                color = "#00d4aa" if score >= 75 else "#f0a030" if score >= 50 else "#666"
                bar_pct = min(score, 100)
                tags = ", ".join(a.industry_tags[:3]) if a.industry_tags else "General"
                st.markdown(f"""
                <div class="card" style="padding: 14px 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: start; gap: 12px;">
                        <div style="flex: 1; min-width: 0;">
                            <a href="{a.url}" target="_blank" style="font-weight: 600; font-size: 1.05rem;">{a.title}</a>
                            <div style="color: #888; font-size: 0.8rem; margin-top: 6px;">
                                {a.source}  ·  {tags}
                            </div>
                            <div style="margin-top: 8px; height: 4px; background: #2a2a5a; border-radius: 2px; max-width: 300px;">
                                <div style="height: 100%; width: {bar_pct}%; background: {color}; border-radius: 2px;"></div>
                            </div>
                        </div>
                        <div style="text-align: center; min-width: 50px;">
                            <div style="font-size: 1.4rem; font-weight: 800; color: {color};">{score:.0f}</div>
                            <div style="color: #555; font-size: 0.65rem; letter-spacing: 1px;">SCORE</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No articles indexed yet. Run the pipeline first.")
    except Exception as e:
        st.error(f"Error loading articles: {e}")


# ===================== TAB 2: INSIGHTS =====================
with tabs[1]:
    st.markdown("# Industry Intelligence")

    industries = get_all_industries()
    sector_names = sorted(set(i["sector"] for i in industries))

    c1, c2 = st.columns([1, 2])
    with c1:
        selected_sector = st.selectbox("Sector", ["All"] + sector_names)
    with c2:
        filtered = [i for i in industries if selected_sector == "All" or i["sector"] == selected_sector]
        selected_industry = st.selectbox("Industry", sorted(set(i["industry"] for i in filtered)))

    if st.button("Search Industry", width='stretch'):
        with st.spinner(f"Searching {selected_industry}..."):
            from enterprise_engine.vector_store import FreeVectorStore
            vs = FreeVectorStore()
            results = vs.search_by_industry(selected_industry, k=10)
            if not results:
                session = get_session()
                db_results = get_articles_by_industry(session, selected_industry)
                session.close()
                results = [
                    {"title": a.title, "url": a.url, "source": a.source, "final_score": a.final_score or 0}
                    for a in db_results
                ]
            if results:
                st.markdown(f"**{len(results)}** articles found for '{selected_industry}'")
                for r in results:
                    st.markdown(f"""
                    <div class="card" style="padding: 12px 16px;">
                        <a href="{r.get('url', '#')}" target="_blank" style="font-weight: 600;">{r.get('title', '')}</a>
                        <div style="color: #888; font-size: 0.8rem; margin-top: 4px;">{r.get('source', '')} · Score: {r.get('final_score', 0):.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No articles for this industry yet.")

    st.markdown("---")
    st.markdown("### Sector Coverage")

    sector_counts = {}
    for i in industries:
        s = i["sector"]
        sector_counts[s] = sector_counts.get(s, 0) + 1
    df = pd.DataFrame([{"Sector": s.replace("_", " ").title(), "Sub-Industries": c} for s, c in sector_counts.items()])

    fig = px.bar(df.sort_values("Sub-Industries", ascending=True),
                 x="Sub-Industries", y="Sector", orientation="h",
                 title=f"Industries per Sector ({total_industries} total)",
                 color="Sub-Industries", color_continuous_scale="tealgrn",
                 text="Sub-Industries")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#c0c0d0", height=500, margin=dict(l=0, r=0, t=40, b=0))
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, width='stretch')


# ===================== TAB 3: ALERTS =====================
with tabs[2]:
    st.markdown("# Real-Time Alerts & Notifications")

    try:
        session = get_session()
        alerts = get_alerts(session, limit=50)
        session.close()
        if alerts:
            for a in alerts[:20]:
                sev = a.severity or 5
                if sev >= 9:
                    cls, icon, label = "alert-critical", "🔴", "CRITICAL"
                elif sev >= 7:
                    cls, icon, label = "alert-high", "🟠", "HIGH"
                elif sev >= 5:
                    cls, icon, label = "alert-medium", "🟡", "MEDIUM"
                else:
                    cls, icon, label = "alert-low", "🟢", "LOW"
                st.markdown(f"""
                <div class="card {cls}" style="padding: 14px 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <span style="font-size: 0.7rem; font-weight: 700; color: #888; letter-spacing: 1px;">{label}</span>
                            <div style="font-weight: 600; margin-top: 4px;">{a.headline}</div>
                            <div style="color: #888; font-size: 0.85rem; margin-top: 6px;">{a.body}</div>
                        </div>
                        <div style="text-align: center; min-width: 50px;">
                            <div style="font-size: 1.5rem; font-weight: 800;">{sev}</div>
                            <div style="color: #555; font-size: 0.65rem;">SEVERITY</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No alerts generated yet. Run the pipeline to detect breaking news.")
    except Exception as e:
        st.error(f"Error loading alerts: {e}")


# ===================== TAB 4: CHAT =====================
with tabs[3]:
    st.markdown("# AI Intelligence Chat")
    st.markdown("*Ask questions about the latest technology news and trends. Uses Gemini AI with RAG context.*")

    for msg in st.session_state.chat_history:
        role = msg["role"]
        st.markdown(f'<div class="chat-bubble {role}"><strong>{"You" if role == "user" else "🧠 AI"}:</strong><br>{msg["content"]}</div>',
                   unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        question = st.text_input("Ask about AI, quantum, robotics, investments...",
                                 placeholder="What are the latest breakthroughs in AI?",
                                 label_visibility="collapsed")
    with c2:
        chat_industry = st.selectbox("Industry filter",
                                     ["All"] + sorted(set(i["industry"] for i in get_all_industries())),
                                     label_visibility="collapsed")

    if question and st.button("Send", width='stretch'):
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("Analyzing..."):
            result = pipeline.rag.ask(
                question=question,
                industry=None if chat_industry == "All" else chat_industry,
            )
            answer = result.get("answer", "No answer available.")
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            if result.get("sources"):
                sources = "\n".join(f"- [{s['title']}]({s['url']})" for s in result["sources"][:3])
                st.session_state.chat_history.append({"role": "assistant", "content": f"**Sources:**\n{sources}"})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear Chat", width='stretch'):
            st.session_state.chat_history = []
            st.rerun()


# ===================== TAB 5: ANALYTICS =====================
with tabs[4]:
    st.markdown("# Visual Analytics")

    try:
        session = get_session()
        articles = get_top_articles(session, limit=200)
        session.close()
        if articles:
            rows = []
            for a in articles:
                tags = a.industry_tags or ["General"]
                for tag in tags[:2]:
                    rows.append({
                        "Industry": tag, "Score": a.final_score or 0,
                        "Source": a.source or "Unknown", "Funding": a.funding_amount_usd or 0,
                    })
            df = pd.DataFrame(rows)

            c1, c2 = st.columns(2)
            with c1:
                top_ind = df.groupby("Industry")["Score"].mean().sort_values(ascending=False).head(12)
                fig = px.bar(top_ind, title="Top Industries by Relevance",
                            color=top_ind.values, color_continuous_scale="tealgrn",
                            text_auto=".0f")
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                 plot_bgcolor="rgba(0,0,0,0)", font_color="#c0c0d0",
                                 height=350, margin=dict(l=0, r=0, t=40, b=0), showlegend=False)
                st.plotly_chart(fig, width='stretch')

            with c2:
                src = df["Source"].value_counts().head(8)
                fig = px.pie(values=src.values, names=src.index, title="Articles by Source",
                            color_discrete_sequence=px.colors.sequential.Tealgrn)
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                 font_color="#c0c0d0", height=350, margin=dict(l=0, r=0, t=40, b=0),
                                 showlegend=True, legend=dict(orientation="h", y=-0.2))
                st.plotly_chart(fig, width='stretch')

            sc = df["Score"].value_counts().sort_index().reset_index()
            sc.columns = ["Score", "Count"]
            fig = px.area(sc, x="Score", y="Count", title="Score Distribution",
                         color_discrete_sequence=["#00d4aa"])
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", font_color="#c0c0d0",
                            height=300, margin=dict(l=0, r=0, t=40, b=0), showlegend=False)
            fig.update_traces(fillcolor="rgba(0,212,170,0.15)")
            st.plotly_chart(fig, width='stretch')

            funding = df[df["Funding"] > 0].drop_duplicates(subset=["Industry"])
            if not funding.empty and len(funding) > 1:
                fig = px.treemap(funding, path=["Industry"], values="Funding",
                                title="Investment Distribution",
                                color="Funding", color_continuous_scale="tealgrn")
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                 font_color="#c0c0d0", height=400, margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig, width='stretch')
        else:
            st.info("Run the pipeline first to generate analytics.")
    except Exception as e:
        st.error(f"Chart error: {e}")


# ===================== TAB 6: SOURCES =====================
with tabs[5]:
    st.markdown("# Configuration & Sources")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Data Sources")
        st.markdown("**RSS Feeds** — 24 active")
        for feed in config.RSS_FEEDS:
            st.markdown(f"- {feed}")
    with c2:
        st.markdown("### API Queries")
        st.markdown("**NewsAPI** — 22 queries")
        for q in config.NEWSAPI_QUERIES:
            st.markdown(f"- `{q}`")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### LLM Config")
        st.json({
            "model": config.LLM_MODEL,
            "temperature": config.LLM_TEMPERATURE,
            "max_tokens": config.LLM_MAX_TOKENS,
            "gemini": bool(config.GEMINI_API_KEY),
        })
    with c2:
        st.markdown("### Tech Stack")
        st.json({
            "Vector DB": "ChromaDB",
            "Embeddings": "all-MiniLM-L6-v2",
            "Database": "SQLite",
            "LLM": "Gemini 2.5 Flash",
            "Frontend": "Streamlit",
        })
    with c3:
        st.markdown("### Free Limits")
        st.json({
            "Gemini API": "5 RPM / 20 RPD",
            "NewsAPI": "100 req/day",
            "Serper.dev": "2500/month",
            "ChromaDB": "Unlimited (local)",
            "SQLite": "Unlimited (local)",
        })

    st.markdown("---")
    st.markdown("### Deploy for Free")
    st.info("""
    1. Push code to GitHub  
    2. Go to [share.streamlit.io](https://share.streamlit.io)  
    3. Connect repo, set `enterprise_engine/streamlit_app.py` as entry point  
    4. Add API keys in Streamlit Secrets → `GEMINI_API_KEY`, `NEWSAPI_KEY`  
    5. Deploy — 0$ infrastructure, fully managed
    """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #444; font-size: 0.75rem; padding: 16px 0;">
    TechPulse Enterprise v2.0  ·  100% Free & Open Source  ·  ChromaDB + Gemini + Streamlit + SQLite + HuggingFace<br>
    <span style="color: #00d4aa;">Zero infrastructure cost — deploy on Streamlit Community Cloud for free</span>
</div>
""", unsafe_allow_html=True)
