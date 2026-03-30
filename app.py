"""
PharmGTN Pro v3 — Dynamic Multi-Year Gross-to-Net Analyzer
• 5–10 year forecast with editable annual volumes & WAC
• Per-year rebates, discounts, and channel allocation
• ASP = 6-month rolling weighted average of non-exempt channel selling prices
• Full GTN waterfall + Buy & Bill / ASP spread analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ───────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PharmGTN Pro v4",
    layout="wide",
    page_icon="⚕️",
    initial_sidebar_state="expanded",
)
# ───────────────────────────────────────────────────────────────────
# CSS
# ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* ===== GOOGLE FONTS ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ===== GLOBAL BACKGROUND ===== */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #F8FAFD !important;
    color: #1A1A2E !important;
    font-family: 'Inter', sans-serif;
}

/* ===== PRESENTATION MODE OVERRIDES ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {display: none;}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F0F5FB 100%) !important;
    border-right: 1px solid #E2E8F0;
    box-shadow: 2px 0 12px rgba(31, 78, 121, 0.04);
}
[data-testid="stSidebar"] * {
    color: #2D3748 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1f4e79 !important;
    letter-spacing: -0.3px;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="popover"],
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D6E8F7 !important;
    border-radius: 8px !important;
    color: #1A1A2E !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="control"],
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="ValueContainer"],
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="singleValue"],
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="indicatorContainer"],
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    background-color: #FFFFFF !important;
    color: #1A1A2E !important;
    fill: #4A5568 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] [role="listbox"],
[data-testid="stSidebar"] [data-baseweb="select"] ul,
[data-testid="stSidebar"] [data-baseweb="select"] li {
    background-color: #FFFFFF !important;
    color: #1A1A2E !important;
}
[data-testid="stSidebar"] .stTextInput > div > div,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background-color: #FFFFFF !important;
    color: #1A1A2E !important;
}
[data-testid="stSidebar"] input:focus,
[data-testid="stSidebar"] [data-baseweb="select"]:focus-within {
    border-color: #4a90d9 !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.12) !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #4A5568 !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stSidebar"] hr {
    border-color: #E2E8F0 !important;
    opacity: 0.6;
}
[data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] small {
    color: #718096 !important;
}

/* ===== CUSTOM TOP BANNER (ONLY BLUE AREA) ===== */
.top-banner {
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 40%, #63b3ed 100%);
    color: #ffffff;
    padding: 16px 24px;
    font-size: 20px;
    font-weight: 700;
    border-radius: 12px;
    margin-bottom: 16px;
    border: none;
    box-shadow: 0 4px 16px rgba(26, 54, 93, 0.15);
    letter-spacing: -0.3px;
}

/* ===== TEXT ===== */
h1, h2, h3 {
    color: #1a365d !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}
h2 {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}

/* ===== SECTION HEADERS ===== */
.sec-header {
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 50%, #3182ce 100%);
    color: white !important;
    border-radius: 10px;
    padding: 12px 18px;
    margin: 14px 0;
    font-weight: 800;
    font-size: 1.15rem;
    letter-spacing: 0.2px;
    box-shadow: 0 4px 14px rgba(26, 54, 93, 0.18);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.sec-header:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(26, 54, 93, 0.22);
}

p, span, label {
    color: #4A5568 !important;
    line-height: 1.6;
    font-size: 1.05rem;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #F0F8FF 0%, #E8F2FC 100%);
    border: 1px solid #D0E3F5;
    padding: 18px 16px;
    border-radius: 12px;
    overflow: visible;
    box-shadow: 0 2px 8px rgba(31, 78, 121, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(31, 78, 121, 0.12);
}
[data-testid="stMetric"] label {
    white-space: nowrap !important;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-weight: 700 !important;
    color: #4A5568 !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    white-space: nowrap !important;
    overflow: visible !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: #1a365d !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ===== BUTTONS ===== */
.stButton>button {
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(26, 54, 93, 0.2);
    transition: all 0.2s ease;
}
.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(26, 54, 93, 0.3);
    background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 700;
    font-size: 0.95rem;
    color: #4A5568 !important;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: #F0F5FB;
    color: #1a365d !important;
}
.stTabs [aria-selected="true"] {
    background-color: #EBF4FF !important;
    color: #1a365d !important;
    border-bottom: 2px solid #2b6cb0 !important;
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* ===== NUMBER INPUTS ===== */
.stNumberInput input {
    background-color: #FFFFFF !important;
    border: 1px solid #D6E8F7 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease;
}
.stNumberInput input:focus {
    border-color: #4a90d9 !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.12) !important;
}

/* ===== SELECTBOX ===== */
.stSelectbox [data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
}

/* ===== INFO BOX ===== */
.info-box {
    background: linear-gradient(135deg, #EBF8FF 0%, #F0F5FB 100%);
    border: 1px solid #BEE3F8;
    border-left: 4px solid #3182ce;
    border-radius: 8px;
    padding: 16px 22px;
    margin: 12px 0;
    font-size: 1rem;
    color: #2D3748 !important;
}

/* ===== YEAR LABEL ===== */
.yr-label {
    background: #EBF4FF;
    border: 1px solid #D0E3F5;
    border-radius: 8px;
    padding: 8px 12px;
    font-weight: 700;
    color: #1a365d;
    text-align: center;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

/* ===== MULTISELECT (Channel Filter) ===== */
[data-testid="stMultiselect"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D6E8F7 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    color: #1A1A2E !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stMultiselect"]:focus-within {
    border-color: #4a90d9 !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.12) !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #1A1A2E !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] div[class*="control"] {
    background-color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    min-height: 40px !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] div[class*="ValueContainer"] {
    color: #1A1A2E !important;
    font-size: 0.9rem !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] div[class*="multiValue"],
[data-testid="stMultiselect"] [data-baseweb="select"] [class*="multiValue"],
[class*="multiValue"] {
    background-color: #A8D5FF !important;
    background-image: linear-gradient(135deg, #A8D5FF 0%, #D4EAFF 100%) !important;
    border: 1px solid #2b6cb0 !important;
    color: #1a365d !important;
    border-radius: 6px !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] div[class*="multiValue"] span,
[data-testid="stMultiselect"] [data-baseweb="select"] div[class*="multiValue"] span span,
[class*="multiValue"] span,
[class*="multiValue"] span span {
    color: #1a365d !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] div[class*="multiValue"] [role="button"] svg,
[class*="multiValue"] [role="button"] svg {
    fill: #1a365d !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] div[class*="control"] {
    background-color: #F8FAFD !important;
    border: 1px solid #D6E8F7 !important;
    color: #1A1A2E !important;
    min-height: 42px !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] {
    background-color: #F8FAFD !important;
    border: 1px solid #D6E8F7 !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] [role="listbox"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D6E8F7 !important;
    color: #1A1A2E !important;
}

[data-testid="stMultiselect"] [data-baseweb="select"] [role="listbox"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] li {
    color: #1A1A2E !important;
    font-size: 0.9rem !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] li:hover {
    background-color: #F0F5FB !important;
}
[data-testid="stMultiselect"] [data-baseweb="select"] svg {
    fill: #4A5568 !important;
}
[data-testid="stMultiselect"] label {
    color: #4A5568 !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: none !important;  /* Remove uppercase */
    letter-spacing: 0.3px !important;
}

/* ===== PLOTLY FIX ===== */
.js-plotly-plot {
    background-color: #FFFFFF !important;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* ===== HORIZONTAL RULES ===== */
hr {
    border: none !important;
    border-top: 1px solid #E2E8F0 !important;
    margin: 16px 0 !important;
}
            /* ===== MULTISELECT CONTAINER ===== */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D0E3F5 !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #4a90d9 !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.12) !important;
}
            /* ===== MULTISELECT ICONS ===== */
[data-baseweb="select"] svg {
    fill: #1a365d !important;
}
[data-baseweb="select"] svg:hover {
    fill: #2b6cb0 !important;
}
/* ===== MULTISELECT TAGS ===== */
[data-baseweb="tag"] {
    background-color: #EBF4FF !important;
    border: 1px solid #2b6cb0 !important;
    border-radius: 6px !important;
}
[data-baseweb="tag"] span {
    color: #1a365d !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-baseweb="tag"] [role="presentation"] svg {
    fill: #2b6cb0 !important;
}
[data-baseweb="tag"] [role="presentation"]:hover svg {
    fill: #1a365d !important;
}
/* Multiselect dropdown container */
[data-baseweb="select"] [data-baseweb="popover"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D0E3F5 !important;
    border-radius: 8px !important;
}
/* Multiselect option hover */
[data-baseweb="menu"] [role="option"]:hover {
    background-color: #EBF4FF !important;
}
/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #F0F5FB;
}
::-webkit-scrollbar-thumb {
    background: #B8CBE0;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #8FA8C8;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background-color: #F7FAFC !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: #2D3748 !important;
}

</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────────
# HELPERS
# ───────────────────────────────────────────────────────────────────
CHANNELS = [
    "Commercial PBM",
    "Commercial Medical",
    "Medicare Part B",
    "Medicare Part D",
    "Medicaid FFS",
    "Managed Medicaid",
    "GPO/IDN Non-340B",
    "GPO/IDN 340B",
    "VA/DoD/Federal",
    "Cash/Uninsured",
]

# ASP-eligible channels and exempt
ASP_ELIGIBLE = {
    "Commercial PBM": True,
    "Commercial Medical": True,
    "Medicare Part B": True,
    "Medicare Part D": True,
    "Medicaid FFS": False,      # Exempt
    "Managed Medicaid": False,  # Exempt
    "GPO/IDN Non-340B": True,
    "GPO/IDN 340B": False,      # Exempt (340B ceiling = exempt)
    "VA/DoD/Federal": False,    # Exempt (Big4 exempt)
    "Cash/Uninsured": True,
}

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

BASE_YEAR = 2025

def fmt_m(v): return f"${v/1e6:.2f}M"
def fmt_b(v): return f"${v/1e9:.3f}B"
def fmt_pct(v): return f"{v:.1f}%"
def fmt_u(v): return f"{v:,.0f}"
def fmt_d(v): return f"${v:,.2f}"

MONTH_PROFILES = {
    "Flat": [1/12]*12,
    "S-Curve (Launch)": [0.03,0.04,0.05,0.07,0.09,0.10,0.10,0.10,0.10,0.10,0.11,0.11],
    "Back-Loaded": [0.04,0.05,0.06,0.07,0.08,0.08,0.09,0.09,0.10,0.10,0.11,0.13],
    "Front-Loaded": [0.13,0.12,0.11,0.10,0.10,0.09,0.08,0.08,0.07,0.05,0.04,0.03],
}

def get_monthly_weights(profile_name, n_years, raw_weights):
    """Return month weights normalized for each year (list of 12-item lists)."""
    if profile_name == "Custom":
        w = raw_weights if raw_weights else [1/12]*12
    else:
        w = MONTH_PROFILES[profile_name]
    s = sum(w)
    return [x/s for x in w]

def expand_to_monthly(forecast_df, weights_12):
    """Expand annual forecast rows to monthly rows."""
    rows = []
    for _, row in forecast_df.iterrows():
        yr = row["Year"]
        for m_idx, mo in enumerate(MONTHS):
            rows.append({
                "Year": yr, "Month": mo, "MonthIdx": m_idx+1,
                "Period": f"{yr}-{mo}",
                "Units": row["Annual Units"] * weights_12[m_idx],
                "WAC": row["WAC per Unit"],
            })
    return pd.DataFrame(rows)

def compute_asp_series(monthly_df, channel_alloc_by_year, discount_by_year):
    """
    Compute monthly ASP as 6-month rolling weighted average of non-exempt selling prices.
    ASP = Σ(price_i × units_i) / Σ(units_i) for eligible channels, 6-month rolling.
    """
    records = []
    for _, row in monthly_df.iterrows():
        yr = row["Year"]
        wac = row["WAC"]
        alloc = channel_alloc_by_year.get(yr, channel_alloc_by_year[min(channel_alloc_by_year.keys())])
        disc  = discount_by_year.get(yr, discount_by_year[min(discount_by_year.keys())])

        gpo_p   = wac * (1 - disc["gpo"] / 100)
        idn_p   = wac * (1 - disc["idn"] / 100)
        va_p    = wac * (1 - disc["va"]  / 100)
        b340_p  = wac * (1 - disc["b340"] / 100)

        # Selling price per channel (what manufacturer actually invoices before rebates)
        ch_prices = {
            "Commercial PBM":    wac,            # WAC invoiced; rebates are post-sale, excluded from ASP
            "Commercial Medical": gpo_p,          # GPO/contract price
            "Medicare Part B":   gpo_p,           # GPO price to provider/wholesaler
            "Medicare Part D":   wac,             # WAC (rebates post-sale, excluded)
            "Medicaid FFS":      wac,             # Excluded from ASP
            "Managed Medicaid":  wac,             # Excluded from ASP
            "GPO/IDN Non-340B":  idn_p,           # IDN contract price
            "GPO/IDN 340B":      b340_p,          # Excluded from ASP
            "VA/DoD/Federal":    va_p,            # Excluded from ASP
            "Cash/Uninsured":    wac,
        }

        total_rev = 0.0
        total_units = 0.0
        for ch in CHANNELS:
            if not ASP_ELIGIBLE.get(ch, False):
                continue
            pct = alloc.get(ch, 0) / 100
            u   = row["Units"] * pct
            p   = ch_prices[ch]
            total_rev   += u * p
            total_units += u

        monthly_asp = total_rev / total_units if total_units > 0 else wac
        records.append({"Period": row["Period"], "Year": yr, "Month": row["Month"],
                        "MonthIdx": row["MonthIdx"], "TotalUnits": row["Units"],
                        "EligibleUnits": total_units, "MonthlyRevASP": total_rev,
                        "MonthlyASP": monthly_asp, "WAC": wac})

    asp_df = pd.DataFrame(records)
    # 6-month rolling weighted average
    asp_df = asp_df.reset_index(drop=True)
    rolling_asp = []
    for i in range(len(asp_df)):
        window = asp_df.iloc[max(0, i-5):i+1]
        denom  = window["EligibleUnits"].sum()
        num    = window["MonthlyRevASP"].sum()
        rolling_asp.append(num / denom if denom > 0 else asp_df.iloc[i]["MonthlyASP"])
    asp_df["RollingASP_6M"] = rolling_asp
    asp_df["ASP_Plus6"]     = asp_df["RollingASP_6M"] * 1.06
    return asp_df

def compute_gtn(monthly_df, asp_df, channel_alloc_by_year, discount_by_year, rebate_by_year, other_by_year):
    """Compute monthly GTN deductions and net sales."""
    rows = []
    asp_lookup = dict(zip(asp_df["Period"], asp_df["RollingASP_6M"]))
    aspplus_lookup = dict(zip(asp_df["Period"], asp_df["ASP_Plus6"]))

    for _, row in monthly_df.iterrows():
        yr     = row["Year"]
        period = row["Period"]
        wac    = row["WAC"]
        units  = row["Units"]
        alloc  = channel_alloc_by_year.get(yr, channel_alloc_by_year[min(channel_alloc_by_year.keys())])
        disc   = discount_by_year.get(yr, discount_by_year[min(discount_by_year.keys())])
        rebate = rebate_by_year.get(yr, rebate_by_year[min(rebate_by_year.keys())])
        other  = other_by_year.get(yr, other_by_year[min(other_by_year.keys())])

        gpo_p  = wac * (1 - disc["gpo"]  / 100)
        idn_p  = wac * (1 - disc["idn"]  / 100)
        b340_p = wac * (1 - disc["b340"] / 100)
        va_p   = wac * (1 - disc["va"]   / 100)

        gross_sales = units * wac

        # Per-channel units
        ch_u = {ch: units * alloc.get(ch, 0) / 100 for ch in CHANNELS}

        # ── Rebates ──
        reb_com_pbm  = ch_u["Commercial PBM"]    * wac * rebate.get("com_pbm",0)/100
        reb_com_med  = ch_u["Commercial Medical"] * wac * rebate.get("com_med",0)/100
        reb_mcr_b    = 0.0
        reb_mcr_d    = ch_u["Medicare Part D"]   * wac * rebate.get("mcr_d",0)/100
        reb_mcaid    = ch_u["Medicaid FFS"]       * wac * rebate.get("mcaid",0)/100
        reb_man_mcaid= ch_u["Managed Medicaid"]   * wac * rebate.get("man_mcaid",0)/100
        total_rebates= reb_com_pbm + reb_com_med + reb_mcr_b + reb_mcr_d + reb_mcaid + reb_man_mcaid

        # ── Chargebacks (WAC − contract price) ──
        cb_gpo  = ch_u["GPO/IDN Non-340B"] * (wac - idn_p)
        cb_b340 = ch_u["GPO/IDN 340B"]     * (wac - b340_p)
        cb_va   = ch_u["VA/DoD/Federal"]   * (wac - va_p)
        total_cb = cb_gpo + cb_b340 + cb_va

        # ── Other deductions ──
        admin_fee = gross_sales * other.get("admin_fee",0)/100
        dist_fee  = gross_sales * other.get("dist_fee",0)/100
        copay     = gross_sales * other.get("copay",0)/100
        returns   = gross_sales * other.get("returns",0)/100
        total_other = admin_fee + dist_fee + copay + returns

        total_ded = total_rebates + total_cb + total_other
        net_sales = gross_sales - total_ded

        # ASP data
        asp_val  = asp_lookup.get(period, wac)
        asp6_val = aspplus_lookup.get(period, wac * 1.06)

        # IDN acquisition vs ASP flag
        idn_below_asp = asp_val < idn_p
        b340_below_asp= asp_val < b340_p

        rows.append({
            "Period": period, "Year": yr, "Month": row["Month"],
            "Units": units, "WAC": wac, "GrossSales": gross_sales,
            "Reb_ComPBM": reb_com_pbm, "Reb_ComMed": reb_com_med,
            "Reb_McrD": reb_mcr_d, "Reb_Mcaid": reb_mcaid, "Reb_ManMcaid": reb_man_mcaid,
            "TotalRebates": total_rebates,
            "CB_GPO": cb_gpo, "CB_340B": cb_b340, "CB_VA": cb_va,
            "TotalChargebacks": total_cb,
            "AdminFee": admin_fee, "DistFee": dist_fee, "Copay": copay, "Returns": returns,
            "TotalOther": total_other,
            "TotalDeductions": total_ded, "NetSales": net_sales,
            "ASP": asp_val, "ASPPlus6": asp6_val,
            "IDN_Price": idn_p, "B340_Price": b340_p,
            "IDN_Below_ASP": idn_below_asp, "B340_Below_ASP": b340_below_asp,
            "IDN_Spread": asp6_val - idn_p,
            "GTN_Pct": total_ded / gross_sales * 100 if gross_sales > 0 else 0,
        })
    return pd.DataFrame(rows)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#1A1A2E", family="Inter", size=12),
    legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor="#E2E8F0", borderwidth=1,
                font=dict(size=11, color="#2D3748")),
)
# xaxis/yaxis removed from PLOTLY_LAYOUT to prevent duplicate-keyword errors.
# Use apply_axes_style(fig) after update_layout to apply the brand grid.
PLOTLY_MARGIN = dict(t=40, b=30, l=80, r=80)
_GRID = dict(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1", gridwidth=1, zerolinewidth=1.5)

def apply_axes_style(fig):
    """Apply dark grid to all axes without conflicting with update_layout kwargs."""
    fig.update_xaxes(**_GRID)
    fig.update_yaxes(**_GRID)
    return fig

def hex_to_rgba(hex_color, alpha=0.73):
    """Convert a 6-digit hex color string to rgba() — Plotly doesn't accept 8-digit hex."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# Brand-first palette: Anakiwa family first, then readable accents on Prussian Blue
COLORS_MAIN = ["#A8D5FF","#D4EAFF","#4ade80","#fbbf24","#f87171","#c084fc","#6AB4F0","#fb923c","#60a5fa","#a78bfa"]

def compute_product_gtn_full(cat, forecast_years, n_years, monthly_weights):
    """Compute full GTN pipeline for a product from catalog entry.
    Returns (annual_gtn DataFrame, forecast_df) or None if inputs are empty.
    """
    fc_df = pd.DataFrame({
        "Year": forecast_years,
        "Annual Units": cat["units"][:n_years],
        "WAC per Unit": [round(cat["base_wac"] * (cat["wac_esc"] ** i), 2) for i in range(n_years)],
        "Monthly Profile": ["S-Curve (Launch)"] + ["Flat"] * (n_years - 1),
    })
    monthly_df = expand_to_monthly(fc_df, monthly_weights)

    # Build dicts
    ch_alloc_dict = {}
    for yr in forecast_years:
        ch_alloc_dict[yr] = dict(cat["channel_mix"])

    disc_dict = {}
    for i, yr in enumerate(forecast_years):
        disc_dict[yr] = {
            "gpo": round(cat["disc"]["gpo"] + i*cat["disc_esc"]["gpo"], 1),
            "idn": round(cat["disc"]["idn"] + i*cat["disc_esc"]["idn"], 1),
            "b340": cat["disc"]["b340"],
            "va": cat["disc"]["va"],
        }

    rebate_dict = {}
    for i, yr in enumerate(forecast_years):
        rebate_dict[yr] = {
            "com_pbm": round(cat["reb"]["com_pbm"] + i*cat["reb_esc"]["com_pbm"], 1),
            "com_med": round(cat["reb"]["com_med"] + i*cat["reb_esc"]["com_med"], 1),
            "mcr_d": round(cat["reb"]["mcr_d"] + i*cat["reb_esc"]["mcr_d"], 1),
            "mcaid": cat["reb"]["mcaid"],
            "man_mcaid": round(cat["reb"]["man_mcaid"] + i*cat["reb_esc"]["man_mcaid"], 1),
        }

    other_dict = {}
    for yr in forecast_years:
        other_dict[yr] = {
            "admin_fee": cat["other"]["admin"],
            "dist_fee": cat["other"]["dist"],
            "copay": cat["other"]["copay"],
            "returns": cat["other"]["returns"],
        }

    asp_df = compute_asp_series(monthly_df, ch_alloc_dict, disc_dict)
    gtn_df = compute_gtn(monthly_df, asp_df, ch_alloc_dict, disc_dict, rebate_dict, other_dict)

    annual_gtn = gtn_df.groupby("Year").agg(
        GrossSales=("GrossSales","sum"), TotalRebates=("TotalRebates","sum"),
        TotalChargebacks=("TotalChargebacks","sum"), TotalOther=("TotalOther","sum"),
        TotalDeductions=("TotalDeductions","sum"), NetSales=("NetSales","sum"),
        Units=("Units","sum"), GTN_Pct=("GTN_Pct","mean"),
    ).reset_index()
    annual_gtn["NetPrice"] = annual_gtn["NetSales"] / annual_gtn["Units"]
    annual_gtn["NetPct"]   = annual_gtn["NetSales"] / annual_gtn["GrossSales"] * 100

    return annual_gtn, fc_df


# PRODUCT CATALOG — 10 dummy products with distinct data
# ───────────────────────────────────────────────────────────────────
PRODUCT_CATALOG = {
    "RXPRODUCT-001": {
        "therapy_area": "Oncology", "admin_route": "IV Infusion (Buy & Bill)",
        "base_wac": 1500, "wac_esc": 1.03,
        "units": [10_000, 22_000, 38_000, 50_000, 58_000, 62_000, 65_000, 67_000, 68_000, 69_000],
        "channel_mix": {"Commercial PBM": 25, "Commercial Medical": 18, "Medicare Part B": 16,
                        "Medicare Part D": 12, "Medicaid FFS": 8, "Managed Medicaid": 6,
                        "GPO/IDN Non-340B": 7, "GPO/IDN 340B": 4, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 14.0, "idn": 20.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.3, "idn": 0.4, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 32.0, "com_med": 13.0, "mcr_d": 28.0, "mcaid": 23.1, "man_mcaid": 42.0},
        "reb_esc": {"com_pbm": 0.5, "com_med": 0.3, "mcr_d": 0.5, "mcaid": 0.0, "man_mcaid": 0.3},
        "other": {"admin": 2.0, "dist": 2.0, "copay": 3.5, "returns": 1.5},
    },
    "RXPRODUCT-002": {
        "therapy_area": "Rare Disease", "admin_route": "SC Injection",
        "base_wac": 8500, "wac_esc": 1.04,
        "units": [800, 1_800, 3_200, 5_000, 6_500, 7_200, 7_800, 8_000, 8_100, 8_200],
        "channel_mix": {"Commercial PBM": 35, "Commercial Medical": 10, "Medicare Part B": 8,
                        "Medicare Part D": 18, "Medicaid FFS": 10, "Managed Medicaid": 8,
                        "GPO/IDN Non-340B": 4, "GPO/IDN 340B": 2, "VA/DoD/Federal": 3, "Cash/Uninsured": 2},
        "disc": {"gpo": 10.0, "idn": 15.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.2, "idn": 0.5, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 25.0, "com_med": 10.0, "mcr_d": 22.0, "mcaid": 23.1, "man_mcaid": 35.0},
        "reb_esc": {"com_pbm": 0.4, "com_med": 0.2, "mcr_d": 0.6, "mcaid": 0.0, "man_mcaid": 0.4},
        "other": {"admin": 1.5, "dist": 3.0, "copay": 5.0, "returns": 1.0},
    },
    "RXPRODUCT-003": {
        "therapy_area": "Immunology", "admin_route": "SC Injection",
        "base_wac": 3200, "wac_esc": 1.035,
        "units": [15_000, 30_000, 52_000, 70_000, 82_000, 90_000, 95_000, 98_000, 100_000, 101_000],
        "channel_mix": {"Commercial PBM": 30, "Commercial Medical": 15, "Medicare Part B": 12,
                        "Medicare Part D": 15, "Medicaid FFS": 9, "Managed Medicaid": 7,
                        "GPO/IDN Non-340B": 5, "GPO/IDN 340B": 3, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 16.0, "idn": 22.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.4, "idn": 0.3, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 35.0, "com_med": 15.0, "mcr_d": 30.0, "mcaid": 23.1, "man_mcaid": 45.0},
        "reb_esc": {"com_pbm": 0.6, "com_med": 0.4, "mcr_d": 0.4, "mcaid": 0.0, "man_mcaid": 0.2},
        "other": {"admin": 2.0, "dist": 2.5, "copay": 4.0, "returns": 1.5},
    },
    "RXPRODUCT-004": {
        "therapy_area": "Cardiovascular", "admin_route": "Oral",
        "base_wac": 450, "wac_esc": 1.025,
        "units": [50_000, 120_000, 200_000, 280_000, 340_000, 380_000, 400_000, 410_000, 415_000, 418_000],
        "channel_mix": {"Commercial PBM": 40, "Commercial Medical": 5, "Medicare Part B": 3,
                        "Medicare Part D": 25, "Medicaid FFS": 10, "Managed Medicaid": 8,
                        "GPO/IDN Non-340B": 3, "GPO/IDN 340B": 2, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 8.0, "idn": 12.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.1, "idn": 0.2, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 40.0, "com_med": 8.0, "mcr_d": 35.0, "mcaid": 23.1, "man_mcaid": 50.0},
        "reb_esc": {"com_pbm": 0.7, "com_med": 0.1, "mcr_d": 0.3, "mcaid": 0.0, "man_mcaid": 0.5},
        "other": {"admin": 2.5, "dist": 1.5, "copay": 2.0, "returns": 2.0},
    },
    "RXPRODUCT-005": {
        "therapy_area": "Neurology", "admin_route": "IV Infusion (Buy & Bill)",
        "base_wac": 5800, "wac_esc": 1.03,
        "units": [3_000, 7_500, 14_000, 20_000, 25_000, 28_000, 30_000, 31_000, 31_500, 32_000],
        "channel_mix": {"Commercial PBM": 20, "Commercial Medical": 22, "Medicare Part B": 20,
                        "Medicare Part D": 10, "Medicaid FFS": 7, "Managed Medicaid": 5,
                        "GPO/IDN Non-340B": 8, "GPO/IDN 340B": 4, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 15.0, "idn": 21.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.5, "idn": 0.6, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 28.0, "com_med": 14.0, "mcr_d": 25.0, "mcaid": 23.1, "man_mcaid": 40.0},
        "reb_esc": {"com_pbm": 0.3, "com_med": 0.5, "mcr_d": 0.7, "mcaid": 0.0, "man_mcaid": 0.6},
        "other": {"admin": 2.0, "dist": 2.0, "copay": 3.0, "returns": 1.5},
    },
    "RXPRODUCT-006": {
        "therapy_area": "Oncology", "admin_route": "SC Injection",
        "base_wac": 12000, "wac_esc": 1.045,
        "units": [2_000, 5_000, 9_000, 13_000, 16_000, 18_000, 19_500, 20_500, 21_000, 21_200],
        "channel_mix": {"Commercial PBM": 22, "Commercial Medical": 20, "Medicare Part B": 18,
                        "Medicare Part D": 10, "Medicaid FFS": 8, "Managed Medicaid": 6,
                        "GPO/IDN Non-340B": 8, "GPO/IDN 340B": 4, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 12.0, "idn": 18.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.6, "idn": 0.7, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 30.0, "com_med": 12.0, "mcr_d": 26.0, "mcaid": 23.1, "man_mcaid": 38.0},
        "reb_esc": {"com_pbm": 0.8, "com_med": 0.6, "mcr_d": 0.2, "mcaid": 0.0, "man_mcaid": 0.7},
        "other": {"admin": 1.5, "dist": 2.5, "copay": 4.0, "returns": 1.0},
    },
    "RXPRODUCT-007": {
        "therapy_area": "Immunology", "admin_route": "IV Infusion (Buy & Bill)",
        "base_wac": 4200, "wac_esc": 1.032,
        "units": [8_000, 18_000, 32_000, 44_000, 52_000, 56_000, 58_000, 59_500, 60_000, 60_500],
        "channel_mix": {"Commercial PBM": 28, "Commercial Medical": 16, "Medicare Part B": 14,
                        "Medicare Part D": 14, "Medicaid FFS": 8, "Managed Medicaid": 7,
                        "GPO/IDN Non-340B": 6, "GPO/IDN 340B": 3, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 13.0, "idn": 19.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.7, "idn": 0.8, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 33.0, "com_med": 14.0, "mcr_d": 29.0, "mcaid": 23.1, "man_mcaid": 43.0},
        "reb_esc": {"com_pbm": 0.9, "com_med": 0.7, "mcr_d": 0.8, "mcaid": 0.0, "man_mcaid": 0.8},
        "other": {"admin": 2.0, "dist": 2.0, "copay": 3.5, "returns": 1.5},
    },
    "RXPRODUCT-008": {
        "therapy_area": "Rare Disease", "admin_route": "IV Infusion (Buy & Bill)",
        "base_wac": 25000, "wac_esc": 1.05,
        "units": [300, 700, 1_200, 1_800, 2_300, 2_600, 2_800, 2_900, 2_950, 3_000],
        "channel_mix": {"Commercial PBM": 18, "Commercial Medical": 25, "Medicare Part B": 15,
                        "Medicare Part D": 8, "Medicaid FFS": 12, "Managed Medicaid": 8,
                        "GPO/IDN Non-340B": 5, "GPO/IDN 340B": 3, "VA/DoD/Federal": 4, "Cash/Uninsured": 2},
        "disc": {"gpo": 10.0, "idn": 16.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.8, "idn": 0.9, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 22.0, "com_med": 10.0, "mcr_d": 20.0, "mcaid": 23.1, "man_mcaid": 30.0},
        "reb_esc": {"com_pbm": 0.1, "com_med": 0.8, "mcr_d": 0.9, "mcaid": 0.0, "man_mcaid": 0.9},
        "other": {"admin": 1.5, "dist": 3.0, "copay": 6.0, "returns": 0.8},
    },
    "RXPRODUCT-009": {
        "therapy_area": "Cardiovascular", "admin_route": "SC Injection",
        "base_wac": 2100, "wac_esc": 1.028,
        "units": [20_000, 45_000, 75_000, 100_000, 120_000, 132_000, 138_000, 142_000, 144_000, 145_000],
        "channel_mix": {"Commercial PBM": 32, "Commercial Medical": 12, "Medicare Part B": 10,
                        "Medicare Part D": 20, "Medicaid FFS": 9, "Managed Medicaid": 7,
                        "GPO/IDN Non-340B": 4, "GPO/IDN 340B": 2, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 11.0, "idn": 17.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 0.9, "idn": 0.1, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 36.0, "com_med": 11.0, "mcr_d": 32.0, "mcaid": 23.1, "man_mcaid": 46.0},
        "reb_esc": {"com_pbm": 1.0, "com_med": 0.9, "mcr_d": 0.1, "mcaid": 0.0, "man_mcaid": 1.0},
        "other": {"admin": 2.0, "dist": 2.0, "copay": 3.0, "returns": 1.5},
    },
    "RXPRODUCT-010": {
        "therapy_area": "Neurology", "admin_route": "Oral",
        "base_wac": 900, "wac_esc": 1.03,
        "units": [35_000, 80_000, 140_000, 190_000, 230_000, 255_000, 268_000, 275_000, 278_000, 280_000],
        "channel_mix": {"Commercial PBM": 38, "Commercial Medical": 5, "Medicare Part B": 3,
                        "Medicare Part D": 28, "Medicaid FFS": 10, "Managed Medicaid": 7,
                        "GPO/IDN Non-340B": 3, "GPO/IDN 340B": 2, "VA/DoD/Federal": 2, "Cash/Uninsured": 2},
        "disc": {"gpo": 9.0, "idn": 14.0, "b340": 25.6, "va": 24.0},
        "disc_esc": {"gpo": 1.0, "idn": 1.0, "b340": 0.0, "va": 0.0},
        "reb": {"com_pbm": 42.0, "com_med": 7.0, "mcr_d": 38.0, "mcaid": 23.1, "man_mcaid": 52.0},
        "reb_esc": {"com_pbm": 0.2, "com_med": 1.0, "mcr_d": 1.0, "mcaid": 0.0, "man_mcaid": 0.1},
        "other": {"admin": 2.5, "dist": 1.5, "copay": 2.5, "returns": 2.0},
    },
}

def load_product_defaults(prod_key, forecast_years, n_years):
    """Load product-specific dummy data into session state."""
    cat = PRODUCT_CATALOG[prod_key]
    # Forecast
    st.session_state.forecast_df = pd.DataFrame({
        "Year": forecast_years,
        "Annual Units": cat["units"][:n_years],
        "WAC per Unit": [round(cat["base_wac"] * (cat["wac_esc"] ** i), 2) for i in range(n_years)],
        "Monthly Profile": ["S-Curve (Launch)"] + ["Flat"] * (n_years - 1),
    })
    # Channel allocation
    rows = []
    for yr in forecast_years:
        row = {"Year": yr}
        row.update(cat["channel_mix"])
        rows.append(row)
    st.session_state.channel_alloc_raw = pd.DataFrame(rows)
    # Discounts
    rows = []
    for i, yr in enumerate(forecast_years):
        rows.append({"Year": yr,
                     "GPO Disc %": round(cat["disc"]["gpo"] + i*cat["disc_esc"]["gpo"], 1),
                     "IDN Disc %": round(cat["disc"]["idn"] + i*cat["disc_esc"]["idn"], 1),
                     "340B Disc %": cat["disc"]["b340"],
                     "VA FSS Disc %": cat["disc"]["va"]})
    st.session_state.discount_raw = pd.DataFrame(rows)
    # Rebates
    rows = []
    for i, yr in enumerate(forecast_years):
        rows.append({"Year": yr,
                     "Com PBM %": round(cat["reb"]["com_pbm"] + i*cat["reb_esc"]["com_pbm"], 1),
                     "Com Med %": round(cat["reb"]["com_med"] + i*cat["reb_esc"]["com_med"], 1),
                     "Mcr Part D %": round(cat["reb"]["mcr_d"] + i*cat["reb_esc"]["mcr_d"], 1),
                     "Medicaid FFS %": cat["reb"]["mcaid"],
                     "Managed Mcaid %": round(cat["reb"]["man_mcaid"] + i*cat["reb_esc"]["man_mcaid"], 1)})
    st.session_state.rebate_raw = pd.DataFrame(rows)
    # Other fees
    rows = []
    for yr in forecast_years:
        rows.append({"Year": yr, "Admin Fee %": cat["other"]["admin"],
                     "Dist Fee %": cat["other"]["dist"],
                     "Copay Support %": cat["other"]["copay"],
                     "Returns %": cat["other"]["returns"]})
    st.session_state.other_raw = pd.DataFrame(rows)
    # Clear computed data so ASP Engine re-runs
    for k in ["asp_df", "monthly_df", "ch_alloc_dict", "disc_dict", "rebate_dict", "other_dict"]:
        st.session_state.pop(k, None)
    # Clear per-year stepper keys so Forecast tab picks up new values
    # Clear per-year stepper keys so Forecast tab picks up new values
    keys_to_clear = [k for k in st.session_state.keys()
                    if k.startswith(("fc_units_", "fc_wac_", "fc_prof_",
                                    "ch_", "disc_", "reb_", "oth_",
                                    "ni_", "sel_prof_"))]
    for k in keys_to_clear:
        del st.session_state[k]

# ───────────────────────────────────────────────────────────────────
# SIDEBAR
# ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚕️ PharmGTN Pro v4")
    st.markdown("<div style='font-size:1.1rem;font-weight:600;color:#1f4e79;margin-bottom:12px;'>Multi-Year GTN Engine</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Product selector (sidebar — synced with dashboard)
    product_name = st.selectbox(
        "Product",
        list(PRODUCT_CATALOG.keys()),
        key="sidebar_prod_sel"
    )
    # Auto-display therapy area and admin route from catalog
    _cat = PRODUCT_CATALOG[product_name]
    therapy_area = _cat["therapy_area"]
    admin_route = _cat["admin_route"]
    st.markdown(f"<div style='font-size:0.82rem;color:#4A5568;margin-top:-8px;margin-bottom:8px;'>"
                f"<b>{therapy_area}</b> · {admin_route.split('(')[0].strip()}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Forecast Horizon")
    n_years = st.slider("Number of Forecast Years", 1, 10, 7)
    start_year = st.number_input("Start Year", 2024, 2030, 2025, 1)
    forecast_years = list(range(start_year, start_year + n_years))
    monthly_profile_choice = st.selectbox("Monthly Distribution Profile", list(MONTH_PROFILES.keys()) + ["Custom"])
    st.markdown("---")
    st.markdown("### 📋 Navigation")
    st.markdown("<div style='font-size:0.95rem;line-height:1.8;'>"
                "<b>0.</b> Dashboard<br>"
                "<b>1.</b> Forecast Volumes<br>"
                "<b>2.</b> Channel Mix<br>"
                "<b>3.</b> Contract Terms<br>"
                "<b>4.</b> ASP Engine<br>"
                "<b>5.</b> GTN Base Model<br>"
                "<b>6.</b> Buy & Bill Analysis</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<div style='font-size:0.9rem;font-weight:600;'>Horizon: {forecast_years[0]}–{forecast_years[-1]} ({n_years} yrs)</div>", unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS — load from product catalog on change
# ───────────────────────────────────────────────────────────────────
# Detect product change — reload all data
if st.session_state.get("_active_product") != product_name:
    load_product_defaults(product_name, forecast_years, n_years)
    st.session_state["_active_product"] = product_name
    # Reset dashboard brand filter each time product changes
    st.session_state["dash_brands"] = [product_name]

# Fallback: if no data yet (first run), load defaults
if "forecast_df" not in st.session_state or len(st.session_state.forecast_df) != n_years:
    load_product_defaults(product_name, forecast_years, n_years)
    st.session_state["_active_product"] = product_name
    st.session_state["dash_brands"] = [product_name]

if "channel_alloc_raw" not in st.session_state:
    load_product_defaults(product_name, forecast_years, n_years)

if "discount_raw" not in st.session_state:
    load_product_defaults(product_name, forecast_years, n_years)

if "rebate_raw" not in st.session_state:
    load_product_defaults(product_name, forecast_years, n_years)

if "other_raw" not in st.session_state:
    load_product_defaults(product_name, forecast_years, n_years)


# ── Multi-IDN session state ──────────────────────────────────────────
if "idn_list" not in st.session_state:
    st.session_state.idn_list = [
        {"name": "IDN-A (Academic Medical)",  "discount": 20.0, "volume_pct": 30.0, "is_340b": False},
        {"name": "IDN-B (Community Hospital)", "discount": 18.0, "volume_pct": 25.0, "is_340b": False},
        {"name": "IDN-C (340B Covered Entity)","discount": 25.6, "volume_pct": 15.0, "is_340b": True},
        {"name": "IDN-D (GPO Member)",         "discount": 15.0, "volume_pct": 20.0, "is_340b": False},
        {"name": "IDN-E (VA Affiliate)",       "discount": 24.0, "volume_pct": 10.0, "is_340b": False},
    ]

# ───────────────────────────────────────────────────────────────────
# TABS
# ───────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏠 Dashboard",
    "📊 Forecast Volumes",
    "🔀 Channel Allocation",
    "📋 Contract Terms",
    "📐 ASP Engine",
    "🧮 GTN Model",
    "🏥 Buy & Bill — Multi-IDN",
])

# ═══════════════════════════════════════════════════════════════════
# TAB 0 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("## 🏠 Executive Dashboard")

    # ── Dashboard Filters Bar ─────────────────────────────────────────
    st.markdown("""<div style='background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;
    padding:16px 24px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.04);'>
    <div style='font-family:Inter;font-size:0.82rem;font-weight:800;color:#1a365d;
    text-transform:uppercase;letter-spacing:0.6px;margin-bottom:12px;'>Dashboard Filters</div>
    <div style='font-size:0.78rem;color:#64748B;margin-bottom:12px;'>
    Select <b>Brand</b> to choose specific products, or <b>Portfolio</b> to view aggregated data
    across all products. Use the Channel Filter to focus on specific payer channels.</div>
    </div>""", unsafe_allow_html=True)

    f_col1, f_col2, f_col3 = st.columns([1.2, 1.5, 2.5])

    with f_col1:
        dash_scope = st.radio(
            "SCOPE", ["Brand", "Portfolio"],
            horizontal=True, key="dash_scope",
            label_visibility="visible"
        )

    with f_col2:
        dash_ch_filter = st.multiselect(
            "Channel Filter", CHANNELS,
            default=CHANNELS, key="dash_ch_filter",
        )
        if not dash_ch_filter:
            dash_ch_filter = CHANNELS
        # Store in session_state for other tabs
        st.session_state["_active_channels"] = dash_ch_filter

    with f_col3:
        if dash_scope == "Brand":
            dash_brands = st.multiselect(
                "BRANDS TO INCLUDE",
                list(PRODUCT_CATALOG.keys()),
                default=st.session_state.get("dash_brands", [product_name]),
                key="dash_brands",
            )
            if not dash_brands:
                dash_brands = [product_name]
                st.session_state["dash_brands"] = dash_brands
        else:
            dash_brands = list(PRODUCT_CATALOG.keys())
            st.markdown(f"""<div style='background:#EBF4FF;border:1px solid #BEE3F8;border-radius:8px;
            padding:10px 16px;margin-top:4px;font-size:0.82rem;color:#1a365d;font-weight:600;'>
            📊 Viewing aggregated analysis for all {len(dash_brands)} products
            </div>""", unsafe_allow_html=True)

    # Build status banner
    n_brands = len(dash_brands)
    n_ch     = len(dash_ch_filter)
    ch_label = "All channels" if n_ch == len(CHANNELS) else f"{n_ch} of {len(CHANNELS)} channels"
    scope_label = f"{n_brands} brand{'s' if n_brands > 1 else ''}" if dash_scope == "Brand" else "Full portfolio"
    st.markdown(f"""<div style='background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;
    padding:10px 16px;margin-bottom:16px;font-size:0.82rem;color:#166534;font-weight:600;'>
    ✅ Viewing analysis for <b>{scope_label}</b> · {ch_label}
    </div>""", unsafe_allow_html=True)

    # ── Compute aggregated data ───────────────────────────────────────
    monthly_weights = get_monthly_weights(monthly_profile_choice, n_years, None)

    agg_annual = None
    agg_fc     = None
    for pkey in dash_brands:
        cat = PRODUCT_CATALOG[pkey]
        ann_gtn, fc_prod = compute_product_gtn_full(cat, forecast_years, n_years, monthly_weights)
        if agg_annual is None:
            agg_annual = ann_gtn.copy()
            agg_fc     = fc_prod.copy()
            agg_fc.rename(columns={"Annual Units": "Annual Units"}, inplace=True)
        else:
            for col in ["GrossSales","TotalRebates","TotalChargebacks","TotalOther",
                         "TotalDeductions","NetSales","Units"]:
                agg_annual[col] = agg_annual[col] + ann_gtn[col]
            agg_fc["Annual Units"] = agg_fc["Annual Units"] + fc_prod["Annual Units"]
            # WAC = weighted average for display
            agg_fc["WAC per Unit"] = (
                agg_fc["WAC per Unit"] * (agg_fc["Annual Units"] - fc_prod["Annual Units"])
                + fc_prod["WAC per Unit"] * fc_prod["Annual Units"]
            ) / agg_fc["Annual Units"]

    # Recalculate derived columns
    agg_annual["GTN_Pct"]  = agg_annual["TotalDeductions"] / agg_annual["GrossSales"] * 100
    agg_annual["NetPrice"] = agg_annual["NetSales"] / agg_annual["Units"]
    agg_annual["NetPct"]   = agg_annual["NetSales"] / agg_annual["GrossSales"] * 100

    ann_dash    = agg_annual
    fc          = agg_fc
    gross_by_yr = fc["Annual Units"] * fc["WAC per Unit"]
    total_gross = ann_dash["GrossSales"].sum()
    total_units = ann_dash["Units"].sum()
    total_net   = ann_dash["NetSales"].sum()
    total_ded   = ann_dash["TotalDeductions"].sum()
    total_reb   = ann_dash["TotalRebates"].sum()
    total_cb    = ann_dash["TotalChargebacks"].sum()
    total_other = ann_dash["TotalOther"].sum()
    avg_gtn_pct = total_ded / total_gross * 100 if total_gross > 0 else 0
    peak_idx    = ann_dash["GrossSales"].idxmax()
    peak_yr     = ann_dash.loc[peak_idx, "Year"]
    has_data    = True  # Always true now since we compute inline

    # ── KPI Banner ────────────────────────────────────────────────────
    banner_name = ", ".join(dash_brands[:3]) + (f" +{len(dash_brands)-3} more" if len(dash_brands) > 3 else "")
    st.markdown(f"""
    <div style='background:#FFFFFF;border:1px solid #E6E6E6;
    border-radius:12px;padding:18px 24px;margin-bottom:16px;'>
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:4px;'>
    <span style='font-family:Inter;font-size:1.2rem;font-weight:800;color:#1f4e79;'>{banner_name}</span>
    <span style='background:#F7F9FC;color:#1f4e79;border:1px solid #E0E0E0;border-radius:8px;
    padding:3px 10px;font-size:0.85rem;font-family:JetBrains Mono;'>{therapy_area}</span>
    <span style='background:#F7F9FC;color:#1f4e79;border:1px solid #E0E0E0;border-radius:8px;
    padding:3px 10px;font-size:0.85rem;font-family:JetBrains Mono;'>{admin_route.split("(")[0].strip()}</span>
    <span style='background:#F7F9FC;color:#1f4e79;border:1px solid #E0E0E0;border-radius:8px;
    padding:3px 10px;font-size:0.85rem;font-family:JetBrains Mono;'>
    {forecast_years[0]}–{forecast_years[-1]} · {n_years}yr</span>
    </div></div>""", unsafe_allow_html=True)

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Units", fmt_u(total_units))
    k2.metric("Gross Sales", fmt_b(total_gross) if total_gross>=1e9 else fmt_m(total_gross))
    k3.metric("Net Sales",   fmt_b(total_net)   if total_net  >=1e9 else fmt_m(total_net))
    k4.metric("Total Deductions", fmt_m(total_ded))
    k5,k6,k7 = st.columns(3)
    k5.metric("Avg GTN %",  fmt_pct(avg_gtn_pct))
    k6.metric("Peak Sales Year", str(peak_yr))
    k7.metric("Brands Included", str(n_brands))

    st.markdown("---")

    # ── Row 1: Total Sales Over Time + GTN Waterfall ─────────────────
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="sec-header">📈 Total Sales Over Time — Gross vs Net</div>', unsafe_allow_html=True)
        fig_sales = go.Figure()
        fig_sales.add_trace(go.Bar(
            x=ann_dash["Year"], y=ann_dash["GrossSales"]/1e6,
            name="Gross Sales", marker_color="#A8D5FF", opacity=0.6,
            hovertemplate="<b>%{x}</b><br>Gross: $%{y:.2f}M<extra></extra>",
        ))
        fig_sales.add_trace(go.Bar(
            x=ann_dash["Year"], y=ann_dash["NetSales"]/1e6,
            name="Net Sales", marker_color="#4ade80", opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Net: $%{y:.2f}M<extra></extra>",
        ))
        # GTN deduction fill
        fig_sales.add_trace(go.Scatter(
            x=ann_dash["Year"].tolist() + ann_dash["Year"].tolist()[::-1],
            y=(ann_dash["GrossSales"]/1e6).tolist() + (ann_dash["NetSales"]/1e6).tolist()[::-1],
            fill="toself", fillcolor="rgba(248,113,113,0.10)",
            line=dict(color="rgba(0,0,0,0)"), name="GTN Deductions",
            hoverinfo="skip",
        ))
        fig_sales.update_layout(
            barmode="overlay", height=340, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            yaxis=dict(title="Sales Revenue ($ Millions USD)", gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
            legend_font_size=10,
        )
        apply_axes_style(fig_sales)
        st.plotly_chart(fig_sales, use_container_width=True, theme=None)

    with col2:
        st.markdown('<div class="sec-header">📉 GTN Waterfall — Full Forecast Period</div>', unsafe_allow_html=True)
        wf_labels = ["Gross Sales","(-) Rebates","(-) Chargebacks","(-) Fees/Other","Net Sales"]
        wf_vals   = [total_gross, -total_reb, -total_cb, -total_other, total_net]
        wf_measure= ["absolute","relative","relative","relative","total"]
        wf_pcts   = ["100%",
                     f"-{total_reb/total_gross*100:.1f}%" if total_gross > 0 else "0%",
                     f"-{total_cb/total_gross*100:.1f}%" if total_gross > 0 else "0%",
                     f"-{total_other/total_gross*100:.1f}%" if total_gross > 0 else "0%",
                     f"{total_net/total_gross*100:.1f}%" if total_gross > 0 else "0%"]
        fig_wfall = go.Figure(go.Waterfall(
            measure=wf_measure, x=wf_labels,
            y=[v/1e6 for v in wf_vals],
            connector=dict(line=dict(color="#003A8C", width=1)),
            decreasing=dict(marker=dict(color="#f87171")),
            increasing=dict(marker=dict(color="#4ade80")),
            totals=dict(marker=dict(color="#A8D5FF",
                        line=dict(color="#D4EAFF", width=2))),
            text=[f"${abs(v)/1e6:.1f}M<br><span style='font-size:9px'>{p}</span>"
                  for v, p in zip(wf_vals, wf_pcts)],
            textposition="outside",
            textfont=dict(color="#4A5568", size=10),
        ))
        fig_wfall.update_layout(
            title=f"GTN Waterfall {forecast_years[0]}–{forecast_years[-1]}",
            height=340, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            showlegend=False,
            yaxis=dict(title="Amount ($ Millions USD)", gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
        )
        apply_axes_style(fig_wfall)
        st.plotly_chart(fig_wfall, use_container_width=True, theme=None)

    # ── Row 2: Annual deduction breakdown + GTN% trend ────────────────
    col3, col4 = st.columns([1.2, 1])

    with col3:
        st.markdown('<div class="sec-header">🧩 Gross-to-Net Deduction Breakdown by Year</div>', unsafe_allow_html=True)
        fig_ded = go.Figure()
        fig_ded.add_trace(go.Bar(x=ann_dash["Year"],
            y=ann_dash["TotalRebates"]/ann_dash["GrossSales"]*100,
            name="Rebates", marker_color="#f87171", opacity=0.85))
        fig_ded.add_trace(go.Bar(x=ann_dash["Year"],
            y=ann_dash["TotalChargebacks"]/ann_dash["GrossSales"]*100,
            name="Chargebacks", marker_color="#fb923c", opacity=0.85))
        fig_ded.add_trace(go.Bar(x=ann_dash["Year"],
            y=ann_dash["TotalOther"]/ann_dash["GrossSales"]*100,
            name="Fees/Other", marker_color="#fbbf24", opacity=0.85))
        fig_ded.add_trace(go.Scatter(
            x=ann_dash["Year"], y=ann_dash["GTN_Pct"],
            name="Total GTN %", mode="lines+markers",
            line=dict(color="#A8D5FF", width=2.5),
            marker=dict(size=8, symbol="diamond"),
            text=[fmt_pct(v) for v in ann_dash["GTN_Pct"]],
            textposition="top center", textfont=dict(size=9, color="#1A1A2E"),
        ))
        fig_ded.update_layout(
            barmode="stack", height=300, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            yaxis=dict(title="Percentage of Gross Sales (%)", gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
            legend_font_size=10,
        )
        apply_axes_style(fig_ded)
        st.plotly_chart(fig_ded, use_container_width=True, theme=None)

    with col4:
        st.markdown('<div class="sec-header">🥧 Payer Channel Mix</div>', unsafe_allow_html=True)
        ch_raw = st.session_state.channel_alloc_raw
        yr_pie_options = [str(y) for y in forecast_years]
        yr_pie_sel = st.selectbox("Year", yr_pie_options, index=0, key="dash_pie_yr",
                                   label_visibility="collapsed")
        yr_pie_int = int(yr_pie_sel)
        row_pie = ch_raw[ch_raw["Year"]==yr_pie_int].iloc[0] if yr_pie_int in ch_raw["Year"].values else ch_raw.iloc[0]
        vals_pie = [row_pie[ch] for ch in dash_ch_filter if ch in row_pie.index]
        _dash_labels = [ch for ch in dash_ch_filter if ch in row_pie.index]
        fig_pie = go.Figure(go.Pie(
            labels=_dash_labels, values=vals_pie, hole=0.44,
            marker_colors=COLORS_MAIN, textfont=dict(size=9, color="#1A1A2E"),
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#1A1A2E", height=280,
            margin=dict(t=10, b=10, l=5, r=5),
            showlegend=True, legend=dict(font_size=9, font=dict(color="#1A1A2E"), bgcolor="rgba(255,255,255,0.8)", bordercolor="#E2E8F0", borderwidth=1),
            annotations=[dict(text=yr_pie_sel, x=0.5, y=0.5, showarrow=False,
                              font=dict(size=16, color="#1f4e79", family="Inter"))],
        )
        st.plotly_chart(fig_pie, use_container_width=True, theme=None)

    # ── Row 3: Customer / IDN Summary ────────────────────────────────
    st.markdown('<div class="sec-header">🏥 Customer / IDN Summary</div>', unsafe_allow_html=True)
    idn_list = st.session_state.idn_list
    idn_cols = st.columns(len(idn_list))
    wac_y1 = fc["WAC per Unit"].iloc[0]
    for i, idn in enumerate(idn_list):
        acq    = wac_y1 * (1 - idn["discount"]/100)
        with idn_cols[i]:
            flag = "🟡 340B" if idn["is_340b"] else "🔵 GPO"
            st.markdown(f"""
            <div style='background:#002766;border:1px solid #6AB4F0;border-radius:10px;
            padding:12px 14px;text-align:center;'>
            <div style='font-family:Syne;font-size:0.82rem;font-weight:700;color:#FFFFFF;
            margin-bottom:6px;'>{idn["name"]}</div>
            <div style='font-size:0.68rem;color:#FFFFFF;margin-bottom:8px;'>{flag}</div>
            <div style='font-family:JetBrains Mono;font-size:0.95rem;color:#FFFFFF;'>{idn["discount"]}% off WAC</div>
            <div style='font-family:JetBrains Mono;font-size:0.8rem;color:#FFFFFF;'>{fmt_d(acq)}/unit</div>
            <div style='font-size:0.7rem;color:#FFFFFF;margin-top:4px;'>{idn["volume_pct"]}% of B&B vol</div>
            </div>""", unsafe_allow_html=True)

    # ── Row 4: Full product summary table ────────────────────────────
    st.markdown('<div class="sec-header">📋 Product Summary — All Years</div>', unsafe_allow_html=True)

    # Safe single-value lookup — returns default if year not found
    def _v(df, yr_col, yr, val_col, default=0.0):
        rows = df.loc[df[yr_col] == yr, val_col]
        return rows.values[0] if len(rows) > 0 else default

    dash_T = pd.DataFrame({
        "Metric": ["Annual Units","WAC/Unit","Gross Sales ($M)",
                   "Rebates ($M)","Chargebacks ($M)","Fees/Other ($M)",
                   "Total Deductions ($M)","Net Sales ($M)","GTN %","Net $/Unit","Net % of WAC"],
        **{str(yr): [
            fmt_u(int(_v(ann_dash, "Year", yr, "Units"))),
            fmt_d(_v(fc, "Year", yr, "WAC per Unit")),
            f"${_v(ann_dash,'Year',yr,'GrossSales')/1e6:.2f}M",
            f"${_v(ann_dash,'Year',yr,'TotalRebates')/1e6:.2f}M",
            f"${_v(ann_dash,'Year',yr,'TotalChargebacks')/1e6:.2f}M",
            f"${_v(ann_dash,'Year',yr,'TotalOther')/1e6:.2f}M",
            f"${_v(ann_dash,'Year',yr,'TotalDeductions')/1e6:.2f}M",
            f"${_v(ann_dash,'Year',yr,'NetSales')/1e6:.2f}M",
            fmt_pct(_v(ann_dash, "Year", yr, "GTN_Pct")),
            fmt_d(_v(ann_dash, "Year", yr, "NetPrice")),
            fmt_pct(_v(ann_dash, "Year", yr, "NetPct")),
        ] for yr in ann_dash["Year"].tolist()}
    })
    st.dataframe(dash_T, use_container_width=True, hide_index=True)



# ═══════════════════════════════════════════════════════════════════
# TAB 1 — FORECAST VOLUMES
# ═══════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("## 📊 Forecast Volumes & WAC")
    st.markdown("""<div class='info-box'>
    Enter annual unit forecasts and WAC per unit for each year. WAC typically increases with CPI-U 
    (currently capped at CPI-U under IRA for Medicare-negotiated drugs). Monthly distribution 
    is applied via the profile selected per year.
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-header">📥 Annual Forecast Input — Years as Columns</div>', unsafe_allow_html=True)

    # ── Per-year stepper cards ──
    fc_src = st.session_state.forecast_df.copy()
    years  = fc_src["Year"].tolist()

    # Init editable values in session state on first load
    for i, yr in enumerate(years):
        if f"fc_units_{yr}" not in st.session_state:
            st.session_state[f"fc_units_{yr}"] = int(fc_src.loc[i, "Annual Units"])
        if f"fc_wac_{yr}" not in st.session_state:
            st.session_state[f"fc_wac_{yr}"] = float(fc_src.loc[i, "WAC per Unit"])
        if f"fc_prof_{yr}" not in st.session_state:
            st.session_state[f"fc_prof_{yr}"] = str(fc_src.loc[i, "Monthly Profile"])

    # ── Year columns with steppers ──
    year_cols = st.columns(len(years))
    new_units    = []
    new_wacs     = []
    new_profiles = []

    for i, yr in enumerate(years):
        with year_cols[i]:
            st.markdown(f"<div class='yr-label'>📅 {yr}</div>", unsafe_allow_html=True)

            # Units stepper
            st.markdown("<div class='metric-label-sm'>Annual Units</div>", unsafe_allow_html=True)
            u_val = st.number_input(
                "Units", label_visibility="collapsed",
                min_value=0, max_value=10_000_000,
                value=st.session_state[f"fc_units_{yr}"],
                step=1_000,
                key=f"ni_units_{yr}",
            )
            st.session_state[f"fc_units_{yr}"] = u_val
            new_units.append(u_val)

            # WAC stepper
            st.markdown("<div class='metric-label-sm'>WAC $/unit</div>", unsafe_allow_html=True)
            w_val = st.number_input(
                "WAC", label_visibility="collapsed",
                min_value=0.01, max_value=1_000_000.0,
                value=st.session_state[f"fc_wac_{yr}"],
                step=25.0, format="%.2f",
                key=f"ni_wac_{yr}",
            )
            st.session_state[f"fc_wac_{yr}"] = w_val
            new_wacs.append(w_val)

            # Profile selectbox
            st.markdown("<div class='metric-label-sm'>Profile</div>", unsafe_allow_html=True)
            prof_options = list(MONTH_PROFILES.keys())
            cur_prof = st.session_state[f"fc_prof_{yr}"]
            p_val = st.selectbox(
                "Profile", prof_options,
                index=prof_options.index(cur_prof) if cur_prof in prof_options else 0,
                key=f"sel_prof_{yr}",
                label_visibility="collapsed",
            )
            st.session_state[f"fc_prof_{yr}"] = p_val
            new_profiles.append(p_val)

    # Reconstruct forecast_df
    forecast_edited = pd.DataFrame({
        "Year":            years,
        "Annual Units":    new_units,
        "WAC per Unit":    new_wacs,
        "Monthly Profile": new_profiles,
    })
    st.session_state.forecast_df = forecast_edited

    # ── Forecast Summary (full width, below transposed input) ──
    st.markdown('<div class="sec-header">📈 Forecast Summary</div>', unsafe_allow_html=True)
    fc = st.session_state.forecast_df
    gross_by_year = fc["Annual Units"] * fc["WAC per Unit"]
    total_units_all = fc["Annual Units"].sum()
    total_gross_all = gross_by_year.sum()
    peak_yr_idx = gross_by_year.idxmax()

    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    sum_col1.metric("Total Units (All Years)", fmt_u(total_units_all))
    sum_col2.metric("Total Gross Sales", fmt_b(total_gross_all) if total_gross_all >= 1e9 else fmt_m(total_gross_all))
    sum_col3.metric("Peak Year", str(fc.loc[peak_yr_idx, "Year"]))
    sum_col4.metric("Peak Gross Sales", fmt_m(gross_by_year[peak_yr_idx]))

    fig_fc = make_subplots(specs=[[{"secondary_y": True}]])
    fig_fc.add_trace(go.Bar(x=fc["Year"], y=fc["Annual Units"]/1000,
                            name="Units (K)", marker_color="#7c4dff", opacity=0.75), secondary_y=False)
    fig_fc.add_trace(go.Scatter(x=fc["Year"], y=gross_by_year/1e6,
                                name="Gross $M", mode="lines+markers",
                                line=dict(color="#A8D5FF", width=2.5),
                                marker=dict(size=7)), secondary_y=True)
    fig_fc.update_layout(title="Units & Gross Sales by Year", height=300, **PLOTLY_LAYOUT,
                         margin=dict(t=40,b=20,l=80,r=80))
    fig_fc.update_yaxes(title_text="Sales Volume (Thousands of Units)", secondary_y=False)
    fig_fc.update_yaxes(title_text="Gross Sales ($ Millions USD)", secondary_y=True)
    apply_axes_style(fig_fc)
    st.plotly_chart(fig_fc, use_container_width=True, theme=None)

    # Monthly expansion preview
    st.markdown('<div class="sec-header">📅 Monthly Expansion Preview</div>', unsafe_allow_html=True)
    fc = st.session_state.forecast_df
    monthly_rows = []
    for _, row in fc.iterrows():
        profile = row.get("Monthly Profile", "Flat")
        w = MONTH_PROFILES.get(profile, MONTH_PROFILES["Flat"])
        ws = sum(w); w = [x/ws for x in w]
        for m_idx, mo in enumerate(MONTHS):
            monthly_rows.append({"Year": row["Year"], "Month": mo,
                                  "Units": row["Annual Units"]*w[m_idx],
                                  "Gross $M": row["Annual Units"]*w[m_idx]*row["WAC per Unit"]/1e6,
                                  "WAC": row["WAC per Unit"]})
    monthly_preview = pd.DataFrame(monthly_rows)

    fig_mo = go.Figure()
    for i, yr in enumerate(forecast_years):
        sub = monthly_preview[monthly_preview["Year"]==yr]
        fig_mo.add_trace(go.Bar(
            name=str(yr),
            x=[f"{yr}-{m}" for m in MONTHS],
            y=sub["Gross $M"],
            marker_color=COLORS_MAIN[i % len(COLORS_MAIN)],
            opacity=0.85,
        ))
    fig_mo.update_layout(title="Monthly Gross Sales ($M) — All Years",
                         barmode="group", height=280, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT, yaxis_title="Gross Sales ($ Millions USD)")
    apply_axes_style(fig_mo)
    st.plotly_chart(fig_mo, use_container_width=True, theme=None)

    # WAC trend
    st.markdown('<div class="sec-header">💲 WAC Trajectory</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        fig_wac = go.Figure()
        fig_wac.add_trace(go.Scatter(x=fc["Year"], y=fc["WAC per Unit"],
                                     mode="lines+markers+text",
                                     line=dict(color="#fbbf24", width=2.5),
                                     marker=dict(size=9, color="#fbbf24"),
                                     text=[f"${v:,.0f}" for v in fc["WAC per Unit"]],
                                     textposition="top center", textfont=dict(size=9),
                                     name="WAC"))
        wac_pcts = [(fc["WAC per Unit"].iloc[i]/fc["WAC per Unit"].iloc[i-1]-1)*100
                    if i>0 else 0 for i in range(len(fc))]
        fig_wac.add_trace(go.Bar(x=fc["Year"], y=wac_pcts, name="YoY % Increase",
                                  marker_color="#c084fc", opacity=0.5, yaxis="y2"))
        fig_wac.update_layout(title="WAC / Unit + Annual % Increase", height=260,
                               margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT, yaxis_title="WAC ($ / Unit)", yaxis2=dict(overlaying="y", side="right",
                               title="YoY Increase (%)", gridcolor="#003A8C"))
        apply_axes_style(fig_wac)
        st.plotly_chart(fig_wac, use_container_width=True, theme=None)
    with col_b:
        st.markdown("""<div class='info-box'>
        <b>WAC Considerations:</b><br>
        • IRA limits WAC increases to CPI-U for Medicare-negotiated drugs<br>
        • Increases above CPI-U trigger inflation rebate liability<br>
        • WAC changes flow directly into Medicaid AMP and rebate calculations<br>
        • ASP lags WAC changes by ~6 months due to reporting delay<br>
        • Model WAC realistically — aggressive increases increase liability
        </div>""", unsafe_allow_html=True)
        # Transposed: metrics as rows, years as columns
        yrs_str = [str(y) for y in fc["Year"]]
        summary_T = pd.DataFrame({
            "Metric": ["Units", "WAC/Unit", "Gross Sales"],
            **{yr: [fmt_u(u), fmt_d(w), fmt_m(g)]
               for yr, u, w, g in zip(yrs_str,
                                       fc["Annual Units"],
                                       fc["WAC per Unit"],
                                       gross_by_year)}
        })
        st.dataframe(summary_T, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 2 — CHANNEL ALLOCATION
# ═══════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## 🔀 Channel Allocation — Per Year")
    st.markdown("""<div class='info-box'>
    Channel mix evolves as the product matures: early years may be heavier on GPO/IDN and specialty;
    Medicare Part B share grows with patient age demographics; 340B mix can increase with hospital 
    consolidation. Edit any cell — rows must sum to 100%.
    </div>""", unsafe_allow_html=True)

    # ── Master channel list (built-in + any custom ones added) ────────
    CHANNEL_DESCRIPTIONS = {
        "Commercial PBM":    "Retail/specialty pharmacy benefit — large rebate driver",
        "Commercial Medical":"Provider buy-and-bill on commercial insurance",
        "Medicare Part B":   "Provider buy-and-bill billed to CMS at ASP+6%",
        "Medicare Part D":   "Pharmacy benefit for Medicare enrollees",
        "Medicaid FFS":      "State fee-for-service Medicaid — statutory rebates apply",
        "Managed Medicaid":  "MCO-managed Medicaid — supplemental rebates",
        "GPO/IDN Non-340B":  "Health system GPO contract price — chargeback driven",
        "GPO/IDN 340B":      "Covered entity 340B ceiling price — deepest discount",
        "VA/DoD/Federal":    "Federal Supply Schedule — FSS pricing required",
        "Cash/Uninsured":    "Out-of-pocket / patient assistance programs",
    }

    # Session state: full channel registry (built-in + custom)
    if "all_channels" not in st.session_state:
        st.session_state.all_channels = list(CHANNELS)

    # ── ⚙️ Customise Channels panel ───────────────────────────────────
    with st.expander("⚙️ Customise Channels — Toggle, Add Custom, Delete", expanded=False):

        # ── Part A: Add a custom channel ─────────────────────────────
        st.markdown('<div class="sec-header">➕ Add a Custom Channel</div>', unsafe_allow_html=True)
        st.caption("Add any payer segment not in the default list (e.g. a specific health plan, employer group, specialty pharmacy).")

        add_col1, add_col2, add_col3 = st.columns([2, 2, 1])
        with add_col1:
            new_ch_name = st.text_input("Channel Name", placeholder="e.g. Kaiser Permanente",
                                         key="new_ch_name", label_visibility="visible")
        with add_col2:
            new_ch_desc = st.text_input("Description (optional)",
                                         placeholder="e.g. Integrated health plan — West Coast",
                                         key="new_ch_desc", label_visibility="visible")
        with add_col3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("➕ Add Channel", use_container_width=True, key="btn_add_ch"):
                nm = new_ch_name.strip()
                if nm and nm not in st.session_state.all_channels:
                    st.session_state.all_channels.append(nm)
                    CHANNEL_DESCRIPTIONS[nm] = new_ch_desc.strip() or "Custom channel"
                    # Init its session-state steppers to 0
                    for yr in forecast_years:
                        k = f"ch_{nm}_{yr}".replace("/","_").replace(" ","_")
                        st.session_state[k] = 0.0
                    # Init toggle as active
                    # Use storage key (chtog_ prefix) not widget key
                    st.session_state[f"chtog_{nm.replace('/','_').replace(' ','_')}"] = True
                    # Add column to channel_alloc_raw
                    if nm not in st.session_state.channel_alloc_raw.columns:
                        st.session_state.channel_alloc_raw[nm] = 0.0
                    st.rerun()
                elif nm in st.session_state.all_channels:
                    st.warning(f"'{nm}' already exists.")
                else:
                    st.warning("Please enter a channel name.")

        st.markdown("---")

        # ── Part B: Toggle existing channels on/off ──────────────────
        st.markdown('<div class="sec-header">🔀 Show / Hide Channels</div>', unsafe_allow_html=True)
        st.caption("Toggle off channels not relevant to your product. They will be hidden from the grid immediately.")

        ALL_CH_NOW = st.session_state.all_channels

        # Storage keys use prefix "chtog_" (never bound to a widget directly)
        def _skey(ch):  # storage key — safe to read/write anytime
            return f"chtog_{ch.replace('/','_').replace(' ','_')}"

        # Init storage keys (done once, before any widget renders)
        for ch in ALL_CH_NOW:
            if _skey(ch) not in st.session_state:
                st.session_state[_skey(ch)] = True

        toggle_cols = st.columns(2)
        for idx, ch in enumerate(ALL_CH_NOW):
            is_active = st.session_state[_skey(ch)]

            with toggle_cols[idx % 2]:
                row_t = st.columns([0.55, 3, 1])
                with row_t[0]:
                    # Widget key is distinct from storage key — Streamlit owns it
                    new_val = st.toggle(
                        "on",
                        value=is_active,
                        key=f"chtog_w_{ch.replace('/','_').replace(' ','_')}",
                        label_visibility="collapsed",
                    )
                    # Write result back to storage key (widget key is not touched)
                    st.session_state[_skey(ch)] = new_val
                    # Zero steppers immediately when turned off
                    if not new_val:
                        for yr in forecast_years:
                            k = f"ch_{ch}_{yr}".replace("/","_").replace(" ","_")
                            st.session_state[k] = 0.0
                with row_t[1]:
                    border_c = "#0D2A56" if new_val else "#CCCCCC"
                    name_c   = "#0D2A56" if new_val else "#0D2A56"
                    desc_c   = "#444444"
                    st.markdown(
                        f"<div style='background:#FFFFFF;border:1px solid {border_c};"
                        f"border-radius:7px;padding:8px 12px;margin:2px 0;'>"
                        f"<div style='font-family:Syne;font-size:0.82rem;font-weight:700;"
                        f"color:{name_c};'>{ch}</div>"
                        f"<div style='font-size:0.69rem;color:{desc_c};margin-top:2px;'>"
                        f"{CHANNEL_DESCRIPTIONS.get(ch, 'Custom channel')}</div></div>",
                        unsafe_allow_html=True)
                with row_t[2]:
                    is_builtin = ch in CHANNELS
                    if not is_builtin:
                        if st.button("🗑️", key=f"del_ch_{idx}",
                                     help=f"Delete '{ch}'",
                                     use_container_width=True):
                            st.session_state.all_channels.remove(ch)
                            for yr in forecast_years:
                                st.session_state.pop(
                                    f"ch_{ch}_{yr}".replace("/","_").replace(" ","_"), None)
                            st.session_state.pop(_skey(ch), None)
                            if ch in st.session_state.channel_alloc_raw.columns:
                                st.session_state.channel_alloc_raw.drop(
                                    columns=[ch], inplace=True)
                            st.rerun()
                    else:
                        st.markdown(
                            "<div style='font-size:0.7rem;color:#0D2A56;"
                            "text-align:center;padding-top:8px;'>built-in</div>",
                            unsafe_allow_html=True)

        n_active_now = sum(
            1 for ch in ALL_CH_NOW if st.session_state.get(_skey(ch), True)
        )
        st.markdown(
            f"<div style='font-size:0.75rem;color:#0D2A56;margin-top:10px;'>"
            f"<b style='color:#0D2A56;'>{n_active_now}</b> of "
            f"<b style='color:#0D2A56;'>{len(ALL_CH_NOW)}</b> channels active "
            f"({len(ALL_CH_NOW) - len(CHANNELS)} custom)</div>",
            unsafe_allow_html=True)

        if st.button("🔄 Re-enable All Channels", key="ch_reset_all"):
            for ch in st.session_state.all_channels:
                st.session_state[_skey(ch)] = True
            st.rerun()

    # ── Resolve ACTIVE_CH from storage keys (never from widget keys) ──
    def _skey(ch):
        return f"chtog_{ch.replace('/','_').replace(' ','_')}"

    ALL_CH_NOW = st.session_state.all_channels
    ACTIVE_CH = [
        ch for ch in ALL_CH_NOW
        if st.session_state.get(_skey(ch), True)
    ]
    if not ACTIVE_CH:
        st.warning("No channels are active — re-enable at least one in Customise above.")
        ACTIVE_CH = list(CHANNELS)

    st.markdown('<div class="sec-header">📥 Channel Mix % by Year (Editable)</div>', unsafe_allow_html=True)
    st.caption("⚠️ Each row must sum to 100%. The app will flag rows that don't.")

    # Sync years if changed
    existing_years = list(st.session_state.channel_alloc_raw["Year"])
    if set(existing_years) != set(forecast_years):
        current = st.session_state.channel_alloc_raw.set_index("Year")
        rows = []
        for yr in forecast_years:
            if yr in current.index:
                row = {"Year": yr}; row.update(current.loc[yr].to_dict()); rows.append(row)
            else:
                base = {"Year": yr, "Commercial PBM": 25, "Commercial Medical": 18,
                        "Medicare Part B": 16, "Medicare Part D": 12, "Medicaid FFS": 8,
                        "Managed Medicaid": 6, "GPO/IDN Non-340B": 7, "GPO/IDN 340B": 4,
                        "VA/DoD/Federal": 2, "Cash/Uninsured": 2}
                rows.append(base)
        st.session_state.channel_alloc_raw = pd.DataFrame(rows)

    # ── Init session state for ALL channel steppers (built-in + custom) ──
    ch_src = st.session_state.channel_alloc_raw.set_index("Year")
    for yr in forecast_years:
        for ch in ALL_CH_NOW:
            key = f"ch_{ch}_{yr}".replace("/","_").replace(" ","_")
            if key not in st.session_state:
                val = 0.0
                if yr in ch_src.index and ch in ch_src.columns:
                    val = float(ch_src.loc[yr, ch])
                elif ch in CHANNELS:
                    val = 5.0
                st.session_state[key] = val

    # ── Transposed stepper grid: rows = active channels only ──
    st.caption(f"Use ＋/－ buttons or type directly. Showing {len(ACTIVE_CH)} of {len(ALL_CH_NOW)} channels active. Each year column must sum to 100%.")

    # Header row: year labels
    hdr_cols = st.columns([2] + [1]*len(forecast_years))
    hdr_cols[0].markdown(
        "<div style='font-size:0.72rem;color:#0D2A56;text-transform:uppercase;"
        "letter-spacing:0.5px;padding:6px 0;font-family:JetBrains Mono;'>Channel</div>",
        unsafe_allow_html=True)
    for j, yr in enumerate(forecast_years):
        hdr_cols[j+1].markdown(
            f"<div style='font-size:0.8rem;font-weight:700;color:#0D2A56;"
            f"text-align:center;padding:6px 0;font-family:Syne;'>{yr}</div>",
            unsafe_allow_html=True)

    ch_values = {yr: {ch: 0.0 for ch in ALL_CH_NOW} for yr in forecast_years}  # all channels incl. custom
    for ch in ACTIVE_CH:
        row_cols = st.columns([2] + [1]*len(forecast_years))
        row_cols[0].markdown(
            f"<div style='font-size:0.75rem;color:#0D2A56;padding:8px 4px;line-height:1.3;'>{ch}</div>",
            unsafe_allow_html=True)
        for j, yr in enumerate(forecast_years):
            key = f"ch_{ch}_{yr}".replace("/","_").replace(" ","_")
            val = row_cols[j+1].number_input(
                f"{ch}_{yr}", label_visibility="collapsed",
                min_value=0.0, max_value=100.0,
                value=st.session_state[key],
                step=0.5, format="%.1f",
                key=f"ni_{key}",
            )
            st.session_state[key] = val
            ch_values[yr][ch] = val
        # Inactive channels stay 0 (already initialised above)

    # Validation row — show sum of ACTIVE channels per year
    val_cols = st.columns([2] + [1]*len(forecast_years))
    val_cols[0].markdown(
        "<div style='font-size:0.72rem;color:#FFFFFF;padding:6px 4px;"
        "font-family:JetBrains Mono;'>Σ Total %</div>",
        unsafe_allow_html=True)
    all_valid = True
    for j, yr in enumerate(forecast_years):
        yr_sum = sum(ch_values[yr][ch] for ch in ACTIVE_CH)
        ok = abs(yr_sum - 100) < 0.6
        if not ok: all_valid = False
        color = "#4ade80" if ok else "#f87171"
        val_cols[j+1].markdown(
            f"<div style='text-align:center;font-family:JetBrains Mono;font-size:0.8rem;"
            f"font-weight:700;color:{color};padding:4px 0;'>{yr_sum:.1f}%</div>",
            unsafe_allow_html=True)

    if all_valid:
        st.markdown("<div class='card card-success' style='padding:8px 14px;'>✅ All years sum to ~100% — allocation valid.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='card card-warn' style='padding:8px 14px;'>⚠️ One or more years don't sum to 100% — check red totals above.</div>", unsafe_allow_html=True)

    # Rebuild channel_alloc_raw from steppers (all channels incl. custom, inactive = 0)
    ch_rows = []
    for yr in forecast_years:
        row = {"Year": yr}
        row.update(ch_values[yr])
        # Ensure every built-in CHANNEL col exists (for downstream compatibility)
        for ch in CHANNELS:
            if ch not in row:
                row[ch] = 0.0
        ch_rows.append(row)
    ch_edited_df = pd.DataFrame(ch_rows)
    st.session_state.channel_alloc_raw = ch_edited_df
    ch_edited = ch_edited_df

    # Stacked area chart — only active channels
    st.markdown('<div class="sec-header">📊 Channel Mix Evolution (Area Chart)</div>', unsafe_allow_html=True)
    fig_ch = go.Figure()
    for i, ch in enumerate(ACTIVE_CH):
        orig_i = CHANNELS.index(ch) if ch in CHANNELS else i
        fig_ch.add_trace(go.Scatter(
            x=ch_edited["Year"], y=ch_edited[ch],
            name=ch, stackgroup="one", mode="none",
            fillcolor=hex_to_rgba(COLORS_MAIN[orig_i % len(COLORS_MAIN)], alpha=0.73),
            hovertemplate=f"<b>{ch}</b><br>%{{y:.1f}}%<extra></extra>",
        ))
    fig_ch.update_layout(title="Payer Channel Mix % by Year", height=350, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
                         yaxis_title="Channel Allocation Share (%)")
    apply_axes_style(fig_ch)
    st.plotly_chart(fig_ch, use_container_width=True, theme=None)

    # Per-year pie grid — active channels only
    st.markdown('<div class="sec-header">🥧 Channel Mix Snapshots</div>', unsafe_allow_html=True)
    display_years = ch_edited["Year"].tolist()[:6]
    cols = st.columns(min(len(display_years), 3))
    pie_colors = [COLORS_MAIN[CHANNELS.index(ch) % len(COLORS_MAIN)] for ch in ACTIVE_CH]
    for idx, yr in enumerate(display_years[:6]):
        row = ch_edited[ch_edited["Year"] == yr].iloc[0]
        vals = [row[ch] for ch in ACTIVE_CH]
        fig_p = go.Figure(go.Pie(
            labels=ACTIVE_CH, values=vals, hole=0.4,
            marker_colors=pie_colors, textfont=dict(size=8, color="#1A1A2E"),
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
        ))
        fig_p.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#1A1A2E",
                            height=220, margin=dict(t=30, b=10, l=5, r=5),
                            title=str(yr), title_font=dict(size=13, color="#0D2A56"),
                            showlegend=False)
        with cols[idx % 3]:
            st.plotly_chart(fig_p, use_container_width=True, theme=None)


# ═══════════════════════════════════════════════════════════════════
# TAB 3 — CONTRACT TERMS
# ═══════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("## 📋 Contract Terms — Per Year")
    st.markdown("""<div class='info-box'>
    Rebates, discounts, and fees can all change year-over-year as contracts renew, formulary tiers shift, 
    or Medicaid supplemental agreements evolve. Enter the effective rate for each year. 
    Missing years inherit the nearest prior year's rates.
    </div>""", unsafe_allow_html=True)

    # Sync years
    def sync_df(df_key, template_fn):
        existing = set(st.session_state[df_key]["Year"])
        needed   = set(forecast_years)
        if existing != needed:
            current = st.session_state[df_key].set_index("Year")
            rows = []
            for yr in forecast_years:
                if yr in current.index:
                    row = {"Year": yr}; row.update(current.loc[yr].to_dict()); rows.append(row)
                else:
                    rows.append(template_fn(yr))
            st.session_state[df_key] = pd.DataFrame(rows)

    def disc_template(yr):
        return {"Year": yr, "GPO Disc %": 14.0, "IDN Disc %": 20.0, "340B Disc %": 25.6, "VA FSS Disc %": 24.0}

    def rebate_template(yr):
        return {"Year": yr, "Com PBM %": 32.0, "Com Med %": 13.0,
                "Mcr Part D %": 28.0, "Medicaid FFS %": 23.1, "Managed Mcaid %": 42.0}

    def other_template(yr):
        return {"Year": yr, "Admin Fee %": 2.0, "Dist Fee %": 2.0, "Copay Support %": 3.5, "Returns %": 1.5}

    sync_df("discount_raw", disc_template)
    sync_df("rebate_raw",   rebate_template)
    sync_df("other_raw",    other_template)

    # ─────────────────────────────────────────────────────────────────
    # Full-width stepper: one metric per row, year values as columns.
    # Each year gets a fixed pixel-width number_input via CSS injection.
    # ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Contract-terms: palette overrides for light theme */
    [data-testid="stNumberInput"] input {
        min-width: 72px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-align: center !important;
        color: #0D2A56 !important;
        background: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
    }
    .ct-section-bg {
        background: #FFFFFF;
        border: 1px solid #E0E6F3;
        border-radius: 10px;
        padding: 14px 18px 10px 18px;
        margin-bottom: 16px;
    }
    .ct-year-hdr {
        font-family: 'Syne', sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        color: #1f4e79;
        text-align: center;
        padding: 4px 0 6px 0;
        border-bottom: 2px solid #B6D6F5;
        margin-bottom: 4px;
    }
    .ct-metric-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #1f4e79;
        padding: 9px 4px 4px 4px;
        white-space: nowrap;
    }
    .ct-caption {
        font-size: 0.73rem;
        color: #333333;
        font-style: italic;
        margin-bottom: 8px;
    }
    </style>""", unsafe_allow_html=True)

    def render_full_width_table(section_title, caption_text, fields, ss_key, ss_prefix,
                                min_v=0.0, max_v=100.0, step=0.5, fmt="%.1f"):
        """
        Full-width transposed stepper.
        - metric label column is fixed wider
        - year columns share remaining space equally
        - no 50% width constraint — uses the full page
        """
        st.markdown(f'<div class="sec-header">{section_title}</div>', unsafe_allow_html=True)
        if caption_text:
            st.markdown(f"<div class='ct-caption'>{caption_text}</div>", unsafe_allow_html=True)

        # Init session state from stored df
        src_df = st.session_state[ss_key].set_index("Year")                  if "Year" in st.session_state[ss_key].columns else st.session_state[ss_key]
        for yr in forecast_years:
            for disp, col in fields:
                k = f"{ss_prefix}_{col}_{yr}"
                if k not in st.session_state:
                    st.session_state[k] = float(src_df.loc[yr, col])                                           if yr in src_df.index else 0.0

        # Label column width scales with number of years so numbers stay large
        n_yr    = len(forecast_years)
        lbl_w   = max(1.4, 10.0 / n_yr)   # shrinks gracefully as years grow
        col_w   = [lbl_w] + [1.0] * n_yr

        # Header row
        hdr_cols = st.columns(col_w)
        hdr_cols[0].markdown("<div class='ct-metric-lbl' style='color:#FFFFFF;'>Metric</div>",
                              unsafe_allow_html=True)
        for j, yr in enumerate(forecast_years):
            hdr_cols[j+1].markdown(f"<div class='ct-year-hdr'>{yr}</div>",
                                    unsafe_allow_html=True)

        result = {yr: {} for yr in forecast_years}
        for disp, col in fields:
            data_cols = st.columns(col_w)
            data_cols[0].markdown(f"<div class='ct-metric-lbl'>{disp}</div>",
                                   unsafe_allow_html=True)
            for j, yr in enumerate(forecast_years):
                k = f"{ss_prefix}_{col}_{yr}"
                v = data_cols[j+1].number_input(
                    label=f"{col}_{yr}",
                    label_visibility="collapsed",
                    min_value=min_v, max_value=max_v,
                    value=float(st.session_state[k]),
                    step=step, format=fmt,
                    key=f"ni_{k}",
                )
                st.session_state[k] = v
                result[yr][col] = v

        rebuilt_rows = [{"Year": yr, **result[yr]} for yr in forecast_years]
        rebuilt = pd.DataFrame(rebuilt_rows)
        st.session_state[ss_key] = rebuilt
        return rebuilt

    # ── Section 1: Discounts ─────────────────────────────────────────
    st.markdown("<div class='ct-section-bg'>", unsafe_allow_html=True)
    disc_fields = [
        ("GPO Disc %",    "GPO Disc %"),
        ("IDN Disc %",    "IDN Disc %"),
        ("340B Disc %",   "340B Disc %"),
        ("VA FSS Disc %", "VA FSS Disc %"),
    ]
    disc_edited = render_full_width_table(
        "🏷️ Discounts / Chargebacks (% off WAC)",
        "Applied at point of sale — drives chargeback = WAC − contract price",
        disc_fields, "discount_raw", "disc", min_v=0.0, max_v=99.0, step=0.5, fmt="%.1f"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 2: Rebates ───────────────────────────────────────────
    st.markdown("<div class='ct-section-bg'>", unsafe_allow_html=True)
    rebate_fields = [
        ("Com PBM %",       "Com PBM %"),
        ("Com Med %",       "Com Med %"),
        ("Mcr Part D %",    "Mcr Part D %"),
        ("Medicaid FFS %",  "Medicaid FFS %"),
        ("Managed Mcaid %", "Managed Mcaid %"),
    ]
    rebate_edited = render_full_width_table(
        "📊 Rebates by Channel (% of Gross at WAC)",
        "Post-sale rebates paid to PBMs, plans, states — largest GTN component",
        rebate_fields, "rebate_raw", "reb", min_v=0.0, max_v=100.0, step=0.5, fmt="%.1f"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 3: Fees ──────────────────────────────────────────────
    st.markdown("<div class='ct-section-bg'>", unsafe_allow_html=True)
    other_fields = [
        ("Admin Fee %",     "Admin Fee %"),
        ("Dist Fee %",      "Dist Fee %"),
        ("Copay Support %", "Copay Support %"),
        ("Returns %",       "Returns %"),
    ]
    render_full_width_table(
        "💰 Fees & Other Deductions (% of Gross Sales)",
        "Distribution, admin, copay programs, and returns",
        other_fields, "other_raw", "oth", min_v=0.0, max_v=20.0, step=0.1, fmt="%.1f"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Trend charts — full width side by side ───────────────────────
    st.markdown('<div class="sec-header">📈 Trend Charts</div>', unsafe_allow_html=True)
    ch_trend1, ch_trend2 = st.columns(2)

    with ch_trend1:
        fig_reb = go.Figure()
        for i, col in enumerate(["Com PBM %","Com Med %","Mcr Part D %","Managed Mcaid %"]):
            fig_reb.add_trace(go.Scatter(
                x=rebate_edited["Year"], y=rebate_edited[col],
                name=col.replace(" %",""), mode="lines+markers",
                line=dict(color=COLORS_MAIN[i], width=2), marker=dict(size=6),
            ))
        fig_reb.update_layout(title="Rebate Rates Over Forecast Period", height=280,
                               margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
                               yaxis_title="Rebate Percentage (%)", legend_font_size=10)
        apply_axes_style(fig_reb)
        st.plotly_chart(fig_reb, use_container_width=True, theme=None)

    with ch_trend2:
        fig_disc = go.Figure()
        for i, col in enumerate(["GPO Disc %","IDN Disc %","340B Disc %","VA FSS Disc %"]):
            fig_disc.add_trace(go.Scatter(
                x=disc_edited["Year"], y=disc_edited[col],
                name=col.replace(" %",""), mode="lines+markers",
                line=dict(color=COLORS_MAIN[i+4], width=2, dash="dash"),
                marker=dict(size=6),
            ))
        fig_disc.update_layout(title="Discount Rates (Off WAC) Over Forecast Period", height=280,
                               margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
                               yaxis_title="Discount Percentage (%)", legend_font_size=10)
        apply_axes_style(fig_disc)
        st.plotly_chart(fig_disc, use_container_width=True, theme=None)

    st.markdown('<div class="sec-header">📉 Effective GTN % Preview (Rebates + Discounts Blended)</div>', unsafe_allow_html=True)
    # Quick blended GTN preview
    ch_df  = st.session_state.channel_alloc_raw.set_index("Year")
    reb_df = st.session_state.rebate_raw.set_index("Year")
    disc_df = st.session_state.discount_raw.set_index("Year")
    oth_df  = st.session_state.other_raw.set_index("Year")
    blended_gtn = []
    for yr in forecast_years:
        alloc = ch_df.loc[yr] if yr in ch_df.index else ch_df.iloc[-1]
        reb   = reb_df.loc[yr] if yr in reb_df.index else reb_df.iloc[-1]
        disc  = disc_df.loc[yr] if yr in disc_df.index else disc_df.iloc[-1]
        oth   = oth_df.loc[yr] if yr in oth_df.index else oth_df.iloc[-1]
        # rebate contribution
        r = (alloc["Commercial PBM"]*reb["Com PBM %"] + alloc["Commercial Medical"]*reb["Com Med %"] +
             alloc["Medicare Part D"]*reb["Mcr Part D %"] + alloc["Medicaid FFS"]*reb["Medicaid FFS %"] +
             alloc["Managed Medicaid"]*reb["Managed Mcaid %"]) / 100
        # chargeback contribution
        c = (alloc["GPO/IDN Non-340B"]*disc["IDN Disc %"] + alloc["GPO/IDN 340B"]*disc["340B Disc %"] +
             alloc["VA/DoD/Federal"]*disc["VA FSS Disc %"]) / 100
        # other
        o = oth["Admin Fee %"] + oth["Dist Fee %"] + oth["Copay Support %"] + oth["Returns %"]
        blended_gtn.append({"Year": yr, "Rebates": r, "Chargebacks": c, "Other": o, "Total GTN": r+c+o})

    gtn_prev = pd.DataFrame(blended_gtn)
    fig_gtn_prev = go.Figure()
    for col, color in [("Rebates","#f87171"),("Chargebacks","#fb923c"),("Other","#fbbf24")]:
        fig_gtn_prev.add_trace(go.Bar(x=gtn_prev["Year"], y=gtn_prev[col],
                                       name=col, marker_color=color, opacity=0.8))
    fig_gtn_prev.add_trace(go.Scatter(x=gtn_prev["Year"], y=gtn_prev["Total GTN"],
                                       name="Total GTN %", mode="lines+markers+text",
                                       line=dict(color="#A8D5FF", width=2.5),
                                       text=[f"{v:.1f}%" for v in gtn_prev["Total GTN"]],
                                       textposition="top center", textfont=dict(size=9, color="#1A1A2E"),
                                       marker=dict(size=8), yaxis="y"))
    fig_gtn_prev.update_layout(barmode="stack", title="Blended GTN % by Year (Indicative)",
                                height=280, **PLOTLY_LAYOUT, yaxis_title="Gross-To-Net Yield (%)",
                                legend_font_size=10)
    apply_axes_style(fig_gtn_prev)
    st.plotly_chart(fig_gtn_prev, use_container_width=True, theme=None)


# ═══════════════════════════════════════════════════════════════════
# TAB 4 — ASP ENGINE
# ═══════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("## 📐 ASP Engine — 6-Month Rolling Weighted Average")
    st.markdown("""<div class='asp-box'>
    <b>ASP Calculation Methodology (per CMS 42 CFR § 414.804):</b><br><br>
    ASP = Σ(Net Sales Price<sub>i</sub> × Units<sub>i</sub>) / Σ(Units<sub>i</sub>) 
    across all <b>non-exempt</b> purchasers, computed quarterly over a 6-month window.<br><br>
    <b>Exempt from ASP calculation:</b> 340B ceiling price sales · VA/Big4 pricing · Medicaid nominal prices 
    · Samples · Free goods · Patient assistance<br>
    <b>Included in ASP:</b> Commercial (medical & pharmacy) · Medicare Part D · GPO/IDN non-340B · Cash<br><br>
    <b>Reporting lag:</b> ASP reported quarterly with approximately a 2-quarter lag. 
    Medicare reimburses at ASP + 6% (effectively ASP + 3.8% post-sequestration).
    </div>""", unsafe_allow_html=True)

    # Build lookup dicts from edited tables
    fc = st.session_state.forecast_df
    ch_alloc_dict = {}
    disc_dict     = {}
    rebate_dict   = {}
    other_dict    = {}

    ch_raw  = st.session_state.channel_alloc_raw.set_index("Year")
    dis_raw = st.session_state.discount_raw.set_index("Year")
    reb_raw = st.session_state.rebate_raw.set_index("Year")
    oth_raw = st.session_state.other_raw.set_index("Year")

    for yr in forecast_years:
        row_ch  = ch_raw.loc[yr]  if yr in ch_raw.index  else ch_raw.iloc[-1]
        row_dis = dis_raw.loc[yr] if yr in dis_raw.index else dis_raw.iloc[-1]
        row_reb = reb_raw.loc[yr] if yr in reb_raw.index else reb_raw.iloc[-1]
        row_oth = oth_raw.loc[yr] if yr in oth_raw.index else oth_raw.iloc[-1]
        ch_alloc_dict[yr] = {ch: float(row_ch[ch]) for ch in CHANNELS}
        disc_dict[yr]     = {"gpo": float(row_dis["GPO Disc %"]), "idn": float(row_dis["IDN Disc %"]),
                             "b340": float(row_dis["340B Disc %"]), "va": float(row_dis["VA FSS Disc %"])}
        rebate_dict[yr]   = {"com_pbm": float(row_reb["Com PBM %"]), "com_med": float(row_reb["Com Med %"]),
                             "mcr_d": float(row_reb["Mcr Part D %"]), "mcaid": float(row_reb["Medicaid FFS %"]),
                             "man_mcaid": float(row_reb["Managed Mcaid %"])}
        other_dict[yr]    = {"admin_fee": float(row_oth["Admin Fee %"]), "dist_fee": float(row_oth["Dist Fee %"]),
                             "copay": float(row_oth["Copay Support %"]), "returns": float(row_oth["Returns %"])}

    # Monthly expansion
    monthly_all = []
    for _, row in fc.iterrows():
        profile = row.get("Monthly Profile", "Flat")
        w = MONTH_PROFILES.get(profile, MONTH_PROFILES["Flat"])
        ws = sum(w); w = [x/ws for x in w]
        for m_idx, mo in enumerate(MONTHS):
            monthly_all.append({"Year": row["Year"], "Month": mo, "MonthIdx": m_idx+1,
                                 "Period": f"{row['Year']}-{mo}",
                                 "Units": row["Annual Units"]*w[m_idx],
                                 "WAC": row["WAC per Unit"]})
    monthly_df = pd.DataFrame(monthly_all)

    # Compute ASP series
    asp_df = compute_asp_series(monthly_df, ch_alloc_dict, disc_dict)
    # Store in session state for Tab 5 & 6
    st.session_state["asp_df"] = asp_df
    st.session_state["monthly_df"] = monthly_df
    st.session_state["ch_alloc_dict"] = ch_alloc_dict
    st.session_state["disc_dict"] = disc_dict
    st.session_state["rebate_dict"] = rebate_dict
    st.session_state["other_dict"] = other_dict

    # ── Charts ──
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="sec-header">📈 Rolling 6-Month ASP vs WAC (Monthly)</div>', unsafe_allow_html=True)
        fig_asp = go.Figure()
        fig_asp.add_trace(go.Scatter(x=asp_df["Period"], y=asp_df["WAC"],
                                     name="WAC", mode="lines",
                                     line=dict(color="#fbbf24", width=1.5, dash="dot")))
        fig_asp.add_trace(go.Scatter(x=asp_df["Period"], y=asp_df["MonthlyASP"],
                                     name="Monthly ASP (raw)", mode="lines",
                                     line=dict(color="#c084fc", width=1, dash="dash"), opacity=0.7))
        fig_asp.add_trace(go.Scatter(x=asp_df["Period"], y=asp_df["RollingASP_6M"],
                                     name="6-Month Rolling ASP", mode="lines",
                                     line=dict(color="#4ade80", width=2.5)))
        fig_asp.add_trace(go.Scatter(x=asp_df["Period"], y=asp_df["ASP_Plus6"],
                                     name="ASP + 6% (Medicare Reimb.)", mode="lines",
                                     line=dict(color="#A8D5FF", width=2)))
        # Shade year boundaries (add_vline fails on string x-axes; use add_shape instead)
        for yr in forecast_years[1:]:
            x_val = f"{yr}-Jan"
            fig_asp.add_shape(type="line", x0=x_val, x1=x_val, y0=0, y1=1,
                              xref="x", yref="paper",
                              line=dict(color="#003A8C", width=1, dash="dot"))
            fig_asp.add_annotation(x=x_val, y=1.02, xref="x", yref="paper",
                                   text=str(yr), showarrow=False,
                                   font=dict(color="#4A5568", size=10))
        fig_asp.update_layout(title="ASP Trend — Rolling 6-Month Weighted Average",
                               height=340, **PLOTLY_LAYOUT, yaxis_title="Price ($ / Unit)",
                               xaxis_tickangle=-45, xaxis_nticks=n_years*2)
        apply_axes_style(fig_asp)
        st.plotly_chart(fig_asp, use_container_width=True, theme=None)

    with col2:
        st.markdown('<div class="sec-header">📊 Annual ASP Summary</div>', unsafe_allow_html=True)
        asp_annual = asp_df.groupby("Year").agg(
            Avg_WAC=("WAC","mean"),
            Avg_ASP=("RollingASP_6M","mean"),
            Avg_ASP6=("ASP_Plus6","mean"),
            ASP_as_WAC=("RollingASP_6M", lambda x: (x / asp_df.loc[x.index,"WAC"]).mean() * 100),
        ).reset_index()

        fig_ann = go.Figure()
        fig_ann.add_trace(go.Bar(x=asp_annual["Year"], y=asp_annual["Avg_WAC"],
                                  name="Avg WAC", marker_color="#fbbf24", opacity=0.7))
        fig_ann.add_trace(go.Bar(x=asp_annual["Year"], y=asp_annual["Avg_ASP"],
                                  name="Avg 6M ASP", marker_color="#4ade80", opacity=0.8))
        fig_ann.add_trace(go.Bar(x=asp_annual["Year"], y=asp_annual["Avg_ASP6"],
                                  name="Avg ASP+6%", marker_color="#A8D5FF", opacity=0.8))
        fig_ann.update_layout(barmode="group", title="Annual Average Prices", height=260,
                               **PLOTLY_LAYOUT, yaxis_title="Price ($ / Unit)")
        apply_axes_style(fig_ann)
        st.plotly_chart(fig_ann, use_container_width=True, theme=None)

        # Transposed: metrics as rows, years as columns
        asp_yrs = asp_annual["Year"].tolist()
        asp_T = pd.DataFrame({
            "Metric": ["Avg WAC", "6M Avg ASP", "ASP+6%", "ASP/WAC %"],
            **{yr: [
                fmt_d(row["Avg_WAC"]),
                fmt_d(row["Avg_ASP"]),
                fmt_d(row["Avg_ASP6"]),
                fmt_pct(row["ASP_as_WAC"]),
            ] for yr, row in zip(asp_yrs, asp_annual.to_dict("records"))}
        })
        st.dataframe(asp_T, use_container_width=True, hide_index=True)

    # ASP methodology explainer
    st.markdown('<div class="sec-header">⚙️ ASP Calculation Step-by-Step</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        html_a = """
        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 16px rgba(0,0,0,0.04); height: 100%; display: flex; flex-direction: column;'>
            <div style='font-family: "Inter", -apple-system, sans-serif; font-size: 1.15rem; font-weight: 800; color: #1E293B; margin-bottom: 20px; border-bottom: 2px solid #F1F5F9; padding-bottom: 12px;'>
                Step 1 — Identify ASP-Eligible Channels
            </div>
            <div style='display: grid; gap: 10px; flex-grow: 1;'>
        """
        for ch, eligible in ASP_ELIGIBLE.items():
            if eligible:
                badge_bg = "#DCFCE7"
                badge_color = "#166534"
                icon = "✓"
                text = "Included"
                border_left = "4px solid #22C55E"
            else:
                badge_bg = "#FEE2E2"
                badge_color = "#991B1B"
                icon = "✕"
                text = "Exempt"
                border_left = "4px solid #EF4444"
            html_a += f"""
                <div style='display: flex; justify-content: space-between; align-items: center; background: #F8FAFC; padding: 12px 16px; border-radius: 8px; border-left: {border_left}; border-right: 1px solid #E2E8F0; border-top: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; box-shadow: 0 1px 2px rgba(0,0,0,0.02);'>
                    <span style='font-family: "Inter", -apple-system, sans-serif; font-size: 0.95rem; font-weight: 600; color: #334155;'>{ch}</span>
                    <span style='background: {badge_bg}; color: {badge_color}; padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; font-family: "JetBrains Mono", monospace; letter-spacing: 0.5px; display: flex; align-items: center; gap: 4px;'>
                        <span style='font-size: 14px; margin-top: -1px;'>{icon}</span> {text}
                    </span>
                </div>
            """
        html_a += "</div></div>"
        st.markdown("\n".join(line.lstrip() for line in html_a.split("\n")), unsafe_allow_html=True)

    with col_b:
        html_b = """
        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 16px rgba(0,0,0,0.04); height: 100%; display: flex; flex-direction: column;'>
            <div style='font-family: "Inter", -apple-system, sans-serif; font-size: 1.15rem; font-weight: 800; color: #1E293B; margin-bottom: 20px; border-bottom: 2px solid #F1F5F9; padding-bottom: 12px;'>
                ASP Mathematical Engine
            </div>
            
            <div style='margin-bottom: 20px;'>
                <div style='font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>Step 2 — Monthly ASP Computation</div>
                <div style='background: #F0F9FF; border-left: 3px solid #0EA5E9; border-radius: 0 8px 8px 0; padding: 12px 16px;'>
                    <code style='color: #0369A1; background: transparent; padding: 0; font-family: "JetBrains Mono", monospace; font-size: 0.85rem; font-weight: 700;'>ASP_t = Σ(price_i × units_i) / Σ(units_i)</code>
                    <div style='font-size: 0.8rem; color: #475569; margin-top: 6px; font-style: italic;'>where <b>i</b> = non-exempt channels only</div>
                </div>
            </div>

            <div style='margin-bottom: 20px;'>
                <div style='font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>Step 3 — Rolling 6-Month Average</div>
                <div style='background: #F0F9FF; border-left: 3px solid #0EA5E9; border-radius: 0 8px 8px 0; padding: 12px 16px;'>
                    <code style='color: #0369A1; background: transparent; padding: 0; font-family: "JetBrains Mono", monospace; font-size: 0.85rem; font-weight: 700;'>ASP_rolling = Σ(rev_{t-5..t}) / Σ(units_{t-5..t})</code>
                    <div style='font-size: 0.8rem; color: #475569; margin-top: 6px; font-style: italic;'>Volume-weighted over the prior 6 months.</div>
                </div>
            </div>

            <div style='margin-bottom: 24px;'>
                <div style='font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>Step 4 — Medicare Reimbursement</div>
                <div style='background: #F0FDF4; border-left: 3px solid #22C55E; border-radius: 0 8px 8px 0; padding: 12px 16px;'>
                    <code style='color: #166534; background: transparent; padding: 0; font-family: "JetBrains Mono", monospace; font-size: 0.85rem; font-weight: 700;'>Medicare B Reimb = ASP_rolling × 1.06</code>
                    <div style='font-size: 0.8rem; color: #15803D; margin-top: 6px;'>Statutory <b>ASP + 6%</b> mark-up for providers.</div>
                </div>
            </div>
            
            <div style='margin-top: auto; background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 8px; padding: 16px; display: flex; gap: 12px; align-items: flex-start;'>
                <div style='font-size: 1.4rem; line-height: 1;'>⏳</div>
                <div>
                    <div style='font-size: 0.82rem; font-weight: 700; color: #92400E; margin-bottom: 2px;'>Step 5 — Reporting Lag</div>
                    <div style='font-size: 0.78rem; color: #B45309; line-height: 1.4;'>ASP is published ~2 quarters after the reference period. Model uses concurrent ASP for simplification.</div>
                </div>
            </div>
        </div>
        """
        st.markdown("\n".join(line.lstrip() for line in html_b.split("\n")), unsafe_allow_html=True)

    # Monthly ASP detail table — transposed: metrics as rows, months as columns
    st.markdown('<div class="sec-header">📋 Monthly ASP Detail (Sample — First Year)</div>', unsafe_allow_html=True)
    yr_asp_sel = st.selectbox("Select Year for ASP Detail", forecast_years, key="asp_yr_sel")
    asp_sub = asp_df[asp_df["Year"] == yr_asp_sel].copy()
    mo_labels = asp_sub["Month"].tolist()
    asp_T = pd.DataFrame({
        "Metric": ["Monthly ASP", "6M Rolling ASP", "ASP+6%", "WAC", "Eligible Units", "Total Units", "ASP/WAC %"],
        **{mo: [
            fmt_d(row["MonthlyASP"]),
            fmt_d(row["RollingASP_6M"]),
            fmt_d(row["ASP_Plus6"]),
            fmt_d(row["WAC"]),
            fmt_u(row["EligibleUnits"]),
            fmt_u(row["TotalUnits"]),
            fmt_pct(row["RollingASP_6M"] / row["WAC"] * 100),
        ] for mo, row in zip(mo_labels, asp_sub.to_dict("records"))}
    })
    st.dataframe(asp_T, use_container_width=True, hide_index=True)


    # ═══════════════════════════════════════════════════════════════
    # ASP RISK STRESS TEST
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1a0505 0%,#0a0515 100%);
    border:1px solid #b02a2a;border-radius:12px;padding:16px 22px;margin:8px 0;'>
    <div style='font-family:Syne;font-weight:800;font-size:1.1rem;color:#FFFFFF;margin-bottom:6px;'>
    🔴 ASP Risk Stress Test — When Does ASP Enter the Danger Zone?</div>
    <div style='font-size:0.82rem;color:#FFFFFF;line-height:1.6;'>
    Use these levers to <b>stress ASP downward</b> and identify the tipping point where
    it falls below the IDN acquisition floor. Each lever reflects a real-world
    market access risk: deep discounting, channel mix erosion, 340B expansion, or
    growing Medicare Part B exposure at suppressed prices.
    <br><br>
    <b style='color:#FFFFFF;'>Risk signals:</b>
    Increasing GPO/IDN discounts · Shifting mix toward deeply discounted channels ·
    340B covered entity volume growth · WAC price increases that lag ASP (IRA caps)
    </div></div>""", unsafe_allow_html=True)

    # Resolve IDN list and baseline values for the stress test
    idn_list_stress = st.session_state.get("idn_list", [
        {"name": "IDN-A", "discount": 20.0, "volume_pct": 30.0, "is_340b": False}
    ])
    wac_base   = float(st.session_state.forecast_df["WAC per Unit"].iloc[0])
    asp_base_y1= float(asp_df[asp_df["Year"]==forecast_years[0]]["RollingASP_6M"].mean())

    st_left, st_right = st.columns([1, 1.6])

    with st_left:
        st.markdown('<div class="sec-header">🔩 Stress Levers</div>', unsafe_allow_html=True)

        # IDN to track as floor
        idn_names_st = [x["name"] for x in idn_list_stress]
        stress_idn_name = st.selectbox("Reference IDN (acquisition floor)",
                                        idn_names_st, key="stress_idn_sel",
                                        label_visibility="visible")
        stress_idn = next((x for x in idn_list_stress if x["name"] == stress_idn_name),
                          idn_list_stress[0])
        stress_floor = wac_base * (1 - stress_idn["discount"] / 100)

        st.markdown("---")
        st.markdown("**Lever 1 — GPO Discount Escalation**")
        st.caption("Simulate payer pressure forcing deeper GPO/IDN contracts")
        stress_gpo = st.slider("GPO Discount % off WAC",
                                min_value=0.0, max_value=70.0,
                                value=float(disc_dict.get(forecast_years[0],{}).get("gpo",14.0)),
                                step=0.5, key="stress_gpo",
                                help="Higher discount → lower invoice price → ASP falls")

        stress_idn_disc = st.slider("IDN Discount % off WAC",
                                     min_value=0.0, max_value=70.0,
                                     value=float(disc_dict.get(forecast_years[0],{}).get("idn",20.0)),
                                     step=0.5, key="stress_idn_disc")

        st.markdown("**Lever 2 — 340B Volume Growth**")
        st.caption("340B sales are exempt from ASP but dilute mfr revenue; large 340B mix erodes blended ASP indirectly by shrinking eligible volume")
        stress_b340_mix = st.slider("340B Channel % of total mix",
                                     min_value=0.0, max_value=40.0,
                                     value=float(ch_alloc_dict.get(forecast_years[0],{}).get("GPO/IDN 340B", 4.0)),
                                     step=1.0, key="stress_b340_mix")

        st.markdown("**Lever 3 — GPO/IDN Non-340B Volume Growth**")
        st.caption("More volume through deeply discounted channels → pulls ASP down")
        stress_gpo_mix = st.slider("GPO/IDN Non-340B % of mix",
                                    min_value=0.0, max_value=50.0,
                                    value=float(ch_alloc_dict.get(forecast_years[0],{}).get("GPO/IDN Non-340B", 7.0)),
                                    step=1.0, key="stress_gpo_mix")

        st.markdown("**Lever 4 — Commercial PBM Mix Erosion**")
        st.caption("PBM invoiced at WAC — losing PBM share lowers ASP")
        stress_pbm_mix = st.slider("Commercial PBM % of mix",
                                    min_value=0.0, max_value=60.0,
                                    value=float(ch_alloc_dict.get(forecast_years[0],{}).get("Commercial PBM", 25.0)),
                                    step=1.0, key="stress_pbm_mix")

        st.markdown("**Lever 5 — WAC Price Erosion vs Baseline**")
        st.caption("Simulate IRA price caps or voluntary price reductions")
        stress_wac_pct = st.slider("WAC as % of current WAC",
                                    min_value=50.0, max_value=110.0,
                                    value=100.0, step=1.0, key="stress_wac_pct",
                                    help="100% = unchanged; 80% = 20% WAC reduction")

        # ── Build stress scenario dicts ──────────────────────────────
        stress_wac_mult = stress_wac_pct / 100.0

        # Remaining channels scale proportionally
        fixed_stress = stress_pbm_mix + stress_gpo_mix + stress_b340_mix
        rem_stress   = max(0.0, 100.0 - fixed_stress)
        other_stress_chs = [c for c in CHANNELS
                            if c not in ("Commercial PBM","GPO/IDN Non-340B","GPO/IDN 340B")]
        other_stress_tot = sum(ch_alloc_dict.get(forecast_years[0],{}).get(c, 0)
                                for c in other_stress_chs)

        stress_alloc = {}
        for c in CHANNELS:
            if c == "Commercial PBM":     stress_alloc[c] = stress_pbm_mix
            elif c == "GPO/IDN Non-340B": stress_alloc[c] = stress_gpo_mix
            elif c == "GPO/IDN 340B":     stress_alloc[c] = stress_b340_mix
            else:
                bs = (ch_alloc_dict.get(forecast_years[0],{}).get(c, 0)
                      / other_stress_tot if other_stress_tot > 0 else 0)
                stress_alloc[c] = rem_stress * bs

        stress_alloc_dict = {yr: stress_alloc for yr in forecast_years}
        stress_disc_dict  = {}
        for yr in forecast_years:
            bd = disc_dict.get(yr, disc_dict[forecast_years[0]])
            stress_disc_dict[yr] = {
                "gpo": stress_gpo, "idn": stress_idn_disc,
                "b340": bd["b340"], "va": bd["va"],
            }

        # Modify monthly_df WAC for WAC erosion lever
        stress_monthly = monthly_df.copy()
        stress_monthly["WAC"] = stress_monthly["WAC"] * stress_wac_mult
        stress_floor_adj = stress_floor  # floor fixed to original IDN contract

        # ── Compute stress ASP ────────────────────────────────────────
        stress_asp_df = compute_asp_series(stress_monthly, stress_alloc_dict, stress_disc_dict)

        # Stress ASP year 1 for display
        stress_asp_y1 = float(stress_asp_df[stress_asp_df["Year"]==forecast_years[0]]["RollingASP_6M"].mean())
        stress_asp6_y1= stress_asp_y1 * 1.06
        asp_delta_y1  = stress_asp_y1 - asp_base_y1
        in_risk_y1    = stress_asp_y1 < stress_floor_adj

        # ── Live risk readout ─────────────────────────────────────────
        risk_bg     = "#2a0505" if in_risk_y1 else "#052010"
        risk_border = "#b02a2a" if in_risk_y1 else "#1a6e3a"
        risk_icon   = "🔴 IN RISK" if in_risk_y1 else "🟢 SAFE"
        risk_color  = "#f87171" if in_risk_y1 else "#4ade80"
        margin_val  = stress_asp6_y1 - stress_floor_adj
        margin_color= "#f87171" if margin_val < 0 else "#4ade80"

        st.markdown(f"""
        <div style='background:{risk_bg};border:2px solid {risk_border};
        border-radius:10px;padding:14px 16px;margin-top:12px;'>
        <div style='font-family:Syne;font-size:1rem;font-weight:800;
        color:{risk_color};margin-bottom:10px;'>{risk_icon}</div>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
        <div style='background:#001C4A;border-radius:6px;padding:8px;'>
        <div style='font-size:0.6rem;color:#FFFFFF;text-transform:uppercase;'>Stress ASP (Y1)</div>
        <div style='font-family:JetBrains Mono;font-size:0.9rem;color:{risk_color};font-weight:700;'>
        {fmt_d(stress_asp_y1)}</div></div>
        <div style='background:#001C4A;border-radius:6px;padding:8px;'>
        <div style='font-size:0.6rem;color:#FFFFFF;text-transform:uppercase;'>Vs Baseline</div>
        <div style='font-family:JetBrains Mono;font-size:0.9rem;
        color:{"#f87171" if asp_delta_y1<0 else "#4ade80"};font-weight:700;'>
        {fmt_d(asp_delta_y1)}</div></div>
        <div style='background:#001C4A;border-radius:6px;padding:8px;'>
        <div style='font-size:0.6rem;color:#FFFFFF;text-transform:uppercase;'>IDN Floor</div>
        <div style='font-family:JetBrains Mono;font-size:0.9rem;color:#FFFFFF;font-weight:700;'>
        {fmt_d(stress_floor_adj)}</div></div>
        <div style='background:#001C4A;border-radius:6px;padding:8px;'>
        <div style='font-size:0.6rem;color:#FFFFFF;text-transform:uppercase;'>Provider Margin</div>
        <div style='font-family:JetBrains Mono;font-size:0.9rem;color:{margin_color};font-weight:700;'>
        {fmt_d(margin_val)}</div></div>
        </div></div>""", unsafe_allow_html=True)

    with st_right:
        st.markdown('<div class="sec-header">📉 ASP Risk Trajectory — Baseline vs Stress</div>',
                    unsafe_allow_html=True)

        # ── Main risk chart ───────────────────────────────────────────
        fig_risk = go.Figure()

        # Risk zone shading (between floor and 0)
        fig_risk.add_hrect(
            y0=0, y1=stress_floor_adj,
            fillcolor="rgba(248,113,113,0.08)",
            line_width=0,
            annotation_text="⚠️ DANGER ZONE (ASP < IDN Floor)",
            annotation_position="top left",
            annotation_font=dict(color="#f87171", size=10),
        )

        # IDN acquisition floor
        fig_risk.add_hline(
            y=stress_floor_adj,
            line_color="#f87171", line_dash="dash", line_width=2,
            annotation_text=f"IDN Floor: {fmt_d(stress_floor_adj)}",
            annotation_position="bottom right",
            annotation_font=dict(color="#f87171", size=10),
        )

        # Baseline ASP
        fig_risk.add_trace(go.Scatter(
            x=asp_df["Period"], y=asp_df["RollingASP_6M"],
            name="Baseline ASP", mode="lines",
            line=dict(color="#4ade80", width=2.5),
        ))

        # Baseline ASP+6%
        fig_risk.add_trace(go.Scatter(
            x=asp_df["Period"], y=asp_df["ASP_Plus6"],
            name="Baseline ASP+6%", mode="lines",
            line=dict(color="#A8D5FF", width=1.5, dash="dot"),
        ))

        # Stress ASP
        fig_risk.add_trace(go.Scatter(
            x=stress_asp_df["Period"], y=stress_asp_df["RollingASP_6M"],
            name="Stress ASP", mode="lines",
            line=dict(color="#f87171", width=3),
        ))

        # Stress ASP+6%
        fig_risk.add_trace(go.Scatter(
            x=stress_asp_df["Period"], y=stress_asp_df["ASP_Plus6"],
            name="Stress ASP+6%", mode="lines",
            line=dict(color="#fb923c", width=1.5, dash="dot"),
        ))

        # Fill between baseline and stress ASP — shows the "erosion gap"
        fig_risk.add_trace(go.Scatter(
            x=asp_df["Period"].tolist() + stress_asp_df["Period"].tolist()[::-1],
            y=asp_df["RollingASP_6M"].tolist() + stress_asp_df["RollingASP_6M"].tolist()[::-1],
            fill="toself", fillcolor="rgba(248,113,113,0.10)",
            line=dict(color="rgba(0,0,0,0)"),
            name="ASP Erosion Gap", showlegend=True, hoverinfo="skip",
        ))

        # Flag months where stress ASP < floor
        for _, r in stress_asp_df[stress_asp_df["RollingASP_6M"] < stress_floor_adj].iterrows():
            fig_risk.add_shape(
                type="line", x0=r["Period"], x1=r["Period"], y0=0, y1=1,
                xref="x", yref="paper",
                line=dict(color="rgba(248,113,113,0.35)", width=2),
            )

        # Year dividers
        for yr in forecast_years[1:]:
            fig_risk.add_shape(type="line", x0=f"{yr}-Jan", x1=f"{yr}-Jan",
                               y0=0, y1=1, xref="x", yref="paper",
                               line=dict(color="#003A8C", width=1, dash="dot"))

        fig_risk.update_layout(
            title="ASP Risk Analysis — Stress vs Baseline (red shading = danger zone)",
            height=400, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            yaxis_title="Price ($ / Unit)", xaxis_tickangle=-45,
        )
        apply_axes_style(fig_risk)
        st.plotly_chart(fig_risk, use_container_width=True, theme=None)

        # ── Year-by-year risk scoreboard ──────────────────────────────
        st.markdown('<div class="sec-header">🎯 Year-by-Year Risk Scoreboard</div>',
                    unsafe_allow_html=True)

        stress_annual = stress_asp_df.groupby("Year").agg(
            Stress_ASP=("RollingASP_6M","mean"),
            Stress_ASP6=("ASP_Plus6","mean"),
        ).reset_index()
        base_annual_st = asp_df.groupby("Year").agg(
            Base_ASP=("RollingASP_6M","mean"),
        ).reset_index()
        risk_cmp = base_annual_st.merge(stress_annual, on="Year")
        risk_cmp["In_Risk"]  = risk_cmp["Stress_ASP"] < stress_floor_adj
        risk_cmp["Margin"]   = risk_cmp["Stress_ASP6"] - stress_floor_adj
        risk_cmp["Erosion"]  = risk_cmp["Stress_ASP"] - risk_cmp["Base_ASP"]

        sb2 = st.columns(len(forecast_years))
        for j, yr in enumerate(forecast_years):
            row_r = risk_cmp[risk_cmp["Year"]==yr]
            if len(row_r) == 0: continue
            row_r   = row_r.iloc[0]
            in_risk = row_r["In_Risk"]
            margin  = row_r["Margin"]
            erosion = row_r["Erosion"]
            with sb2[j]:
                icon_r  = "🔴" if in_risk else "🟢"
                status_r= "RISK" if in_risk else "SAFE"
                c_r     = "#f87171" if in_risk else "#4ade80"
                bg_r    = "border:1px solid #b02a2a;background:#1a0505" if in_risk else "border:1px solid #1a6e3a;background:#031209"
                st.markdown(f"""
                <div style='{bg_r};border-radius:8px;padding:9px 8px;text-align:center;'>
                <div style='font-family:Syne;font-weight:700;color:#FFFFFF;font-size:0.72rem;'>{yr}</div>
                <div style='font-size:1rem;margin:3px 0;'>{icon_r}</div>
                <div style='font-family:JetBrains Mono;font-size:0.7rem;color:{c_r};font-weight:700;'>{status_r}</div>
                <div style='font-size:0.62rem;color:#FFFFFF;margin-top:3px;font-family:JetBrains Mono;'>
                ASP: {fmt_d(row_r["Stress_ASP"])}</div>
                <div style='font-size:0.62rem;color:{"#f87171" if margin<0 else "#4ade80"};font-family:JetBrains Mono;'>
                Margin: {fmt_d(margin)}</div>
                <div style='font-size:0.62rem;color:{"#f87171" if erosion<0 else "#4ade80"};font-family:JetBrains Mono;'>
                Δ: {fmt_d(erosion)}</div>
                </div>""", unsafe_allow_html=True)

        # ── Tipping point analysis ─────────────────────────────────────
        st.markdown('<div class="sec-header">📌 Tipping Point — At What GPO Discount Does ASP Hit the Floor?</div>',
                    unsafe_allow_html=True)

        # Sweep GPO discount from current to max, find where stress ASP crosses the floor
        sweep_discounts = [round(x * 0.5, 1) for x in range(0, 141)]  # 0 to 70%
        tipping_point   = None
        sweep_rows = []
        for gd in sweep_discounts:
            sd = {}
            for yr in forecast_years:
                bd = disc_dict.get(yr, disc_dict[forecast_years[0]])
                sd[yr] = {"gpo": gd, "idn": stress_idn_disc, "b340": bd["b340"], "va": bd["va"]}
            sw_asp = compute_asp_series(stress_monthly, stress_alloc_dict, sd)
            sw_asp_y1 = float(sw_asp[sw_asp["Year"]==forecast_years[0]]["RollingASP_6M"].mean())
            sw_asp6_y1= sw_asp_y1 * 1.06
            in_r = sw_asp_y1 < stress_floor_adj
            sweep_rows.append({"GPO Disc %": gd, "Stress ASP": sw_asp_y1,
                                "ASP+6%": sw_asp6_y1, "In Risk": in_r})
            if tipping_point is None and in_r:
                tipping_point = gd

        sweep_df = pd.DataFrame(sweep_rows)

        # Tipping point callout
        if tipping_point is not None:
            cur_gpo = disc_dict.get(forecast_years[0], {}).get("gpo", 14.0)
            gap     = tipping_point - cur_gpo
            gap_color = "#4ade80" if gap > 5 else "#fbbf24" if gap > 0 else "#f87171"
            st.markdown(f"""
            <div style='background:#001C4A;border:2px solid {gap_color};border-radius:10px;
            padding:14px 18px;margin-bottom:10px;'>
            <div style='font-family:Syne;font-weight:700;font-size:0.9rem;color:{gap_color};'>
            ⚠️ Tipping Point: GPO Discount ≥ <span style='font-family:JetBrains Mono;
            font-size:1.1rem;'>{tipping_point:.1f}%</span></div>
            <div style='font-size:0.78rem;color:#FFFFFF;margin-top:6px;'>
            Current GPO discount: <b style='color:#FFFFFF;font-family:JetBrains Mono;'>{cur_gpo:.1f}%</b> &nbsp;|&nbsp;
            Headroom before risk: <b style='color:{gap_color};font-family:JetBrains Mono;'>{gap:+.1f} pp</b>
            </div>
            <div style='font-size:0.72rem;color:#FFFFFF;margin-top:4px;'>
            At {tipping_point:.1f}% GPO discount, stress ASP crosses below the IDN acquisition floor
            of {fmt_d(stress_floor_adj)} — buy-and-bill becomes unprofitable for providers.
            </div></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='card card-success' style='padding:12px 16px;'>
            ✅ ASP does not breach the IDN floor at any GPO discount up to 70%.
            Current channel mix and pricing maintain a safe margin throughout.
            </div>""", unsafe_allow_html=True)

        # Tipping point chart
        fig_tp = go.Figure()
        fig_tp.add_hline(y=stress_floor_adj, line_color="#f87171", line_dash="dash",
                         line_width=2, annotation_text=f"IDN Floor {fmt_d(stress_floor_adj)}",
                         annotation_font=dict(color="#f87171", size=10))
        fig_tp.add_trace(go.Scatter(
            x=sweep_df["GPO Disc %"], y=sweep_df["Stress ASP"],
            name="Stress ASP", mode="lines",
            line=dict(color="#f87171", width=2.5),
        ))
        fig_tp.add_trace(go.Scatter(
            x=sweep_df["GPO Disc %"], y=sweep_df["ASP+6%"],
            name="Stress ASP+6%", mode="lines",
            line=dict(color="#fb923c", width=1.5, dash="dot"),
        ))
        if tipping_point is not None:
            fig_tp.add_vline(x=tipping_point, line_color="#fbbf24", line_dash="dot",
                             line_width=2,
                             annotation_text=f"Tipping: {tipping_point:.1f}%",
                             annotation_font=dict(color="#fbbf24", size=11))
        fig_tp.update_layout(
            title="ASP vs GPO Discount Sweep — Finding the Tipping Point",
            height=300, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            xaxis_title="GPO Discount (% off WAC)",
            yaxis_title="Average Selling Price ($ / Unit)",
        )
        apply_axes_style(fig_tp)
        st.plotly_chart(fig_tp, use_container_width=True, theme=None)

    # ═══════════════════════════════════════════════════════════════
    # ASP RESCUE SIMULATOR
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#050f05 0%,#050a18 100%);
    border:1px solid #0a4a20;border-radius:12px;padding:16px 22px;margin:8px 0;'>
    <div style='font-family:Syne;font-weight:800;font-size:1.1rem;color:#FFFFFF;margin-bottom:6px;'>
    🎯 ASP Rescue Simulator</div>
    <div style='font-size:0.82rem;color:#FFFFFF;line-height:1.6;'>
    Adjust contract terms below and watch the 6-month rolling ASP recalculate in real time.
    The goal: find the combination of GPO/IDN discounts and channel mix that lifts ASP
    <b style='color:#FFFFFF;'>above the IDN acquisition floor</b> — turning 🚩 flags into ✅ clean status.
    <br><br>
    <b>What drives ASP down:</b> Higher GPO/IDN discounts (lower invoice price to providers) ·
    Growing IDN/GPO channel share · 340B volumes (exempt but reduce mfr revenue)<br>
    <b>What rescues ASP:</b> Reducing GPO/IDN discounts · Shifting mix toward Commercial PBM/WAC channels
    </div></div>""", unsafe_allow_html=True)

    # ── Reference IDN floor (pick one IDN to track) ─────────────────
    idn_list_sim = st.session_state.get("idn_list", [
        {"name": "IDN-A", "discount": 20.0, "volume_pct": 30.0, "is_340b": False}
    ])
    sim_col_cfg, sim_col_chart = st.columns([1, 1.6])

    with sim_col_cfg:
        st.markdown('<div class="sec-header">⚙️ Scenario Controls</div>', unsafe_allow_html=True)

        st.markdown("<div class='metric-label-sm'>🎯 Track IDN (acquisition floor)</div>",
                    unsafe_allow_html=True)
        idn_names_sim = [x["name"] for x in idn_list_sim]
        tracked_idn_name = st.selectbox("Track IDN", idn_names_sim, key="sim_tracked_idn",
                                         label_visibility="collapsed")
        tracked_idn = next((x for x in idn_list_sim if x["name"] == tracked_idn_name), idn_list_sim[0])

        st.markdown("---")
        st.markdown("**📉 Discount Levers** *(lower = higher ASP)*")

        sim_gpo = st.slider("GPO Contract Discount % off WAC",
                            min_value=0.0, max_value=50.0,
                            value=float(st.session_state.get("disc_sim_gpo",
                                disc_dict.get(forecast_years[0], {}).get("gpo", 14.0))),
                            step=0.5, key="disc_sim_gpo",
                            help="Lowering GPO discount raises the invoice price → raises ASP")

        sim_idn = st.slider("IDN Contract Discount % off WAC",
                            min_value=0.0, max_value=60.0,
                            value=float(st.session_state.get("disc_sim_idn",
                                disc_dict.get(forecast_years[0], {}).get("idn", 20.0))),
                            step=0.5, key="disc_sim_idn")

        st.markdown("**🔀 Channel Mix Levers** *(shift mix toward WAC channels)*")

        sim_com_pbm = st.slider("Commercial PBM % of mix",
                                min_value=0.0, max_value=60.0,
                                value=float(st.session_state.get("mix_sim_com_pbm",
                                    ch_alloc_dict.get(forecast_years[0], {}).get("Commercial PBM", 25.0))),
                                step=1.0, key="mix_sim_com_pbm",
                                help="Commercial PBM invoiced at WAC — highest ASP contributor")

        sim_mcr_b = st.slider("Medicare Part B % of mix",
                               min_value=0.0, max_value=40.0,
                               value=float(st.session_state.get("mix_sim_mcr_b",
                                   ch_alloc_dict.get(forecast_years[0], {}).get("Medicare Part B", 16.0))),
                               step=1.0, key="mix_sim_mcr_b")

        sim_gpo_mix = st.slider("GPO/IDN Non-340B % of mix",
                                min_value=0.0, max_value=40.0,
                                value=float(st.session_state.get("mix_sim_gpo",
                                    ch_alloc_dict.get(forecast_years[0], {}).get("GPO/IDN Non-340B", 7.0))),
                                step=1.0, key="mix_sim_gpo")

        # Normalize remaining channels to fill 100%
        fixed_pct  = sim_com_pbm + sim_mcr_b + sim_gpo_mix
        remaining  = max(0.0, 100.0 - fixed_pct)

        # Build scenario alloc — scale other channels proportionally
        base_alloc_yr1  = ch_alloc_dict.get(forecast_years[0], {})
        other_channels  = [c for c in CHANNELS
                           if c not in ("Commercial PBM","Medicare Part B","GPO/IDN Non-340B")]
        other_base_total= sum(base_alloc_yr1.get(c, 0) for c in other_channels)
        sim_alloc = {}
        for c in CHANNELS:
            if c == "Commercial PBM":     sim_alloc[c] = sim_com_pbm
            elif c == "Medicare Part B":  sim_alloc[c] = sim_mcr_b
            elif c == "GPO/IDN Non-340B": sim_alloc[c] = sim_gpo_mix
            else:
                base_share = base_alloc_yr1.get(c, 0) / other_base_total if other_base_total > 0 else 0
                sim_alloc[c] = remaining * base_share

        total_check = sum(sim_alloc.values())
        color_check = "#4ade80" if abs(total_check - 100) < 1 else "#f87171"
        st.markdown(f"<div style='font-size:0.75rem;color:{color_check};"
                    f"font-family:JetBrains Mono;'>Σ mix = {total_check:.1f}%</div>",
                    unsafe_allow_html=True)

        # Build scenario discount dict (apply to all years)
        sim_disc_dict = {}
        for yr in forecast_years:
            base_d = disc_dict.get(yr, disc_dict[forecast_years[0]])
            sim_disc_dict[yr] = {
                "gpo":  sim_gpo,
                "idn":  sim_idn,
                "b340": base_d["b340"],
                "va":   base_d["va"],
            }

        sim_alloc_dict = {yr: sim_alloc for yr in forecast_years}

        # IDN acquisition floor under scenario
        wac_y1_sim  = st.session_state.forecast_df["WAC per Unit"].iloc[0]
        idn_acq_sim = wac_y1_sim * (1 - tracked_idn["discount"] / 100)
        st.markdown(f"""
        <div style='background:#002766;border:1px solid #6AB4F0;border-radius:8px;
        padding:10px 14px;margin-top:10px;'>
        <div style='font-size:0.7rem;color:#FFFFFF;font-family:JetBrains Mono;'>
        TRACKED IDN ACQUISITION FLOOR</div>
        <div style='font-family:JetBrains Mono;font-size:1.1rem;font-weight:700;color:#FFFFFF;'>
        {fmt_d(idn_acq_sim)}/unit</div>
        <div style='font-size:0.7rem;color:#FFFFFF;'>({tracked_idn["discount"]}% off WAC
        ${wac_y1_sim:,.0f}) — ASP must exceed this</div>
        </div>""", unsafe_allow_html=True)

    with sim_col_chart:
        st.markdown('<div class="sec-header">📈 Baseline vs Scenario ASP Comparison</div>',
                    unsafe_allow_html=True)

        # Re-compute ASP under scenario
        sim_asp_df = compute_asp_series(monthly_df, sim_alloc_dict, sim_disc_dict)

        # Annual summaries
        base_annual = asp_df.groupby("Year")["RollingASP_6M"].mean().reset_index()
        base_annual.columns = ["Year", "Baseline_ASP"]
        scen_annual = sim_asp_df.groupby("Year")["RollingASP_6M"].mean().reset_index()
        scen_annual.columns = ["Year", "Scenario_ASP"]
        compare_df  = base_annual.merge(scen_annual, on="Year")
        compare_df["Delta"] = compare_df["Scenario_ASP"] - compare_df["Baseline_ASP"]
        compare_df["Above_Floor"] = compare_df["Scenario_ASP"] > idn_acq_sim

        # Chart — monthly lines
        fig_sim = go.Figure()

        # IDN floor line
        fig_sim.add_hline(
            y=idn_acq_sim,
            line_color="#f87171", line_dash="dot", line_width=2,
            annotation_text=f"IDN Floor ({tracked_idn_name}): {fmt_d(idn_acq_sim)}",
            annotation_position="top left",
            annotation_font=dict(color="#f87171", size=10),
        )

        # Baseline ASP
        fig_sim.add_trace(go.Scatter(
            x=asp_df["Period"], y=asp_df["RollingASP_6M"],
            name="Baseline ASP", mode="lines",
            line=dict(color="#A09A96", width=2, dash="dash"),
            opacity=0.8,
        ))

        # Scenario ASP
        fig_sim.add_trace(go.Scatter(
            x=sim_asp_df["Period"], y=sim_asp_df["RollingASP_6M"],
            name="Scenario ASP", mode="lines",
            line=dict(color="#4ade80", width=3),
        ))

        # ASP+6% scenario
        fig_sim.add_trace(go.Scatter(
            x=sim_asp_df["Period"], y=sim_asp_df["ASP_Plus6"],
            name="Scenario ASP+6%", mode="lines",
            line=dict(color="#A8D5FF", width=1.5),
        ))

        # Fill: green when scenario ASP > floor, red when below
        for i in range(len(sim_asp_df) - 1):
            row_curr = sim_asp_df.iloc[i]
            row_next = sim_asp_df.iloc[i + 1]
            above = row_curr["RollingASP_6M"] >= idn_acq_sim
            fig_sim.add_trace(go.Scatter(
                x=[row_curr["Period"], row_next["Period"],
                   row_next["Period"], row_curr["Period"]],
                y=[idn_acq_sim, idn_acq_sim,
                   row_next["RollingASP_6M"], row_curr["RollingASP_6M"]],
                fill="toself",
                fillcolor="rgba(74,222,128,0.12)" if above else "rgba(248,113,113,0.12)",
                line=dict(color="rgba(0,0,0,0)"),
                showlegend=False, hoverinfo="skip",
            ))

        # Year dividers
        for yr in forecast_years[1:]:
            fig_sim.add_shape(type="line", x0=f"{yr}-Jan", x1=f"{yr}-Jan",
                              y0=0, y1=1, xref="x", yref="paper",
                              line=dict(color="#003A8C", width=1, dash="dot"))

        fig_sim.update_layout(
            title="ASP Rescue: Scenario vs Baseline vs IDN Floor",
            height=380, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            yaxis_title="Price ($ / Unit)", xaxis_tickangle=-45,
        )
        apply_axes_style(fig_sim)
        st.plotly_chart(fig_sim, use_container_width=True, theme=None)

        # ── Annual comparison scoreboard ─────────────────────────────
        st.markdown('<div class="sec-header">🏆 Year-by-Year Rescue Scoreboard</div>',
                    unsafe_allow_html=True)

        sb_cols = st.columns(len(forecast_years))
        for j, yr in enumerate(forecast_years):
            row_c = compare_df[compare_df["Year"] == yr]
            if len(row_c) == 0:
                continue
            row_c  = row_c.iloc[0]
            b_asp  = row_c["Baseline_ASP"]
            s_asp  = row_c["Scenario_ASP"]
            delta  = row_c["Delta"]
            rescued= row_c["Above_Floor"]
            with sb_cols[j]:
                icon   = "✅" if rescued else "🚩"
                color  = "#4ade80" if rescued else "#f87171"
                status = "RESCUED" if rescued else "BELOW FLOOR"
                delta_color = "#4ade80" if delta > 0 else "#f87171"
                st.markdown(f"""
                <div style='background:#FFFFFF; border:1px solid {"#86EFAC" if rescued else "#FCA5A5"}; box-shadow:0 4px 12px {"rgba(34,197,94,0.15)" if rescued else "rgba(239,68,68,0.15)"};
                border-radius:12px; padding:16px 12px; text-align:center; transition: transform 0.2s;' onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style='font-family:"Inter", sans-serif; font-weight:800; color:#1E293B; font-size:1rem; margin-bottom:4px;'>{yr}</div>
                <div style='font-size:1.4rem; margin:8px 0;'>{icon}</div>
                <div style='margin: 8px auto; display: inline-block; background: {"#DCFCE7" if rescued else "#FEE2E2"}; color: {"#166534" if rescued else "#991B1B"}; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-family: "JetBrains Mono", monospace; font-size: 0.7rem; letter-spacing: 0.5px;'>
                {status}</div>
                <div style='font-size:0.75rem; color:#64748B; margin-top:8px; font-family:"JetBrains Mono", monospace;'>
                Base: {fmt_d(b_asp)}</div>
                <div style='font-size:0.75rem; color:#64748B; font-family:"JetBrains Mono", monospace;'>
                Scen: <span style='font-weight:700; color:#1E293B;'>{fmt_d(s_asp)}</span></div>
                <div style='font-size:0.75rem; color:{delta_color}; font-weight:700; font-family:"JetBrains Mono", monospace; margin-top:4px;'>
                Δ {fmt_d(delta)}</div>
                </div>""", unsafe_allow_html=True)

        # ── Break-even finder ────────────────────────────────────────
        st.markdown('<div class="sec-header">🔍 What GPO Discount Makes ASP = IDN Floor?</div>',
                    unsafe_allow_html=True)

        wac_be    = st.session_state.forecast_df["WAC per Unit"].mean()
        base_alloc_be = ch_alloc_dict.get(forecast_years[0], {})

        # Eligible channel weights for ASP
        eligible_chs = {c: base_alloc_be.get(c, 0) for c in CHANNELS if ASP_ELIGIBLE.get(c, False)}
        total_elig   = sum(eligible_chs.values())
        if total_elig > 0:
            # ASP = Σ(price_i × w_i) where w_i = alloc_i / Σ(eligible allocs)
            # price_i = WAC for PBM/D/Cash, gpo_price for Med/McrB, idn_price for GPO
            # Solve for gpo_disc such that ASP = idn_acq_sim
            # ASP ≈ WAC × [w_pbm + w_d + w_cash + w_med×(1-gpo) + w_mcrb×(1-gpo) + w_gpoidn×(1-idn)]
            # = WAC × [C_fixed + C_gpo×(1-gpo_disc/100)]
            w  = {c: eligible_chs[c] / total_elig for c in eligible_chs}
            c_fixed = (w.get("Commercial PBM",0) + w.get("Medicare Part D",0)
                       + w.get("Cash/Uninsured",0))
            c_gpo   = w.get("Commercial Medical",0) + w.get("Medicare Part B",0)
            c_idn   = w.get("GPO/IDN Non-340B",0)
            idn_frac= 1 - tracked_idn["discount"] / 100

            # idn_acq_sim = WAC × [c_fixed + c_gpo×(1-x/100) + c_idn×idn_frac]
            # solve for x:
            target_ratio = idn_acq_sim / wac_be if wac_be > 0 else 0
            if c_gpo > 0:
                be_disc = (1 - (target_ratio - c_fixed - c_idn * idn_frac) / c_gpo) * 100
                be_disc = max(0, min(99, be_disc))
                be_color= "#4ade80" if be_disc < sim_gpo else "#fbbf24"
                st.markdown(f"""
                <div style='background:#F0F9FF; border-left:4px solid #0EA5E9; border-radius:4px; margin-top:12px;
                padding:16px 20px; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
                <span style='color:#0369A1; font-family:"Inter", sans-serif; font-size:0.95rem; line-height:1.5;'>To make <b style='color:#0284C7;'>
                Scenario ASP ≥ {fmt_d(idn_acq_sim)}</b> (IDN floor), GPO discount must be
                <b style='color:{be_color}; font-family:"JetBrains Mono", monospace; background:#E0F2FE; padding:2px 6px; border-radius:4px;'>≤ {be_disc:.1f}%</b>
                (current scenario: {sim_gpo:.1f}%) — assuming current channel mix.
                </span></div>""", unsafe_allow_html=True)
            else:
                st.markdown("<div class='info-box'>Set GPO/Commercial Medical mix > 0% to enable break-even analysis.</div>",
                            unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 5 — GTN MODEL
# ═══════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("## 🧮 GTN Model — Full Multi-Year Waterfall")

    # Compute full GTN
    if "asp_df" not in st.session_state:
        st.warning("Please visit the ASP Engine tab first to initialize calculations.")
        st.stop()

    asp_df    = st.session_state["asp_df"]
    monthly_df= st.session_state["monthly_df"]
    gtn_df    = compute_gtn(monthly_df, asp_df,
                             st.session_state["ch_alloc_dict"],
                             st.session_state["disc_dict"],
                             st.session_state["rebate_dict"],
                             st.session_state["other_dict"])

    # Annual rollup
    annual_gtn = gtn_df.groupby("Year").agg(
        GrossSales=("GrossSales","sum"), TotalRebates=("TotalRebates","sum"),
        TotalChargebacks=("TotalChargebacks","sum"), TotalOther=("TotalOther","sum"),
        TotalDeductions=("TotalDeductions","sum"), NetSales=("NetSales","sum"),
        Units=("Units","sum"), GTN_Pct=("GTN_Pct","mean"),
    ).reset_index()
    annual_gtn["NetPrice"] = annual_gtn["NetSales"] / annual_gtn["Units"]
    annual_gtn["NetPct"]   = annual_gtn["NetSales"] / annual_gtn["GrossSales"] * 100

    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    total_gross = annual_gtn["GrossSales"].sum()
    total_net   = annual_gtn["NetSales"].sum()
    total_deductions = annual_gtn["TotalDeductions"].sum()
    avg_gtn_pct = total_deductions / total_gross * 100
    peak_net_yr = annual_gtn.loc[annual_gtn["NetSales"].idxmax(), "Year"]

    col1.metric("Total Gross Sales", fmt_b(total_gross) if total_gross>=1e9 else fmt_m(total_gross))
    col2.metric("Total Net Sales", fmt_b(total_net) if total_net>=1e9 else fmt_m(total_net))
    col3.metric("Total Deductions", fmt_m(total_deductions))
    col4.metric("Avg GTN %", fmt_pct(avg_gtn_pct))
    col5.metric("Peak Net Sales Year", str(peak_net_yr))

    # ── Multi-year waterfall ──
    st.markdown('<div class="sec-header">📉 Annual GTN Waterfall</div>', unsafe_allow_html=True)
    fig_wf = go.Figure()
    fig_wf.add_trace(go.Bar(x=annual_gtn["Year"], y=annual_gtn["GrossSales"]/1e6,
                             name="Gross Sales", marker_color="#A8D5FF", opacity=0.85))
    fig_wf.add_trace(go.Bar(x=annual_gtn["Year"], y=-annual_gtn["TotalRebates"]/1e6,
                             name="Rebates", marker_color="#f87171", opacity=0.85))
    fig_wf.add_trace(go.Bar(x=annual_gtn["Year"], y=-annual_gtn["TotalChargebacks"]/1e6,
                             name="Chargebacks", marker_color="#fb923c", opacity=0.85))
    fig_wf.add_trace(go.Bar(x=annual_gtn["Year"], y=-annual_gtn["TotalOther"]/1e6,
                             name="Fees/Other", marker_color="#fbbf24", opacity=0.85))
    fig_wf.add_trace(go.Scatter(x=annual_gtn["Year"], y=annual_gtn["NetSales"]/1e6,
                                 name="Net Sales", mode="lines+markers+text",
                                 line=dict(color="#4ade80", width=3),
                                 marker=dict(size=10, symbol="diamond", color="#4ade80"),
                                 text=[fmt_m(v) for v in annual_gtn["NetSales"]],
                                 textposition="top center", textfont=dict(size=9, color="#4ade80")))
    fig_wf.update_layout(barmode="relative", title="GTN Waterfall — Annual ($M)",
                          height=380, **PLOTLY_LAYOUT, yaxis_title="Amount ($ Millions USD)", legend_font_size=11)
    apply_axes_style(fig_wf)
    st.plotly_chart(fig_wf, use_container_width=True, theme=None)

    # ── GTN % trend ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-header">📊 GTN % & Net Price Trend</div>', unsafe_allow_html=True)
        fig_gtnpct = make_subplots(specs=[[{"secondary_y": True}]])
        fig_gtnpct.add_trace(go.Bar(x=annual_gtn["Year"], y=annual_gtn["GTN_Pct"],
                                     name="GTN %", marker_color="#f87171", opacity=0.75), secondary_y=False)
        fig_gtnpct.add_trace(go.Scatter(x=annual_gtn["Year"], y=annual_gtn["NetPrice"],
                                         name="Net $/Unit", mode="lines+markers",
                                         line=dict(color="#4ade80", width=2.5),
                                         marker=dict(size=8)), secondary_y=True)
        fig_gtnpct.update_layout(title="GTN % and Net Price per Unit", height=280,
                                  **PLOTLY_LAYOUT, margin=dict(t=40,b=20,l=80,r=80))
        fig_gtnpct.update_yaxes(title_text="Gross-To-Net Yield (%)", secondary_y=False)
        fig_gtnpct.update_yaxes(title_text="Net Price ($ / Unit)", secondary_y=True)
        apply_axes_style(fig_gtnpct)
        st.plotly_chart(fig_gtnpct, use_container_width=True, theme=None)

    with col2:
        st.markdown('<div class="sec-header">🧩 Deduction Mix by Year</div>', unsafe_allow_html=True)
        fig_dmix = go.Figure()
        fig_dmix.add_trace(go.Bar(x=annual_gtn["Year"],
                                   y=annual_gtn["TotalRebates"]/annual_gtn["GrossSales"]*100,
                                   name="Rebates", marker_color="#f87171"))
        fig_dmix.add_trace(go.Bar(x=annual_gtn["Year"],
                                   y=annual_gtn["TotalChargebacks"]/annual_gtn["GrossSales"]*100,
                                   name="Chargebacks", marker_color="#fb923c"))
        fig_dmix.add_trace(go.Bar(x=annual_gtn["Year"],
                                   y=annual_gtn["TotalOther"]/annual_gtn["GrossSales"]*100,
                                   name="Fees/Other", marker_color="#fbbf24"))
        fig_dmix.update_layout(barmode="stack", title="Deduction Components (% of Gross)", height=280,
                                **PLOTLY_LAYOUT, yaxis_title="Percentage of Gross (%)", legend_font_size=10)
        apply_axes_style(fig_dmix)
        st.plotly_chart(fig_dmix, use_container_width=True, theme=None)

    # ── Full Annual Summary Table — transposed (metrics as rows, years as cols) ──
    st.markdown('<div class="sec-header">📋 Annual GTN Summary Table</div>', unsafe_allow_html=True)
    gtn_yrs = annual_gtn["Year"].tolist()
    gtn_metrics = {
        "Units":              [fmt_u(v)  for v in annual_gtn["Units"]],
        "Gross Sales ($M)":   [f"${v/1e6:.2f}M" for v in annual_gtn["GrossSales"]],
        "Rebates ($M)":       [f"${v/1e6:.2f}M" for v in annual_gtn["TotalRebates"]],
        "Chargebacks ($M)":   [f"${v/1e6:.2f}M" for v in annual_gtn["TotalChargebacks"]],
        "Fees/Other ($M)":    [f"${v/1e6:.2f}M" for v in annual_gtn["TotalOther"]],
        "Total Deductions":   [f"${v/1e6:.2f}M" for v in annual_gtn["TotalDeductions"]],
        "Net Sales ($M)":     [f"${v/1e6:.2f}M" for v in annual_gtn["NetSales"]],
        "GTN %":              [fmt_pct(v) for v in annual_gtn["GTN_Pct"]],
        "Net $/Unit":         [fmt_d(v)  for v in annual_gtn["NetPrice"]],
        "Net % of WAC":       [fmt_pct(v) for v in annual_gtn["NetPct"]],
    }
    gtn_T = pd.DataFrame({
        "Metric": list(gtn_metrics.keys()),
        **{str(yr): [gtn_metrics[m][i] for m in gtn_metrics]
           for i, yr in enumerate(gtn_yrs)}
    })
    st.dataframe(gtn_T, use_container_width=True, hide_index=True)

    # ── Monthly detail ──
    st.markdown('<div class="sec-header">📅 Monthly GTN Detail</div>', unsafe_allow_html=True)
    yr_sel = st.selectbox("Select Year for Monthly Detail", forecast_years, key="gtn_yr_sel")
    mo_sub = gtn_df[gtn_df["Year"] == yr_sel]

    fig_mo_gtn = go.Figure()
    fig_mo_gtn.add_trace(go.Bar(x=mo_sub["Month"], y=mo_sub["GrossSales"]/1e6,
                                 name="Gross", marker_color="#A8D5FF", opacity=0.75))
    fig_mo_gtn.add_trace(go.Bar(x=mo_sub["Month"], y=mo_sub["NetSales"]/1e6,
                                 name="Net", marker_color="#4ade80", opacity=0.85))
    fig_mo_gtn.add_trace(go.Scatter(x=mo_sub["Month"], y=mo_sub["GTN_Pct"],
                                     name="GTN %", mode="lines+markers",
                                     line=dict(color="#f87171", width=2), yaxis="y2"))
    fig_mo_gtn.update_layout(barmode="group", title=f"{yr_sel} — Monthly Gross vs Net ($M) + GTN%",
                              height=300, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
                              yaxis=dict(title="Amount ($ Millions USD)", gridcolor="#003A8C", zerolinecolor="#003A8C"),
                              yaxis2=dict(title="Gross-To-Net Yield (%)", overlaying="y", side="right",
                                          gridcolor="#003A8C", zerolinecolor="#003A8C"))
    st.plotly_chart(fig_mo_gtn, use_container_width=True, theme=None)

    # ── Channel-Wise GTN Breakdown ──────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="sec-header">📡 Channel-Wise GTN Breakdown</div>', unsafe_allow_html=True)
    st.markdown("""<div class='info-box'>
    Revenue flows differently through each payer channel. Commercial PBM and Medicare Part D
    are invoiced at WAC with post-sale rebates; GPO/IDN channels have chargebacks at point of sale;
    340B and VA have the deepest discounts. This section shows the per-channel economics.
    </div>""", unsafe_allow_html=True)

    yr_ch_sel = st.selectbox("Select Year for Channel Breakdown", forecast_years, key="gtn_ch_yr_sel")

    # Compute per-channel economics for selected year
    ch_alloc = st.session_state["ch_alloc_dict"].get(yr_ch_sel, {})
    disc_yr  = st.session_state["disc_dict"].get(yr_ch_sel, {})
    reb_yr   = st.session_state["rebate_dict"].get(yr_ch_sel, {})
    oth_yr   = st.session_state["other_dict"].get(yr_ch_sel, {})
    fc_yr    = st.session_state.forecast_df[st.session_state.forecast_df["Year"]==yr_ch_sel]
    yr_units = float(fc_yr["Annual Units"].values[0]) if len(fc_yr) else 0
    yr_wac   = float(fc_yr["WAC per Unit"].values[0]) if len(fc_yr) else 0

    # Price schedule
    gpo_p  = yr_wac * (1 - disc_yr.get("gpo",0)/100)
    idn_p  = yr_wac * (1 - disc_yr.get("idn",0)/100)
    b340_p = yr_wac * (1 - disc_yr.get("b340",0)/100)
    va_p   = yr_wac * (1 - disc_yr.get("va",0)/100)

    # Rebate map
    ch_rebate_pct = {
        "Commercial PBM": reb_yr.get("com_pbm",0), "Commercial Medical": reb_yr.get("com_med",0),
        "Medicare Part B": 0, "Medicare Part D": reb_yr.get("mcr_d",0),
        "Medicaid FFS": reb_yr.get("mcaid",0), "Managed Medicaid": reb_yr.get("man_mcaid",0),
        "GPO/IDN Non-340B": 0, "GPO/IDN 340B": 0, "VA/DoD/Federal": 0, "Cash/Uninsured": 0,
    }
    # Chargeback per unit
    ch_cb_per_unit = {
        "Commercial PBM": 0, "Commercial Medical": yr_wac - gpo_p,
        "Medicare Part B": yr_wac - gpo_p, "Medicare Part D": 0,
        "Medicaid FFS": 0, "Managed Medicaid": 0,
        "GPO/IDN Non-340B": yr_wac - idn_p, "GPO/IDN 340B": yr_wac - b340_p,
        "VA/DoD/Federal": yr_wac - va_p, "Cash/Uninsured": 0,
    }

    other_total_pct = oth_yr.get("admin_fee",0) + oth_yr.get("dist_fee",0) + oth_yr.get("copay",0) + oth_yr.get("returns",0)

    ch_data_rows = []
    for ch in CHANNELS:
        alloc_pct = ch_alloc.get(ch, 0)
        ch_units  = yr_units * alloc_pct / 100
        gross     = ch_units * yr_wac
        rebates   = ch_units * yr_wac * ch_rebate_pct[ch] / 100
        cbacks    = ch_units * ch_cb_per_unit[ch]
        other_ded = gross * other_total_pct / 100
        total_ded = rebates + cbacks + other_ded
        net       = gross - total_ded
        gtn_pct   = total_ded / gross * 100 if gross > 0 else 0
        ch_data_rows.append({
            "Channel": ch, "Alloc %": alloc_pct, "Units": ch_units,
            "Gross ($M)": gross/1e6, "Rebates ($M)": rebates/1e6,
            "Chargebacks ($M)": cbacks/1e6, "Other ($M)": other_ded/1e6,
            "Total Ded ($M)": total_ded/1e6, "Net ($M)": net/1e6, "GTN %": gtn_pct,
            # Raw for Sankey
            "_gross": gross, "_rebates": rebates, "_cbacks": cbacks, "_other": other_ded, "_net": net,
        })
    ch_breakdown = pd.DataFrame(ch_data_rows)

    # ── Grouped Bar: Gross / Deductions / Net per Channel ────────────
    col_bar, col_pie = st.columns([1.6, 1])
    with col_bar:
        st.markdown(f'<div class="sec-header">📊 Channel GTN Waterfall — {yr_ch_sel}</div>', unsafe_allow_html=True)
        fig_ch_bar = go.Figure()
        fig_ch_bar.add_trace(go.Bar(
            y=ch_breakdown["Channel"], x=ch_breakdown["Gross ($M)"],
            name="Gross Sales", marker_color="#A8D5FF", opacity=0.85, orientation="h",
        ))
        fig_ch_bar.add_trace(go.Bar(
            y=ch_breakdown["Channel"], x=-ch_breakdown["Total Ded ($M)"],
            name="Total Deductions", marker_color="#f87171", opacity=0.85, orientation="h",
        ))
        fig_ch_bar.add_trace(go.Bar(
            y=ch_breakdown["Channel"], x=ch_breakdown["Net ($M)"],
            name="Net Sales", marker_color="#4ade80", opacity=0.85, orientation="h",
        ))
        fig_ch_bar.update_layout(
            barmode="group", height=420, margin=dict(t=30, b=20, l=160, r=40),
            **PLOTLY_LAYOUT, xaxis_title="Amount ($ Millions USD)",
        )
        fig_ch_bar.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        font=dict(size=10, color="#2D3748"), bgcolor="rgba(255,255,255,0.8)"),
        )
        apply_axes_style(fig_ch_bar)
        st.plotly_chart(fig_ch_bar, use_container_width=True, theme=None)

    with col_pie:
        st.markdown(f'<div class="sec-header">🥧 GTN % by Channel — {yr_ch_sel}</div>', unsafe_allow_html=True)
        active_ch = ch_breakdown[ch_breakdown["Alloc %"] > 0]
        fig_gtn_pie = go.Figure(go.Bar(
            x=active_ch["Channel"], y=active_ch["GTN %"],
            marker_color=[COLORS_MAIN[i % len(COLORS_MAIN)] for i in range(len(active_ch))],
            text=[f"{v:.1f}%" for v in active_ch["GTN %"]],
            textposition="outside", textfont=dict(size=9, color="#1A1A2E"),
        ))
        fig_gtn_pie.update_layout(
            height=420, margin=dict(t=30, b=80, l=40, r=20),
            **PLOTLY_LAYOUT, yaxis_title="GTN %", xaxis_tickangle=-45,
        )
        apply_axes_style(fig_gtn_pie)
        st.plotly_chart(fig_gtn_pie, use_container_width=True, theme=None)

    # ── Sankey Diagram: Channel Path Flow ─────────────────────────────
    st.markdown(f'<div class="sec-header">🔀 Channel Path — Revenue Flow Diagram ({yr_ch_sel})</div>', unsafe_allow_html=True)
    st.caption("Shows how gross revenue flows through each payer channel and splits into net sales vs. deduction categories.")

    # Build Sankey nodes and links
    active_channels = [r for _, r in ch_breakdown.iterrows() if r["_gross"] > 0]
    n_ch = len(active_channels)

    # Nodes: [0] Gross Sales → [1..n_ch] Channels → [n_ch+1] Net Sales, [n_ch+2] Rebates, [n_ch+3] Chargebacks, [n_ch+4] Fees
    node_labels = ["Gross Sales"]
    node_colors = ["#A8D5FF"]
    for i, r in enumerate(active_channels):
        node_labels.append(r["Channel"])
        node_colors.append(COLORS_MAIN[i % len(COLORS_MAIN)])
    node_labels += ["Net Sales", "Rebates", "Chargebacks", "Fees/Other"]
    node_colors += ["#4ade80", "#f87171", "#fb923c", "#fbbf24"]

    net_idx = n_ch + 1
    reb_idx = n_ch + 2
    cb_idx  = n_ch + 3
    fee_idx = n_ch + 4

    sources, targets, values, link_colors = [], [], [], []
    for i, r in enumerate(active_channels):
        ch_idx = i + 1
        # Gross → Channel
        sources.append(0); targets.append(ch_idx); values.append(r["_gross"])
        link_colors.append("rgba(168,213,255,0.3)")
        # Channel → Net
        if r["_net"] > 0:
            sources.append(ch_idx); targets.append(net_idx); values.append(r["_net"])
            link_colors.append("rgba(74,222,128,0.3)")
        # Channel → Rebates
        if r["_rebates"] > 0:
            sources.append(ch_idx); targets.append(reb_idx); values.append(r["_rebates"])
            link_colors.append("rgba(248,113,113,0.3)")
        # Channel → Chargebacks
        if r["_cbacks"] > 0:
            sources.append(ch_idx); targets.append(cb_idx); values.append(r["_cbacks"])
            link_colors.append("rgba(251,146,60,0.3)")
        # Channel → Fees
        if r["_other"] > 0:
            sources.append(ch_idx); targets.append(fee_idx); values.append(r["_other"])
            link_colors.append("rgba(251,191,36,0.3)")

    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            pad=15, thickness=20,
            label=node_labels,
            color=node_colors,
            line=dict(color="#E2E8F0", width=0.5),
        ),
        link=dict(
            source=sources, target=targets, value=values,
            color=link_colors,
        ),
    ))
    fig_sankey.update_layout(
        title=f"Revenue Flow: Gross → Channels → Net / Deductions ({yr_ch_sel})",
        height=480, margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#1A1A2E", family="Inter", size=11),
    )
    st.plotly_chart(fig_sankey, use_container_width=True, theme=None)

    # ── Channel Summary Table ─────────────────────────────────────────
    st.markdown(f'<div class="sec-header">📋 Channel Summary Table — {yr_ch_sel}</div>', unsafe_allow_html=True)
    ch_table = ch_breakdown[ch_breakdown["Alloc %"] > 0][
        ["Channel", "Alloc %", "Units", "Gross ($M)", "Rebates ($M)",
         "Chargebacks ($M)", "Other ($M)", "Total Ded ($M)", "Net ($M)", "GTN %"]
    ].copy()
    ch_table["Units"] = ch_table["Units"].apply(lambda v: fmt_u(v))
    for col in ["Gross ($M)", "Rebates ($M)", "Chargebacks ($M)", "Other ($M)", "Total Ded ($M)", "Net ($M)"]:
        ch_table[col] = ch_table[col].apply(lambda v: f"${v:.2f}M")
    ch_table["GTN %"] = ch_table["GTN %"].apply(lambda v: fmt_pct(v))
    ch_table["Alloc %"] = ch_table["Alloc %"].apply(lambda v: f"{v:.1f}%")
    st.dataframe(ch_table, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 6 — BUY & BILL — MULTI-IDN
# ═══════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("## 🏥 Buy & Bill — Multi-IDN Analysis")

    if "asp_df" not in st.session_state:
        st.warning("Please visit the ASP Engine tab first to initialise calculations.")
        st.stop()

    asp_df_bb  = st.session_state["asp_df"]
    gtn_df_bb  = compute_gtn(
        st.session_state["monthly_df"], asp_df_bb,
        st.session_state["ch_alloc_dict"], st.session_state["disc_dict"],
        st.session_state["rebate_dict"],   st.session_state["other_dict"],
    )
    annual_asp = asp_df_bb.groupby("Year").agg(
        ASP=("RollingASP_6M","mean"), ASP6=("ASP_Plus6","mean"), WAC=("WAC","mean"),
    ).reset_index()

    # ── Init IDN list ────────────────────────────────────────────────
    if "idn_list" not in st.session_state:
        st.session_state.idn_list = [
            {"name": "IDN-A (Academic Medical)",   "discount": 20.0, "volume_pct": 30.0, "is_340b": False},
            {"name": "IDN-B (Community Hospital)", "discount": 18.0, "volume_pct": 25.0, "is_340b": False},
            {"name": "IDN-C (340B Entity)",        "discount": 25.6, "volume_pct": 15.0, "is_340b": True},
            {"name": "IDN-D (GPO Member)",         "discount": 15.0, "volume_pct": 20.0, "is_340b": False},
            {"name": "IDN-E (VA Affiliate)",       "discount": 24.0, "volume_pct": 10.0, "is_340b": False},
        ]

    # Use current list for read-only display (pre-computation)
    idn_list_ro = st.session_state.idn_list

    # ────────────────────────────────────────────────────────────────
    # SECTION 1 — PORTFOLIO OVERVIEW (read-only KPI cards + charts)
    # ────────────────────────────────────────────────────────────────
    st.markdown("""<div class='info-box'>
    <b>Buy & Bill mechanics:</b> Provider purchases drug at IDN/GPO contract price,
    administers to patient, then bills Medicare at <b>ASP + 6%</b>.
    Manufacturer revenue = IDN acquisition price. Provider margin = ASP+6% − Acquisition.
    A 🚩 flag fires when <b>ASP falls below acquisition cost</b> — the provider loses money
    on every unit and will stop using the drug.
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-header">🏥 IDN Portfolio — High Level Overview</div>',
                unsafe_allow_html=True)
    st.caption("KPIs computed at Year 1 prices. Click '⚙️ Edit IDN Allocations' below to adjust.")

    # Quick compute Year 1 KPIs for overview cards
    yr1_asp_row = annual_asp.iloc[0] if len(annual_asp) > 0 else None
    yr1_asp  = float(yr1_asp_row["ASP"])  if yr1_asp_row is not None else 0.0
    yr1_asp6 = float(yr1_asp_row["ASP6"]) if yr1_asp_row is not None else 0.0
    yr1_wac  = float(yr1_asp_row["WAC"])  if yr1_asp_row is not None else 0.0
    yr1_total_units = float(
        st.session_state.forecast_df["Annual Units"].iloc[0]
    ) if len(st.session_state.forecast_df) > 0 else 0.0

    # ── Portfolio KPI banner ─────────────────────────────────────────
    k_cols = st.columns(4)
    k_cols[0].metric("IDNs Configured",   str(len(idn_list_ro)))
    k_cols[1].metric("Year 1 ASP",        fmt_d(yr1_asp))
    k_cols[2].metric("Medicare Reimb (ASP+6%)", fmt_d(yr1_asp6))
    k_cols[3].metric("Year 1 WAC",        fmt_d(yr1_wac))

    # ── IDN Portfolio Cards ──────────────────────────────────────────
    n_ro   = len(idn_list_ro)
    card_cols = st.columns(min(n_ro, 5))
    for i, idn in enumerate(idn_list_ro):
        acq      = yr1_wac * (1 - idn["discount"] / 100)
        spread   = yr1_asp6 - acq
        flagged  = yr1_asp < acq          # ASP below what provider paid
        bb_pct   = (
            st.session_state.ch_alloc_dict.get(
                int(st.session_state.forecast_df["Year"].iloc[0]), {}
            ).get("Medicare Part B", 16)
            + st.session_state.ch_alloc_dict.get(
                int(st.session_state.forecast_df["Year"].iloc[0]), {}
            ).get("Commercial Medical", 18)
        ) / 100
        idn_units  = yr1_total_units * bb_pct * (idn["volume_pct"] / 100)
        mfr_rev_yr1= idn_units * acq

        status_icon  = "🚩" if flagged else "✅"
        status_text  = "ASP < ACQ" if flagged else "Profitable"
        card_bg      = "#1a0505" if flagged else "#031209"
        card_border  = "#b02a2a" if flagged else "#1a6e3a"
        spread_color = "#f87171" if spread < 0 else "#4ade80"
        type_tag     = "🟡 340B" if idn["is_340b"] else "🔵 GPO/IDN"

        with card_cols[i % 5]:
            st.markdown(f"""
            <div style='background:#FFFFFF; border:1px solid {"#FECACA" if flagged else "#E2E8F0"};
            border-radius:12px; padding:16px 14px; margin-bottom:8px; box-shadow: 0 4px 16px rgba(0,0,0,0.04);'>

            <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;'>
            <div style='font-family:"Inter", sans-serif; font-size:0.85rem; font-weight:800;
            color:#1E293B; line-height:1.3;'>{idn["name"]}</div>
            <div style='font-size:1.1rem;'>{status_icon}</div>
            </div>

            <div style='font-size:0.68rem; color:#64748B; font-weight:600; margin-bottom:12px;'>{type_tag}</div>

            <div style='display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-bottom:8px;'>
            <div style='background:#F8FAFC; border:1px solid #F1F5F9; border-radius:6px; padding:8px 10px;'>
            <div style='font-size:0.6rem; color:#64748B; text-transform:uppercase; letter-spacing:0.4px; font-weight:700;'>Discount</div>
            <div style='font-family:"JetBrains Mono", monospace; font-size:0.88rem; color:#0F172A; font-weight:700;'>
            {idn["discount"]}%</div>
            </div>
            <div style='background:#F8FAFC; border:1px solid #F1F5F9; border-radius:6px; padding:8px 10px;'>
            <div style='font-size:0.6rem; color:#64748B; text-transform:uppercase; letter-spacing:0.4px; font-weight:700;'>B&B Vol</div>
            <div style='font-family:"JetBrains Mono", monospace; font-size:0.88rem; color:#0F172A; font-weight:700;'>
            {idn["volume_pct"]:.0f}%</div>
            </div>
            <div style='background:#F8FAFC; border:1px solid #F1F5F9; border-radius:6px; padding:8px 10px;'>
            <div style='font-size:0.6rem; color:#64748B; text-transform:uppercase; letter-spacing:0.4px; font-weight:700;'>Acq. Price</div>
            <div style='font-family:"JetBrains Mono", monospace; font-size:0.88rem; color:#0F172A; font-weight:700;'>
            {fmt_d(acq)}</div>
            </div>
            <div style='background:{"#FEF2F2" if spread < 0 else "#F0FDF4"}; border:1px solid {"#FCA5A5" if spread < 0 else "#86EFAC"}; border-radius:6px; padding:8px 10px;'>
            <div style='font-size:0.6rem; color:{"#991B1B" if spread < 0 else "#166534"}; text-transform:uppercase; letter-spacing:0.4px; font-weight:700;'>Spread</div>
            <div style='font-family:"JetBrains Mono", monospace; font-size:0.88rem; color:{"#991B1B" if spread < 0 else "#166534"}; font-weight:700;'>
            {fmt_d(spread)}</div>
            </div>
            </div>

            <div style='background:#F8FAFC; border:1px solid #F1F5F9; border-radius:6px; padding:8px 10px; margin-bottom:12px;'>
            <div style='font-size:0.6rem; color:#64748B; text-transform:uppercase; letter-spacing:0.4px; font-weight:700;'>Est. Mfr Rev (Y1)</div>
            <div style='font-family:"JetBrains Mono", monospace; font-size:0.88rem; color:#0F172A; font-weight:700;'>
            {fmt_m(mfr_rev_yr1)}</div>
            </div>

            <div style='text-align:center; background:{"#FEF2F2" if flagged else "#ECFCCB"}; border-radius:6px; padding:6px; font-size:0.75rem; font-weight:700; color:{"#991B1B" if flagged else "#166534"}; font-family:"JetBrains Mono", monospace;'>{status_icon} {status_text}</div>
            </div>""", unsafe_allow_html=True)

    # ── Portfolio summary table ──────────────────────────────────────
    st.markdown('<div class="sec-header">📋 Portfolio Summary Table</div>', unsafe_allow_html=True)
    port_rows = []
    for idn in idn_list_ro:
        acq    = yr1_wac * (1 - idn["discount"] / 100)
        spread = yr1_asp6 - acq
        flagged= yr1_asp < acq
        port_rows.append({
            "IDN Name":        idn["name"],
            "Type":            "340B" if idn["is_340b"] else "GPO/IDN",
            "Discount % off WAC": f"{idn['discount']:.1f}%",
            "B&B Volume %":    f"{idn['volume_pct']:.1f}%",
            "Acquisition Price": fmt_d(acq),
            "ASP+6% (Medicare)": fmt_d(yr1_asp6),
            "Provider Spread":  fmt_d(spread),
            "Status":          "🚩 ASP<ACQ" if flagged else "✅ Profitable",
        })
    st.dataframe(pd.DataFrame(port_rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ────────────────────────────────────────────────────────────────
    # SECTION 2 — DRILL DOWN: EDIT IDN ALLOCATIONS (expander)
    # ────────────────────────────────────────────────────────────────
    with st.expander("⚙️ Edit IDN Allocations — Add, Remove & Adjust", expanded=False):
        st.caption("Changes here update all charts and flags below in real time.")

        btn_cols = st.columns([1, 1, 4])
        with btn_cols[0]:
            if st.button("➕ Add IDN", use_container_width=True):
                st.session_state.idn_list.append({
                    "name": f"IDN-{chr(65+len(st.session_state.idn_list))} (New)",
                    "discount": 15.0, "volume_pct": 10.0, "is_340b": False,
                })
                st.rerun()
        with btn_cols[1]:
            if st.button("🗑️ Remove Last", use_container_width=True) and len(st.session_state.idn_list) > 1:
                st.session_state.idn_list.pop()
                st.rerun()

        idn_list = st.session_state.idn_list
        n_idn    = len(idn_list)

        # Column headers
        hdr_c = st.columns([0.3, 2.2, 1.2, 1.2, 0.8])
        for hc, lbl in zip(hdr_c, ["#", "IDN Name", "Discount % off WAC", "% of B&B Volume", "340B"]):
            hc.markdown(f"<div style='font-size:0.7rem;color:#475569;text-transform:uppercase;font-weight:700;"
                        f"font-family:Inter, sans-serif;padding:6px 2px;border-bottom:2px solid #E2E8F0;'>"
                        f"{lbl}</div>", unsafe_allow_html=True)

        updated_idn = []
        for i, idn in enumerate(idn_list):
            row_c = st.columns([0.3, 2.2, 1.2, 1.2, 0.8])
            with row_c[0]:
                st.markdown(f"<div style='font-family:Inter, sans-serif;font-weight:800;color:#334155;"
                            f"font-size:0.95rem;padding:12px 4px;'>#{i+1}</div>",
                            unsafe_allow_html=True)
            with row_c[1]:
                name = st.text_input("Name", value=idn["name"], key=f"idn_name_{i}",
                                      label_visibility="collapsed")
            with row_c[2]:
                disc = st.number_input("Disc", min_value=0.0, max_value=99.0,
                                        value=float(idn["discount"]), step=0.5, format="%.1f",
                                        key=f"idn_disc_{i}", label_visibility="collapsed")
            with row_c[3]:
                vol = st.number_input("Vol%", min_value=0.0, max_value=100.0,
                                       value=float(idn["volume_pct"]), step=1.0, format="%.1f",
                                       key=f"idn_vol_{i}", label_visibility="collapsed")
            with row_c[4]:
                is340 = st.checkbox("340B", value=bool(idn["is_340b"]), key=f"idn_340b_{i}")
            updated_idn.append({"name": name, "discount": disc, "volume_pct": vol, "is_340b": is340})
        st.session_state.idn_list = updated_idn

        total_vol = sum(x["volume_pct"] for x in updated_idn)
        if abs(total_vol - 100) > 1:
            st.markdown(f"<div class='card card-warn' style='padding:8px 14px;'>⚠️ IDN volume %s sum to {total_vol:.1f}% — should be 100%</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='card card-success' style='padding:8px 14px;'>✅ IDN volume allocation sums to {total_vol:.1f}%</div>", unsafe_allow_html=True)
    # end expander — use updated_idn from expander if it ran, else fall back to read-only list
    updated_idn = st.session_state.idn_list
    n_idn = len(updated_idn)

    st.markdown("---")

    # ── Per-IDN Computations ──────────────────────────────────────────
    # Build per-IDN annual data
    idn_data = []
    for idn in updated_idn:
        rows = []
        for _, asp_row in annual_asp.iterrows():
            yr  = asp_row["Year"]
            wac = asp_row["WAC"]
            asp = asp_row["ASP"]
            asp6= asp_row["ASP6"]
            acq = wac * (1 - idn["discount"] / 100)
            spread       = asp6 - acq
            spread_pct   = spread / asp6 * 100 if asp6 > 0 else 0
            below_asp    = asp < acq
            fc_row       = st.session_state.forecast_df[st.session_state.forecast_df["Year"]==yr]
            total_units  = float(fc_row["Annual Units"].values[0]) if len(fc_row) else 0
            # B&B units = total units × channel share × IDN volume share
            bb_channel_pct = (
                st.session_state.ch_alloc_dict.get(yr, {}).get("Medicare Part B", 16)
                + st.session_state.ch_alloc_dict.get(yr, {}).get("Commercial Medical", 18)
            ) / 100
            idn_units    = total_units * bb_channel_pct * (idn["volume_pct"] / 100)
            mfr_revenue  = idn_units * acq
            prov_profit  = idn_units * spread
            rows.append({
                "IDN": idn["name"], "Year": yr, "WAC": wac, "ASP": asp, "ASP6": asp6,
                "Acquisition": acq, "Spread": spread, "Spread_Pct": spread_pct,
                "Below_ASP": below_asp, "Is_340B": idn["is_340b"],
                "Discount": idn["discount"], "IDN_Units": idn_units,
                "Mfr_Revenue": mfr_revenue, "Prov_Profit": prov_profit,
            })
        idn_data.extend(rows)
    idn_df = pd.DataFrame(idn_data)

    # ── WAC vs ASP vs Acquisition — All IDNs ─────────────────────────
    st.markdown('<div class="sec-header">📊 WAC / ASP / Acquisition Price Comparison — All IDNs</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1.5, 1])

    with col_a:
        fig_all = go.Figure()
        fig_all.add_trace(go.Scatter(
            x=annual_asp["Year"], y=annual_asp["WAC"],
            name="WAC", line=dict(color="#fbbf24", width=2, dash="dot"),
            mode="lines+markers", marker=dict(size=7),
        ))
        fig_all.add_trace(go.Scatter(
            x=annual_asp["Year"], y=annual_asp["ASP"],
            name="6M Rolling ASP", line=dict(color="#4ade80", width=2.5),
            mode="lines+markers", marker=dict(size=8),
        ))
        fig_all.add_trace(go.Scatter(
            x=annual_asp["Year"], y=annual_asp["ASP6"],
            name="ASP+6% (Medicare Reimb.)", line=dict(color="#A8D5FF", width=2.5),
            mode="lines+markers", marker=dict(size=8),
        ))
        idn_colors = ["#f87171","#fb923c","#c084fc","#fbbf24","#60a5fa",
                      "#34d399","#a78bfa","#f472b6","#38bdf8","#84cc16"]
        for j, idn in enumerate(updated_idn):
            sub = idn_df[idn_df["IDN"] == idn["name"]]
            color = idn_colors[j % len(idn_colors)]
            dash  = "dash" if idn["is_340b"] else "solid"
            fig_all.add_trace(go.Scatter(
                x=sub["Year"], y=sub["Acquisition"],
                name=f"{idn['name']} ({idn['discount']}% off)",
                line=dict(color=color, width=1.8, dash=dash),
                mode="lines+markers", marker=dict(size=6, symbol="circle"),
            ))
            # Flag years where ASP < acquisition (provider loses money)
            for _, r in sub[sub["Below_ASP"]].iterrows():
                fig_all.add_vrect(
                    x0=r["Year"]-0.45, x1=r["Year"]+0.45,
                    fillcolor=color, opacity=0.05, line_width=0,
                )
        fig_all.update_layout(
            title="Price Comparison: WAC / ASP / All IDN Acquisitions",
            height=400, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT, yaxis_title="Price ($ / Unit)",
        )
        fig_all.update_layout(legend=dict(
            bgcolor="rgba(255,255,255,0.9)", bordercolor="#E2E8F0", borderwidth=1,
            font=dict(size=11, color="#1E293B", family="Inter"),
            orientation="v", x=1.02, xanchor="left", y=1, yanchor="top"
        ))
        apply_axes_style(fig_all)
        st.plotly_chart(fig_all, use_container_width=True, theme=None)

    with col_b:
        st.markdown('<div class="sec-header">📐 Provider Spread by IDN</div>', unsafe_allow_html=True)
        # Heatmap: rows=IDN, cols=Year, values=spread $
        idn_names = [x["name"] for x in updated_idn]
        spread_matrix = []
        for idn in updated_idn:
            sub = idn_df[idn_df["IDN"]==idn["name"]].sort_values("Year")
            spread_matrix.append(sub["Spread"].tolist())

        yr_labels = [str(y) for y in annual_asp["Year"].tolist()]
        fig_heat = go.Figure(go.Heatmap(
            z=spread_matrix,
            x=yr_labels,
            y=[x["name"].split("(")[0].strip() for x in updated_idn],
            colorscale=[[0, "#FCA5A5"], [0.5, "#FEF08A"], [1, "#86EFAC"]],
            text=[[f"${int(v):,}" for v in row] for row in spread_matrix],
            texttemplate="%{text}",
            textfont=dict(size=8, family="Inter", color="#1E293B"),
            hovertemplate="<b>%{y}</b><br>%{x}: Spread $%{z:,.0f}<extra></extra>",
            colorbar=dict(title="Spread $", tickfont=dict(size=9)),
        ))
        fig_heat.update_layout(
            title="Provider Spread (ASP+6% − Acq.) Heatmap",
            height=280, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
        )
        apply_axes_style(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True, theme=None)

    # ── Per-IDN Flag Cards ────────────────────────────────────────────
    st.markdown('<div class="sec-header">🚩 ASP vs Acquisition Flags — Per IDN Per Year</div>', unsafe_allow_html=True)
    flag_cols = st.columns(n_idn)
    for i, idn in enumerate(updated_idn):
        sub = idn_df[idn_df["IDN"]==idn["name"]].sort_values("Year")
        with flag_cols[i]:
            any_flag = sub["Below_ASP"].any()
            header_color = "#f87171" if any_flag else "#4ade80"
            st.markdown(f"""
            <div style='border:1px solid {"#FCA5A5" if any_flag else "#E2E8F0"};
            background:{"#FEF2F2" if any_flag else "#FFFFFF"}; box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            border-radius:12px; padding:12px 14px; margin-bottom:8px;'>
            <div style='font-family:"Inter", sans-serif; font-size:0.85rem; font-weight:800;
            color:{"#991B1B" if any_flag else "#1E293B"}; margin-bottom:6px;'>{idn["name"]}</div>
            <div style='font-size:0.68rem; color:#475569; font-weight:600; margin-bottom:8px;'>
            {"🟡 340B" if idn["is_340b"] else "🔵 GPO"} · {idn["discount"]}% off WAC</div>
            """, unsafe_allow_html=True)
            for _, row in sub.iterrows():
                flag  = row["Below_ASP"]
                color = "#f87171" if flag else "#4ade80"
                icon  = "🚩 ASP<ACQ" if flag else "✅ OK"
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                padding:6px 0;border-bottom:1px solid #E2E8F0;font-size:0.78rem;'>
                <span style='color:#334155;font-family:"JetBrains Mono", monospace;font-weight:600;'>{int(row["Year"])}</span>
                <span style='color:{color};font-family:JetBrains Mono;'>{icon} {fmt_d(row["Spread"])}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Provider Economics Chart per IDN ─────────────────────────────
    st.markdown('<div class="sec-header">💰 Provider Economics — Manufacturer Revenue vs Provider Profit by IDN</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)

    with col_e1:
        fig_mfr = go.Figure()
        for j, idn in enumerate(updated_idn):
            sub = idn_df[idn_df["IDN"]==idn["name"]].sort_values("Year")
            fig_mfr.add_trace(go.Bar(
                name=idn["name"].split("(")[0].strip(),
                x=sub["Year"], y=sub["Mfr_Revenue"]/1e6,
                marker_color=idn_colors[j % len(idn_colors)], opacity=0.8,
            ))
        fig_mfr.update_layout(
            barmode="group", title="Manufacturer Revenue by IDN ($M)",
            height=300, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            yaxis=dict(title="Amount ($ Millions USD)", gridcolor="#003A8C", zerolinecolor="#003A8C"),
            legend_font_size=9,
        )
        apply_axes_style(fig_mfr)
        st.plotly_chart(fig_mfr, use_container_width=True, theme=None)

    with col_e2:
        fig_prov2 = go.Figure()
        for j, idn in enumerate(updated_idn):
            sub = idn_df[idn_df["IDN"]==idn["name"]].sort_values("Year")
            fig_prov2.add_trace(go.Bar(
                name=idn["name"].split("(")[0].strip(),
                x=sub["Year"], y=sub["Prov_Profit"]/1e6,
                marker_color=idn_colors[j % len(idn_colors)], opacity=0.8,
            ))
        fig_prov2.update_layout(
            barmode="group", title="Provider Profit (Spread) by IDN ($M)",
            height=300, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            yaxis=dict(title="Amount ($ Millions USD)", gridcolor="#003A8C", zerolinecolor="#003A8C"),
            legend_font_size=9,
        )
        apply_axes_style(fig_prov2)
        st.plotly_chart(fig_prov2, use_container_width=True, theme=None)

    # ── Summary table: all IDNs × all years ──────────────────────────
    st.markdown('<div class="sec-header">📋 Multi-IDN Summary Table — Acquisition / ASP / Spread by Year</div>', unsafe_allow_html=True)
    sel_yr_bb = st.selectbox("View Year", forecast_years, key="bb_yr_sel")
    yr_sub    = idn_df[idn_df["Year"]==sel_yr_bb].copy()

    def _asp_val(col, default=0.0):
        rows = annual_asp.loc[annual_asp["Year"]==sel_yr_bb, col]
        return float(rows.values[0]) if len(rows) > 0 else default
    asp_sel  = _asp_val("ASP",  1500.0)
    asp6_sel = _asp_val("ASP6", 1590.0)
    wac_sel  = _asp_val("WAC",  1500.0)

    # Header row
    hdr = st.columns([2.2, 1, 1, 1, 1, 1, 1])
    for col_h, label in zip(hdr, ["IDN","WAC","ASP","ASP+6%","Acquisition","Spread/Unit","Flag"]):
        col_h.markdown(f"<div style='font-size:0.75rem;color:#475569;text-transform:uppercase;font-weight:700;"
                       f"font-family:Inter, sans-serif;padding:6px 0;border-bottom:2px solid #E2E8F0;'>{label}</div>",
                       unsafe_allow_html=True)

    # Reference row
    ref_row = st.columns([2.2, 1, 1, 1, 1, 1, 1])
    for rc, val in zip(ref_row, ["── Reference ──", fmt_d(wac_sel), fmt_d(asp_sel),
                                  fmt_d(asp6_sel), "—", "—", "—"]):
        rc.markdown(f"<div style='font-size:0.78rem;color:#0EA5E9;font-weight:700;padding:8px 2px;"
                    f"font-family:JetBrains Mono, monospace;'>{val}</div>", unsafe_allow_html=True)

    for _, row in yr_sub.iterrows():
        flag   = row["Below_ASP"]
        color  = "#f87171" if flag else "#4ade80"
        icon   = "🚩 ASP < ACQ" if flag else "✅ Clean"
        r_cols = st.columns([2.2, 1, 1, 1, 1, 1, 1])
        vals   = [
            row["IDN"],
            fmt_d(row["WAC"]),
            fmt_d(row["ASP"]),
            fmt_d(row["ASP6"]),
            fmt_d(row["Acquisition"]),
            fmt_d(row["Spread"]),
            icon,
        ]
        colors = ["#1E293B","#334155","#334155","#334155","#991B1B",
                  "#DC2626" if row["Spread"]<0 else "#166534", color]
        for rc, v, c in zip(r_cols, vals, colors):
            rc.markdown(f"<div style='font-size:0.8rem;color:{c};padding:8px 2px;font-weight:600;"
                        f"font-family:JetBrains Mono, monospace;border-bottom:1px solid #E2E8F0;'>{v}</div>",
                        unsafe_allow_html=True)

    # ── ASP Sensitivity Table ─────────────────────────────────────────
    st.markdown('<div class="sec-header">📐 ASP Sensitivity — Impact on All IDN Spreads</div>', unsafe_allow_html=True)
    asp_base = asp_sel
    sens_steps = [-10, -5, -3, 0, 3, 5, 10]
    sens_data = {"ASP Δ": [f"{s:+d}%" for s in sens_steps],
                 "New ASP": [fmt_d(asp_base*(1+s/100)) for s in sens_steps],
                 "ASP+6%":  [fmt_d(asp_base*(1+s/100)*1.06) for s in sens_steps]}
    for idn in updated_idn:
        acq   = wac_sel * (1 - idn["discount"]/100)
        label = idn["name"].split("(")[0].strip()
        spreads = []
        for s in sens_steps:
            new_asp6 = asp_base*(1+s/100)*1.06
            sp = new_asp6 - acq
            flag = " 🚩" if asp_base*(1+s/100) < acq else ""
            spreads.append(f"{fmt_d(sp)}{flag}")
        sens_data[label] = spreads
    st.dataframe(pd.DataFrame(sens_data), use_container_width=True, hide_index=True)

# ── Footer ──
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#999999;font-size:0.72rem;padding:6px;font-family:JetBrains Mono;'>
PharmGTN Pro v3 · Dynamic Multi-Year GTN Engine · For internal forecasting use only
</div>""", unsafe_allow_html=True)