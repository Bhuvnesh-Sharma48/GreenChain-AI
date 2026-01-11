import os
import requests
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# -----------------------
# Config
# -----------------------
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(
    page_title="GreenChain AI",
    page_icon="📦",
    layout="wide",
)

# -----------------------
# Session State Defaults
# -----------------------
if "loading" not in st.session_state:
    st.session_state["loading"] = False
if "result" not in st.session_state:
    st.session_state["result"] = None
if "last_error" not in st.session_state:
    st.session_state["last_error"] = None
if "trigger_run" not in st.session_state:
    st.session_state["trigger_run"] = False

# -----------------------
# Force Dark Theme + Green Accent (Cloud-safe)
# -----------------------
st.markdown(
    """
    <style>
    :root {
        --primary: #2ecc71;
        --bg: #070c17;
        --sidebar: #0f1a2e;
        --text: #e8eef7;
        --muted: rgba(232,238,247,0.75);
        --border: rgba(255,255,255,0.10);
        --card: rgba(255,255,255,0.05);
    }

    /* Force base theme */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background: var(--sidebar) !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* Remove default white blocks */
    .block-container { background: transparent !important; }

    /* Header transparent */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }

    /* Ensure ALL widget labels are light */
    label, .stMarkdown, .stText, .stCaption {
        color: var(--text) !important;
    }

    /* Inputs */
    input, textarea {
        background-color: var(--sidebar) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
    }

    /* ✅ Selectbox / dropdown */
    div[data-baseweb="select"] > div {
        background-color: var(--sidebar) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 12px !important;
    }

    /* Dropdown list */
    ul[role="listbox"] {
        background-color: #0b1426 !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }
    li[role="option"] {
        color: var(--text) !important;
    }
    li[role="option"]:hover {
        background: rgba(46,204,113,0.15) !important;
    }

    /* ✅ Number input stepper (+/-) */
    div[data-testid="stNumberInput"] button {
        background: #0b1426 !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stNumberInput"] button:hover {
        background: rgba(46,204,113,0.18) !important;
        border-color: rgba(46,204,113,0.35) !important;
    }

    /* ============================================================
       ✅✅✅ Global Accent Fix
       Streamlit adds some orange accents via CSS variables.
       We override those to green.
       ============================================================ */
    :root {
        --accent: var(--primary) !important;
        --primary-color: var(--primary) !important;
    }

    /* Force focus outline / active border green */
    *:focus, *:focus-visible {
        outline-color: var(--primary) !important;
        border-color: var(--primary) !important;
    }

    /* ============================================================
       ✅✅✅ Slider Fix (works on Streamlit Cloud + localhost)
       ============================================================ */

    /* Filled track */
    div[data-testid="stSlider"] [data-baseweb="slider"] div div div div {
        background-color: var(--primary) !important;
    }

    /* Unfilled track */
    div[data-testid="stSlider"] [data-baseweb="slider"] div div div {
        background-color: rgba(255,255,255,0.25) !important;
    }

    /* Thumb */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: var(--primary) !important;
        border: 2px solid var(--primary) !important;
        box-shadow: 0 0 0 4px rgba(46,204,113,0.25) !important;
    }

    /* Remove tooltip background bubble in cloud */
    div[data-testid="stSlider"] [data-baseweb="tooltip"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    /* Slider number text */
    div[data-testid="stSlider"] [data-baseweb="tooltip"] * {
        color: var(--primary) !important;
        background: transparent !important;
        font-weight: 900 !important;
    }

    /* Remove tooltip arrow */
    div[data-testid="stSlider"] [data-baseweb="tooltip"] svg {
        display: none !important;
    }

    /* Extra fallback for Streamlit builds */
    div[data-testid="stSlider"] div[aria-valuenow] {
        color: var(--primary) !important;
        font-weight: 900 !important;
        background: transparent !important;
    }

    /* ✅ Tabs styling */
    button[data-baseweb="tab"] {
        background: rgba(46, 204, 113, 0.12) !important;
        color: var(--text) !important;
        border-radius: 999px !important;
        border: 1px solid rgba(46, 204, 113, 0.22) !important;
        padding: 0.2rem 0.8rem !important;
    }

    /* ✅ ALL Buttons forced green */
    .stButton > button,
    button[kind="primary"],
    button[kind="secondary"] {
        background: var(--primary) !important;
        border: none !important;
        color: #00140a !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    }

    /* ✅ Download button (Streamlit adds different DOM) */
    div[data-testid="stDownloadButton"] button {
        background: var(--primary) !important;
        color: #00140a !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
    }

    /* Fix hover */
    .stButton > button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        filter: brightness(1.05);
    }

    </style>
    """,
    unsafe_allow_html=True
)

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

# -----------------------
# Styling (Dark glass UI)
# -----------------------
def load_css():
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.4rem; padding-bottom: 2rem; }

        .section-title { font-size: 1.35rem; font-weight: 900; margin-top: 0.85rem; margin-bottom: 0.35rem; }
        .muted { color: rgba(229,231,235,0.75); }

        .card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 12px 40px rgba(0,0,0,0.35);
            backdrop-filter: blur(8px);
        }

        .divider { height: 1px; background: rgba(255,255,255,0.08); margin: 1.05rem 0; }

        .metric-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 0.85rem 1rem;
            box-shadow: 0 12px 40px rgba(0,0,0,0.35);
            backdrop-filter: blur(8px);
        }
        .metric-label { color: rgba(229,231,235,0.75); font-size: 0.88rem; font-weight: 600; }
        .metric-value { font-size: 1.55rem; font-weight: 900; margin-top: 0.1rem; }

        .banner-wrap img {
            border-radius: 18px !important;
            max-height: 240px;
            object-fit: cover;
        }

        .sidebar-logo img {
            width: 100% !important;
            max-width: 170px;
            border-radius: 14px !important;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

load_css()

# -----------------------
# Image helper
# -----------------------
def img_if_exists(base_name: str, *, width: int | None = None, full: bool = False):
    for ext in ["png", "jpg", "jpeg", "webp"]:
        path = ASSETS_DIR / f"{base_name}.{ext}"
        if path.exists():
            if full:
                st.image(str(path), use_container_width=True)
            else:
                st.image(str(path), width=width)
            return True
    return False

# -----------------------
# Render helpers
# -----------------------
def render_bullets(items):
    if not items:
        st.write("—")
        return
    for x in items:
        st.write(f"- {x}")

def metric_box(label: str, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_risk_report(risk_report: dict):
    top_risks = risk_report.get("top_risks", [])
    mitigations = risk_report.get("mitigation_plan", [])
    quick_wins = risk_report.get("quick_wins_2_weeks", [])
    notes = risk_report.get("notes", "")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Top Risks")
    if not top_risks:
        st.info("No risk items returned.")
    else:
        for i, r in enumerate(top_risks, start=1):
            risk = r.get("risk", "—")
            sev = r.get("severity_1_to_5", "—")
            prob = r.get("probability_1_to_5", "—")
            impact = r.get("impact", "—")
            st.markdown(
                f"""
**{i}. {risk}**  
- Severity: **{sev}/5**  
- Probability: **{prob}/5**  
- Business impact: {impact}
"""
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Mitigation Plan")
        render_bullets(mitigations)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Quick Wins (≤ 2 weeks)")
        render_bullets(quick_wins)
        st.markdown("</div>", unsafe_allow_html=True)

    if notes:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Notes")
        st.write(notes)
        st.markdown("</div>", unsafe_allow_html=True)

def render_efficiency_plan(eff: dict):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Transport Efficiency")
    for item in eff.get("transport_efficiency", []):
        st.markdown(
            f"- **{item.get('action','—')}**  \n"
            f"  Benefit: {item.get('business_benefit','—')}  \n"
            f"  Effort: **{item.get('effort','—')}**"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Packaging & Damage Reduction")
    for item in eff.get("packaging_damage_reduction", []):
        st.markdown(
            f"- **{item.get('action','—')}**  \n"
            f"  Benefit: {item.get('business_benefit','—')}  \n"
            f"  Effort: **{item.get('effort','—')}**"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Inventory & Waste Reduction")
    for item in eff.get("inventory_waste_reduction", []):
        st.markdown(
            f"- **{item.get('action','—')}**  \n"
            f"  Benefit: {item.get('business_benefit','—')}  \n"
            f"  Effort: **{item.get('effort','—')}**"
        )
    st.markdown("</div>", unsafe_allow_html=True)

def render_action_plan(plan: dict):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Executive Summary")
    render_bullets(plan.get("executive_summary", []))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("30-Day Plan")
        tasks_30 = plan.get("plan_30_days", [])
        if tasks_30:
            for i, t in enumerate(tasks_30, start=1):
                st.markdown(
                    f"**{i}. {t.get('task','—')}**  \n"
                    f"Owner: **{t.get('owner','—')}**  \n"
                    f"Expected result: {t.get('expected_result','—')}"
                )
        else:
            st.write("—")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("90-Day Plan")
        tasks_90 = plan.get("plan_90_days", [])
        if tasks_90:
            for i, t in enumerate(tasks_90, start=1):
                st.markdown(
                    f"**{i}. {t.get('task','—')}**  \n"
                    f"Owner: **{t.get('owner','—')}**  \n"
                    f"Expected result: {t.get('expected_result','—')}"
                )
        else:
            st.write("—")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("KPIs")
    kpis = plan.get("kpis", [])
    if kpis:
        for k in kpis:
            st.markdown(f"- **{k.get('kpi','—')}** — Target: {k.get('target','—')}")
    else:
        st.write("—")
    st.markdown("</div>", unsafe_allow_html=True)

def format_report_text(data: dict) -> str:
    inv = data.get("inventory_strategy", {})
    risk = data.get("risk_report", {})
    eff = data.get("efficiency_plan", {})
    plan = data.get("action_plan", {})
    dis = data.get("disruption_signals", {})

    lines = []
    lines.append("GREENCHAIN AI — SUPPLY CHAIN REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("== Inventory Strategy ==")
    lines.append(f"EOQ: {inv.get('eoq_units')}")
    lines.append(f"Reorder Point: {inv.get('reorder_point_units')}")
    lines.append(f"Safety Stock: {inv.get('safety_stock_units')}")
    lines.append("")
    lines.append("Interpretation:")
    for x in inv.get("interpretation", []):
        lines.append(f"- {x}")

    lines.append("")
    lines.append("== Disruption Signals (Tavily) ==")
    lines.append(dis.get("answer_summary", "") or "—")
    return "\n".join(lines)

# -----------------------
# Backend call
# -----------------------
def call_backend(payload: dict) -> dict:
    res = requests.post(f"{BACKEND_URL}/analyze_supply_chain", json=payload, timeout=240)
    if res.status_code != 200:
        raise RuntimeError(f"Backend error {res.status_code}: {res.text}")
    return res.json()

# -----------------------
# Sidebar
# -----------------------
with st.sidebar:
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    img_if_exists("logo")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## GreenChain AI")
    st.caption("Supply Chain Decision Copilot")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.header("Supply Chain Inputs")
    product = st.text_input("Product", value="Rice")
    origin = st.text_input("Origin", value="Jaipur, India")
    destination = st.text_input("Destination", value="Dubai, UAE")

    monthly_demand = st.number_input("Monthly demand (units)", min_value=1, value=5000)
    priority = st.selectbox("Priority", ["low_cost", "fast_delivery", "sustainability"], index=0)

    st.subheader("Advanced (Optional)")
    lead_time_days = st.slider("Lead time (days)", 1, 60, 14)
    holding_cost = st.number_input("Holding cost per unit / year", min_value=1.0, value=20.0)
    ordering_cost = st.number_input("Ordering cost per order", min_value=1.0, value=200.0)

    service_level = st.slider("Service level", min_value=0.50, max_value=0.99, value=0.95, step=0.01)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    run_btn = st.button(
        "Generate Plan",
        type="primary",
        key="generate_plan_btn",
        disabled=st.session_state["loading"],
    )

    if run_btn and not st.session_state["loading"]:
        st.session_state["trigger_run"] = True

# -----------------------
# Banner
# -----------------------
st.markdown('<div class="banner-wrap">', unsafe_allow_html=True)
img_if_exists("banner", full=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# -----------------------
# Trigger backend call
# -----------------------
if st.session_state["trigger_run"] and not st.session_state["loading"]:
    st.session_state["trigger_run"] = False
    st.session_state["loading"] = True
    st.session_state["last_error"] = None
    st.session_state["result"] = None

    payload = {
        "product": product,
        "origin": origin,
        "destination": destination,
        "monthly_demand": int(monthly_demand),
        "lead_time_days": int(lead_time_days),
        "holding_cost_per_unit_year": float(holding_cost),
        "ordering_cost": float(ordering_cost),
        "service_level": float(service_level),
        "priority": priority,
    }

    try:
        with st.spinner("Running agentic analysis (Gemini + Tavily)..."):
            data = call_backend(payload)
        st.session_state["result"] = data
    except Exception as e:
        st.session_state["last_error"] = str(e)
    finally:
        st.session_state["loading"] = False
        st.rerun()

# -----------------------
# Main render
# -----------------------
if st.session_state["last_error"]:
    st.error(st.session_state["last_error"])

data = st.session_state["result"]

if data:
    st.success("✅ Analysis completed successfully. (Theme is now fully green!)")
else:
    st.markdown(
        '<div class="card"><b>How to use:</b><br>'
        'Fill inputs in the sidebar and click <b>Generate Plan</b> to run the multi-agent analysis.</div>',
        unsafe_allow_html=True,
    )
