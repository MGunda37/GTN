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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;600&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Brand Palette ──────────────────────────────────────────────────
   Prussian Blue  #001C4A   backgrounds (darkest)
   Prussian Mid   #002766   cards, sidebar
   Prussian Light #003A8C   borders, dividers
   Anakiwa        #A8D5FF   primary accent / labels
   Anakiwa Dim    #6AB4F0   secondary accent
   Anakiwa Pale   #D4EAFF   headings, bright values
   Pampas         #F1ECE9   body text
   Pampas Dim     #C8C2BE   muted text
   Pampas Faint   #A09A96   very muted
   ──────────────────────────────────────────────────────────────── */

html, body, [data-testid="stAppViewContainer"] {
    background: #001C4A !important;
    color: #F1ECE9;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #002766 !important;
    border-right: 1px solid #003A8C;
}
[data-testid="stSidebar"] *, [data-testid="stSidebar"] label { color: #A8D5FF !important; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #D4EAFF !important; font-family: 'Syne', sans-serif !important; }

h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; font-size: 1.7rem !important;
     background: linear-gradient(135deg, #A8D5FF 0%, #D4EAFF 100%);
     -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; }
h2 { color: #D4EAFF !important; font-size: 1.1rem !important; }
h3 { color: #A8D5FF !important; font-size: 0.95rem !important; }

.stTabs [data-baseweb="tab-list"] {
    gap: 2px; background: #002766; padding: 5px 6px;
    border-radius: 10px; border: 1px solid #003A8C;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 7px; border: none;
    color: #C8C2BE; font-family: 'DM Sans', sans-serif; font-size: 0.8rem; font-weight: 500;
    padding: 7px 14px; transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #003A8C 0%, #002766 100%) !important;
    color: #A8D5FF !important; border: 1px solid #6AB4F0 !important;
}

.card {
    background: #002766; border: 1px solid #003A8C; border-radius: 10px;
    padding: 14px 18px; margin: 5px 0;
}
.card-accent { border-color: #6AB4F0; background: #001C4A; }
.card-warn { border-color: #b38600; background: #1a1200; }
.card-danger { border-color: #b02a2a; background: #1a0505; }
.card-success { border-color: #1a6e3a; background: #031209; }

.mono { font-family: 'JetBrains Mono', monospace; }
.val-blue  { color: #A8D5FF; font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.val-green { color: #4ade80; font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.val-red   { color: #f87171; font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.val-amber { color: #fbbf24; font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.val-purple{ color: #c084fc; font-family: 'JetBrains Mono', monospace; font-weight: 600; }

.sec-header {
    background: linear-gradient(90deg, #003A8C55 0%, transparent 100%);
    border-left: 3px solid #A8D5FF; padding: 7px 14px;
    border-radius: 0 6px 6px 0; margin: 14px 0 10px; font-family: 'Syne', sans-serif;
    font-size: 0.85rem; font-weight: 700; color: #D4EAFF; letter-spacing: 0.3px;
}
.pill {
    display: inline-block; padding: 2px 9px; border-radius: 10px; font-size: 0.7rem;
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin: 1px;
    font-family: 'JetBrains Mono', monospace;
}
.pill-b { background: #002766; color: #A8D5FF; border: 1px solid #6AB4F0; }
.pill-g { background: #031a0a; color: #4ade80; border: 1px solid #1a6e3a; }
.pill-r { background: #1a0505; color: #f87171; border: 1px solid #b02a2a; }
.pill-a { background: #1a1200; color: #fbbf24; border: 1px solid #b38600; }
.pill-p { background: #120a1a; color: #c084fc; border: 1px solid #6a1a9a; }

.asp-box {
    background: linear-gradient(135deg, #001C4A 0%, #002766 100%);
    border: 1px solid #6AB4F0; border-radius: 10px; padding: 16px 20px; margin: 8px 0;
    color: #F1ECE9;
}
.flag-box {
    background: #1a0505; border: 1px solid #b02a2a; border-radius: 8px;
    padding: 12px 16px; margin: 6px 0; font-size: 0.82rem; color: #F1ECE9;
}
.info-box {
    background: #002766; border: 1px solid #003A8C; border-radius: 8px;
    padding: 13px 17px; font-size: 0.82rem; color: #C8C2BE; line-height: 1.65; margin: 8px 0;
}
div[data-testid="metric-container"] {
    background: #002766 !important; border: 1px solid #003A8C !important;
    border-radius: 9px !important; padding: 11px 15px !important;
}
div[data-testid="stMetricValue"] { color: #A8D5FF !important; font-family: 'JetBrains Mono', monospace !important; }
div[data-testid="stMetricLabel"] { color: #C8C2BE !important; }
div[data-testid="stMetricDelta"] svg { display: none; }

.stDataFrame { border-radius: 8px; overflow: hidden; }
.stDataFrame td, .stDataFrame th {
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important;
    background: #002766 !important; color: #F1ECE9 !important;
}
.stDataFrame thead th {
    background: #003A8C !important; color: #D4EAFF !important; font-weight: 700 !important;
}
input[type="number"], .stNumberInput input, .stSelectbox > div > div {
    background: #002766 !important; color: #F1ECE9 !important;
    border: 1px solid #003A8C !important; border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stSlider > div > div > div { background: #A8D5FF !important; }
hr { border-color: #003A8C !important; }

/* ── Stepper number_input: +/- buttons ── */
div[data-testid="stNumberInput"] {
    background: #001C4A;
}
div[data-testid="stNumberInput"] input {
    text-align: center !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    background: #002766 !important;
    color: #F1ECE9 !important;
    border: 1px solid #003A8C !important;
    border-radius: 6px !important;
    padding: 4px 6px !important;
}
div[data-testid="stNumberInput"] > div {
    gap: 2px !important;
}
button[data-testid="stNumberInput-StepUp"],
button[data-testid="stNumberInput-StepDown"] {
    background: #003A8C !important;
    color: #A8D5FF !important;
    border: 1px solid #6AB4F0 !important;
    border-radius: 5px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    min-width: 28px !important;
    height: 28px !important;
    padding: 0 !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
button[data-testid="stNumberInput-StepUp"]:hover,
button[data-testid="stNumberInput-StepDown"]:hover {
    background: #A8D5FF !important;
    color: #001C4A !important;
    border-color: #D4EAFF !important;
}
/* Year column header in stepper grids */
.yr-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #A8D5FF;
    text-align: center;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}
.metric-label-sm {
    font-size: 0.68rem;
    color: #C8C2BE;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
    font-family: 'JetBrains Mono', monospace;
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
        idn_below_asp = idn_p < asp_val
        b340_below_asp= b340_p < asp_val

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
    paper_bgcolor="#001C4A", plot_bgcolor="#002766",
    font=dict(color="#F1ECE9", family="DM Sans"),
    legend=dict(bgcolor="#002766", bordercolor="#003A8C", borderwidth=1,
                font_size=11, font_color="#F1ECE9"),
)
# xaxis/yaxis removed from PLOTLY_LAYOUT to prevent duplicate-keyword errors.
# Use apply_axes_style(fig) after update_layout to apply the brand grid.
PLOTLY_MARGIN = dict(t=40, b=30, l=20, r=20)
_GRID = dict(gridcolor="#003A8C", zerolinecolor="#003A8C")

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

# ───────────────────────────────────────────────────────────────────
# SIDEBAR
# ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚕️ PharmGTN Pro v4")
    st.markdown("*Dynamic Multi-Year GTN Engine*")
    st.markdown("---")
    product_name = st.text_input("Product Name", "RXPRODUCT-001")
    therapy_area = st.selectbox("Therapy Area", ["Oncology","Rare Disease","Immunology","Cardiovascular","Neurology","Other"])
    admin_route  = st.selectbox("Administration", ["IV Infusion (Buy & Bill)","SC Injection","Oral","IM Injection"])
    st.markdown("---")
    st.markdown("### ⚙️ Forecast Horizon")
    n_years = st.slider("Number of Forecast Years", 1, 10, 7)
    start_year = st.number_input("Start Year", 2024, 2030, 2025, 1)
    forecast_years = list(range(start_year, start_year + n_years))
    monthly_profile_choice = st.selectbox("Monthly Distribution Profile", list(MONTH_PROFILES.keys()) + ["Custom"])
    st.markdown("---")
    st.markdown("### 📋 Tabs")
    st.markdown("0. Dashboard\n1. Forecast Volumes\n2. Channel Allocation\n3. Contract Terms\n4. ASP Engine\n5. GTN Model\n6. Buy & Bill (Multi-IDN)")
    st.markdown("---")
    st.caption(f"Horizon: {forecast_years[0]}–{forecast_years[-1]} · {n_years} years")

# ───────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ───────────────────────────────────────────────────────────────────
if "forecast_df" not in st.session_state or len(st.session_state.forecast_df) != n_years:
    st.session_state.forecast_df = pd.DataFrame({
        "Year": forecast_years,
        "Annual Units": [10_000, 22_000, 38_000, 50_000, 58_000, 62_000, 65_000, 67_000, 68_000, 69_000][:n_years],
        "WAC per Unit": [round(1500 * (1.03 ** i), 2) for i in range(n_years)],
        "Monthly Profile": ["S-Curve (Launch)"] + ["Flat"] * (n_years - 1),
    })

if "channel_alloc_raw" not in st.session_state:
    base_alloc = {
        "Commercial PBM": 25, "Commercial Medical": 18, "Medicare Part B": 16,
        "Medicare Part D": 12, "Medicaid FFS": 8, "Managed Medicaid": 6,
        "GPO/IDN Non-340B": 7, "GPO/IDN 340B": 4, "VA/DoD/Federal": 2, "Cash/Uninsured": 2,
    }
    rows = []
    for yr in forecast_years:
        row = {"Year": yr}
        row.update(base_alloc)
        rows.append(row)
    st.session_state.channel_alloc_raw = pd.DataFrame(rows)

if "discount_raw" not in st.session_state:
    rows = []
    for i, yr in enumerate(forecast_years):
        rows.append({"Year": yr,
                     "GPO Disc %": round(14 + i*0.3, 1), "IDN Disc %": round(20 + i*0.4, 1),
                     "340B Disc %": round(25.6, 1),       "VA FSS Disc %": round(24.0, 1)})
    st.session_state.discount_raw = pd.DataFrame(rows)

if "rebate_raw" not in st.session_state:
    rows = []
    for i, yr in enumerate(forecast_years):
        rows.append({"Year": yr,
                     "Com PBM %": round(32 + i*0.5, 1), "Com Med %": round(13 + i*0.3, 1),
                     "Mcr Part D %": round(28 + i*0.5, 1), "Medicaid FFS %": 23.1,
                     "Managed Mcaid %": round(42 + i*0.3, 1)})
    st.session_state.rebate_raw = pd.DataFrame(rows)

if "other_raw" not in st.session_state:
    rows = []
    for yr in forecast_years:
        rows.append({"Year": yr, "Admin Fee %": 2.0, "Dist Fee %": 2.0,
                     "Copay Support %": 3.5, "Returns %": 1.5})
    st.session_state.other_raw = pd.DataFrame(rows)


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

    fc         = st.session_state.forecast_df
    gross_by_yr= fc["Annual Units"] * fc["WAC per Unit"]
    total_gross= gross_by_yr.sum()
    total_units= fc["Annual Units"].sum()
    peak_idx   = gross_by_yr.idxmax()
    peak_yr    = fc.loc[peak_idx, "Year"]
    has_data   = "asp_df" in st.session_state and "monthly_df" in st.session_state

    # Pre-compute GTN if data available
    if has_data:
        gtn_df_dash = compute_gtn(
            st.session_state["monthly_df"], st.session_state["asp_df"],
            st.session_state["ch_alloc_dict"], st.session_state["disc_dict"],
            st.session_state["rebate_dict"],   st.session_state["other_dict"],
        )
        ann_dash = gtn_df_dash.groupby("Year").agg(
            NetSales=("NetSales","sum"), GrossSales=("GrossSales","sum"),
            TotalDeductions=("TotalDeductions","sum"), TotalRebates=("TotalRebates","sum"),
            TotalChargebacks=("TotalChargebacks","sum"), TotalOther=("TotalOther","sum"),
            GTN_Pct=("GTN_Pct","mean"), Units=("Units","sum"),
        ).reset_index()
        ann_dash["NetPrice"] = ann_dash["NetSales"]  / ann_dash["Units"]
        ann_dash["NetPct"]   = ann_dash["NetSales"]  / ann_dash["GrossSales"] * 100
        total_net   = ann_dash["NetSales"].sum()
        total_ded   = ann_dash["TotalDeductions"].sum()
        avg_gtn_pct = total_ded / total_gross * 100
        total_reb   = ann_dash["TotalRebates"].sum()
        total_cb    = ann_dash["TotalChargebacks"].sum()
        total_other = ann_dash["TotalOther"].sum()
    else:
        total_net = total_ded = avg_gtn_pct = 0

    # ── KPI Banner ────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#001C4A 0%,#050a14 100%);border:1px solid #6AB4F0;
    border-radius:12px;padding:18px 24px;margin-bottom:16px;'>
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:14px;'>
    <span style='font-family:Syne;font-size:1.1rem;font-weight:800;color:#A8D5FF;'>{product_name}</span>
    <span style='background:#003A8C;color:#D4EAFF;border:1px solid #6AB4F0;border-radius:8px;
    padding:3px 10px;font-size:0.72rem;font-family:JetBrains Mono;'>{therapy_area}</span>
    <span style='background:#003A8C;color:#D4EAFF;border:1px solid #6AB4F0;border-radius:8px;
    padding:3px 10px;font-size:0.72rem;font-family:JetBrains Mono;'>{admin_route.split("(")[0].strip()}</span>
    <span style='background:#003A8C;color:#D4EAFF;border:1px solid #6AB4F0;border-radius:8px;
    padding:3px 10px;font-size:0.72rem;font-family:JetBrains Mono;'>
    {forecast_years[0]}–{forecast_years[-1]} · {n_years}yr</span>
    </div></div>""", unsafe_allow_html=True)

    k1,k2,k3,k4,k5,k6,k7 = st.columns(7)
    k1.metric("Total Units", fmt_u(total_units))
    k2.metric("Gross Sales", fmt_b(total_gross) if total_gross>=1e9 else fmt_m(total_gross))
    k3.metric("Net Sales",   fmt_b(total_net)   if total_net  >=1e9 else fmt_m(total_net) if has_data else "—")
    k4.metric("Total Deductions", fmt_m(total_ded) if has_data else "—")
    k5.metric("Avg GTN %",  fmt_pct(avg_gtn_pct) if has_data else "—")
    k6.metric("Peak Sales Year", str(peak_yr))
    k7.metric("Channels", str(len(CHANNELS)))

    if not has_data:
        st.markdown("""<div class='info-box'>
        ℹ️ <b>Visit the ASP Engine tab first</b> to unlock full GTN data.
        Gross sales charts are live below.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Row 1: Total Sales Over Time + GTN Waterfall ─────────────────
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="sec-header">📈 Total Sales Over Time — Gross vs Net</div>', unsafe_allow_html=True)
        fig_sales = go.Figure()
        fig_sales.add_trace(go.Bar(
            x=fc["Year"], y=gross_by_yr/1e6,
            name="Gross Sales", marker_color="#A8D5FF", opacity=0.6,
            hovertemplate="<b>%{x}</b><br>Gross: $%{y:.2f}M<extra></extra>",
        ))
        if has_data:
            fig_sales.add_trace(go.Bar(
                x=ann_dash["Year"], y=ann_dash["NetSales"]/1e6,
                name="Net Sales", marker_color="#4ade80", opacity=0.85,
                hovertemplate="<b>%{x}</b><br>Net: $%{y:.2f}M<extra></extra>",
            ))
            # GTN deduction fill
            fig_sales.add_trace(go.Scatter(
                x=ann_dash["Year"].tolist() + ann_dash["Year"].tolist()[::-1],
                y=(gross_by_yr/1e6).tolist() + (ann_dash["NetSales"]/1e6).tolist()[::-1],
                fill="toself", fillcolor="rgba(248,113,113,0.10)",
                line=dict(color="rgba(0,0,0,0)"), name="GTN Deductions",
                hoverinfo="skip",
            ))
            # WAC trend line
            fig_sales.add_trace(go.Scatter(
                x=fc["Year"], y=fc["WAC per Unit"],
                name="WAC/unit ($)", mode="lines+markers",
                line=dict(color="#fbbf24", width=1.5, dash="dot"),
                marker=dict(size=5), yaxis="y2",
            ))
        fig_sales.update_layout(
            barmode="overlay", height=340, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
            yaxis=dict(title="Sales ($M)", gridcolor="#003A8C", zerolinecolor="#003A8C"),
            yaxis2=dict(title="WAC ($/unit)", overlaying="y", side="right",
                        gridcolor="#003A8C", zerolinecolor="#003A8C"),
            legend_font_size=10,
        )
        apply_axes_style(fig_sales)
        st.plotly_chart(fig_sales, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-header">📉 GTN Waterfall — Full Forecast Period</div>', unsafe_allow_html=True)
        if has_data:
            wf_labels = ["Gross Sales","(-) Rebates","(-) Chargebacks","(-) Fees/Other","Net Sales"]
            wf_vals   = [total_gross, -total_reb, -total_cb, -total_other, total_net]
            wf_measure= ["absolute","relative","relative","relative","total"]
            wf_pcts   = ["100%",
                         f"-{total_reb/total_gross*100:.1f}%",
                         f"-{total_cb/total_gross*100:.1f}%",
                         f"-{total_other/total_gross*100:.1f}%",
                         f"{total_net/total_gross*100:.1f}%"]
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
                textfont=dict(color="#C8C2BE", size=10),
            ))
            fig_wfall.update_layout(
                title=f"GTN Waterfall {forecast_years[0]}–{forecast_years[-1]}",
                height=340, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
                showlegend=False,
                yaxis=dict(title="$M", gridcolor="#003A8C", zerolinecolor="#003A8C"),
            )
            apply_axes_style(fig_wfall)
            st.plotly_chart(fig_wfall, use_container_width=True)
        else:
            st.markdown("""<div class='card' style='height:300px;display:flex;align-items:center;
            justify-content:center;flex-direction:column;gap:8px;'>
            <span style='font-size:1.5rem;'>📉</span>
            <span style='color:#A09A96;font-size:0.85rem;'>Run ASP Engine tab to unlock waterfall</span>
            </div>""", unsafe_allow_html=True)

    # ── Row 2: Annual deduction breakdown + GTN% trend ────────────────
    col3, col4 = st.columns([1.2, 1])

    with col3:
        st.markdown('<div class="sec-header">🧩 Gross-to-Net Deduction Breakdown by Year</div>', unsafe_allow_html=True)
        if has_data:
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
                textposition="top center", textfont=dict(size=9, color="#A8D5FF"),
            ))
            fig_ded.update_layout(
                barmode="stack", height=300, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
                yaxis=dict(title="% of Gross", gridcolor="#003A8C", zerolinecolor="#003A8C"),
                legend_font_size=10,
            )
            apply_axes_style(fig_ded)
            st.plotly_chart(fig_ded, use_container_width=True)
        else:
            st.markdown("<div class='card' style='height:260px;display:flex;align-items:center;justify-content:center;'><span style='color:#A09A96;'>Run ASP Engine to unlock</span></div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="sec-header">🥧 Payer Channel Mix</div>', unsafe_allow_html=True)
        ch_raw = st.session_state.channel_alloc_raw
        yr_pie_options = [str(y) for y in forecast_years]
        yr_pie_sel = st.selectbox("Year", yr_pie_options, index=0, key="dash_pie_yr",
                                   label_visibility="collapsed")
        yr_pie_int = int(yr_pie_sel)
        row_pie = ch_raw[ch_raw["Year"]==yr_pie_int].iloc[0] if yr_pie_int in ch_raw["Year"].values else ch_raw.iloc[0]
        vals_pie = [row_pie[ch] for ch in CHANNELS]
        fig_pie = go.Figure(go.Pie(
            labels=CHANNELS, values=vals_pie, hole=0.44,
            marker_colors=COLORS_MAIN, textfont_size=9,
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
        ))
        fig_pie.update_layout(
            paper_bgcolor="#001C4A", font_color="#C8C2BE", height=280,
            margin=dict(t=10, b=10, l=5, r=5),
            showlegend=True, legend=dict(font_size=9, bgcolor="#001C4A"),
            annotations=[dict(text=yr_pie_sel, x=0.5, y=0.5, showarrow=False,
                              font=dict(size=16, color="#A8D5FF", family="Syne"))],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Row 3: Customer / IDN Summary ────────────────────────────────
    st.markdown('<div class="sec-header">🏥 Customer / IDN Summary</div>', unsafe_allow_html=True)
    idn_list = st.session_state.idn_list
    idn_cols = st.columns(len(idn_list))
    for i, idn in enumerate(idn_list):
        wac_y1 = fc["WAC per Unit"].iloc[0]
        acq    = wac_y1 * (1 - idn["discount"]/100)
        with idn_cols[i]:
            flag = "🟡 340B" if idn["is_340b"] else "🔵 GPO"
            st.markdown(f"""
            <div style='background:#002766;border:1px solid #6AB4F0;border-radius:10px;
            padding:12px 14px;text-align:center;'>
            <div style='font-family:Syne;font-size:0.82rem;font-weight:700;color:#A8D5FF;
            margin-bottom:6px;'>{idn["name"]}</div>
            <div style='font-size:0.68rem;color:#A09A96;margin-bottom:8px;'>{flag}</div>
            <div style='font-family:JetBrains Mono;font-size:0.95rem;color:#F1ECE9;'>{idn["discount"]}% off WAC</div>
            <div style='font-family:JetBrains Mono;font-size:0.8rem;color:#4ade80;'>{fmt_d(acq)}/unit</div>
            <div style='font-size:0.7rem;color:#A09A96;margin-top:4px;'>{idn["volume_pct"]}% of B&B vol</div>
            </div>""", unsafe_allow_html=True)

    # ── Row 4: Full product summary table ────────────────────────────
    st.markdown('<div class="sec-header">📋 Product Summary — All Years</div>', unsafe_allow_html=True)

    # Safe single-value lookup — returns default if year not found
    def _v(df, yr_col, yr, val_col, default=0.0):
        rows = df.loc[df[yr_col] == yr, val_col]
        return rows.values[0] if len(rows) > 0 else default

    if has_data:
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
            ] for yr in fc["Year"].tolist()}
        })
    else:
        u_by_yr = dict(zip(fc["Year"], fc["Annual Units"]))
        w_by_yr = dict(zip(fc["Year"], fc["WAC per Unit"]))
        dash_T = pd.DataFrame({
            "Metric": ["Annual Units","WAC/Unit","Gross Sales ($M)"],
            **{str(yr): [
                fmt_u(int(u_by_yr.get(yr, 0))),
                fmt_d(w_by_yr.get(yr, 0.0)),
                f"${u_by_yr.get(yr,0) * w_by_yr.get(yr,0) / 1e6:.2f}M",
            ] for yr in fc["Year"].tolist()}
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
                         margin=dict(t=40,b=20,l=10,r=20))
    fig_fc.update_yaxes(title_text="Units (K)", secondary_y=False)
    fig_fc.update_yaxes(title_text="Gross Sales ($M)", secondary_y=True)
    apply_axes_style(fig_fc)
    st.plotly_chart(fig_fc, use_container_width=True)

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
                         barmode="group", height=280, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT)
    apply_axes_style(fig_mo)
    st.plotly_chart(fig_mo, use_container_width=True)

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
                               margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT, yaxis2=dict(overlaying="y", side="right",
                               title="WAC Inc. %", gridcolor="#003A8C"))
        apply_axes_style(fig_wac)
        st.plotly_chart(fig_wac, use_container_width=True)
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

    # ── Init session state for channel steppers ──
    ch_src = st.session_state.channel_alloc_raw.set_index("Year")
    for yr in forecast_years:
        for ch in CHANNELS:
            key = f"ch_{ch}_{yr}".replace("/","_").replace(" ","_")
            if key not in st.session_state:
                st.session_state[key] = float(ch_src.loc[yr, ch]) if yr in ch_src.index else 5.0

    # ── Transposed stepper grid: rows = channels, cols = years ──
    st.caption("Use ＋/－ buttons or type directly. Each year column must sum to 100%.")

    # Header row: year labels
    hdr_cols = st.columns([2] + [1]*len(forecast_years))
    hdr_cols[0].markdown("<div style='font-size:0.72rem;color:#A09A96;text-transform:uppercase;letter-spacing:0.5px;padding:6px 0;font-family:JetBrains Mono;'>Channel</div>", unsafe_allow_html=True)
    for j, yr in enumerate(forecast_years):
        hdr_cols[j+1].markdown(f"<div style='font-size:0.8rem;font-weight:700;color:#A8D5FF;text-align:center;padding:6px 0;font-family:Syne;'>{yr}</div>", unsafe_allow_html=True)

    ch_values = {yr: {} for yr in forecast_years}
    for ch in CHANNELS:
        row_cols = st.columns([2] + [1]*len(forecast_years))
        row_cols[0].markdown(f"<div style='font-size:0.75rem;color:#D4EAFF;padding:8px 4px;line-height:1.3;'>{ch}</div>", unsafe_allow_html=True)
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

    # Validation row — show sum per year
    val_cols = st.columns([2] + [1]*len(forecast_years))
    val_cols[0].markdown("<div style='font-size:0.72rem;color:#A09A96;padding:6px 4px;font-family:JetBrains Mono;'>Σ Total %</div>", unsafe_allow_html=True)
    all_valid = True
    for j, yr in enumerate(forecast_years):
        yr_sum = sum(ch_values[yr].values())
        ok = abs(yr_sum - 100) < 0.6
        if not ok: all_valid = False
        color = "#4ade80" if ok else "#f87171"
        val_cols[j+1].markdown(f"<div style='text-align:center;font-family:JetBrains Mono;font-size:0.8rem;font-weight:700;color:{color};padding:4px 0;'>{yr_sum:.1f}%</div>", unsafe_allow_html=True)

    if all_valid:
        st.markdown("<div class='card card-success' style='padding:8px 14px;'>✅ All years sum to ~100% — allocation valid.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='card card-warn' style='padding:8px 14px;'>⚠️ One or more years don't sum to 100% — check red totals above.</div>", unsafe_allow_html=True)

    # Rebuild channel_alloc_raw from steppers
    ch_rows = []
    for yr in forecast_years:
        row = {"Year": yr}
        row.update(ch_values[yr])
        ch_rows.append(row)
    ch_edited_df = pd.DataFrame(ch_rows)
    st.session_state.channel_alloc_raw = ch_edited_df
    ch_edited = ch_edited_df

    # Stacked area chart
    st.markdown('<div class="sec-header">📊 Channel Mix Evolution (Area Chart)</div>', unsafe_allow_html=True)
    fig_ch = go.Figure()
    for i, ch in enumerate(CHANNELS):
        fig_ch.add_trace(go.Scatter(
            x=ch_edited["Year"], y=ch_edited[ch],
            name=ch, stackgroup="one", mode="none",
            fillcolor=hex_to_rgba(COLORS_MAIN[i % len(COLORS_MAIN)], alpha=0.73),
            hovertemplate=f"<b>{ch}</b><br>%{{y:.1f}}%<extra></extra>",
        ))
    fig_ch.update_layout(title="Payer Channel Mix % by Year", height=350, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
                         yaxis_title="Share (%)")
    apply_axes_style(fig_ch)
    st.plotly_chart(fig_ch, use_container_width=True)

    # Per-year pie grid
    st.markdown('<div class="sec-header">🥧 Channel Mix Snapshots</div>', unsafe_allow_html=True)
    display_years = ch_edited["Year"].tolist()[:6]
    cols = st.columns(min(len(display_years), 3))
    for idx, yr in enumerate(display_years[:6]):
        row = ch_edited[ch_edited["Year"] == yr].iloc[0]
        vals = [row[ch] for ch in CHANNELS]
        fig_p = go.Figure(go.Pie(
            labels=CHANNELS, values=vals, hole=0.4,
            marker_colors=COLORS_MAIN, textfont_size=8,
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
        ))
        fig_p.update_layout(paper_bgcolor="#001C4A", font_color="#C8C2BE",
                            height=220, margin=dict(t=30, b=10, l=5, r=5),
                            title=str(yr), title_font=dict(size=13, color="#A8D5FF"),
                            showlegend=False)
        with cols[idx % 3]:
            st.plotly_chart(fig_p, use_container_width=True)


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
    /* Contract-terms: brand palette overrides */
    [data-testid="stNumberInput"] input {
        min-width: 72px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-align: center !important;
        color: #F1ECE9 !important;
        background: #002766 !important;
    }
    .ct-section-bg {
        background: #002766;
        border: 1px solid #003A8C;
        border-radius: 10px;
        padding: 14px 18px 10px 18px;
        margin-bottom: 16px;
    }
    .ct-year-hdr {
        font-family: 'Syne', sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        color: #A8D5FF;
        text-align: center;
        padding: 4px 0 6px 0;
        border-bottom: 2px solid #6AB4F0;
        margin-bottom: 4px;
    }
    .ct-metric-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #D4EAFF;
        padding: 9px 4px 4px 4px;
        white-space: nowrap;
    }
    .ct-caption {
        font-size: 0.73rem;
        color: #C8C2BE;
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
        hdr_cols[0].markdown("<div class='ct-metric-lbl' style='color:#A09A96;'>Metric</div>",
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
                               yaxis_title="Rebate %", legend_font_size=10)
        apply_axes_style(fig_reb)
        st.plotly_chart(fig_reb, use_container_width=True)

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
                               yaxis_title="Discount %", legend_font_size=10)
        apply_axes_style(fig_disc)
        st.plotly_chart(fig_disc, use_container_width=True)

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
                                       textposition="top center", textfont=dict(size=9, color="#A8D5FF"),
                                       marker=dict(size=8), yaxis="y"))
    fig_gtn_prev.update_layout(barmode="stack", title="Blended GTN % by Year (Indicative)",
                                height=280, **PLOTLY_LAYOUT, yaxis_title="GTN %",
                                legend_font_size=10)
    apply_axes_style(fig_gtn_prev)
    st.plotly_chart(fig_gtn_prev, use_container_width=True)


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
                                   font=dict(color="#C8C2BE", size=10))
        fig_asp.update_layout(title="ASP Trend — Rolling 6-Month Weighted Average",
                               height=340, **PLOTLY_LAYOUT, yaxis_title="$/unit",
                               xaxis_tickangle=-45, xaxis_nticks=n_years*2)
        apply_axes_style(fig_asp)
        st.plotly_chart(fig_asp, use_container_width=True)

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
                               **PLOTLY_LAYOUT, yaxis_title="$/unit")
        apply_axes_style(fig_ann)
        st.plotly_chart(fig_ann, use_container_width=True)

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
        st.markdown("""<div class='card'>
        <b style='color:#A8D5FF;'>Step 1 — Identify ASP-Eligible Channels</b>
        <table style='width:100%;font-size:0.78rem;margin-top:8px;'>
        <tr><th style='color:#C8C2BE;text-align:left;'>Channel</th><th style='color:#C8C2BE;'>ASP Eligible?</th></tr>
        """, unsafe_allow_html=True)
        for ch, eligible in ASP_ELIGIBLE.items():
            color = "#4ade80" if eligible else "#f87171"
            tag = "✅ Included" if eligible else "❌ Exempt"
            st.markdown(f"<tr><td style='color:#F1ECE9;padding:3px 0;'>{ch}</td><td style='color:{color};font-family:JetBrains Mono;font-size:0.75rem;'>{tag}</td></tr>",
                        unsafe_allow_html=True)
        st.markdown("</table></div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("""<div class='card'>
        <b style='color:#A8D5FF;'>Step 2 — Monthly ASP Computation</b>
        <div style='margin-top:10px;font-size:0.8rem;color:#C8C2BE;line-height:1.7;'>
        For each month <em>t</em>:<br>
        <code style='color:#4ade80;'>ASP_t = Σ(price_i × units_i) / Σ(units_i)</code><br>
        where <em>i</em> = non-exempt channels only<br><br>
        <b style='color:#F1ECE9;'>Step 3 — Rolling 6-Month Average</b><br>
        <code style='color:#4ade80;'>ASP_rolling = Σ(rev_{t-5..t}) / Σ(units_{t-5..t})</code><br>
        (volume-weighted, not simple average)<br><br>
        <b style='color:#F1ECE9;'>Step 4 — Medicare Reimbursement</b><br>
        <code style='color:#4ade80;'>Medicare B Reimb = ASP_rolling × 1.06</code><br>
        (pre-sequestration; effective = × 1.04 post-seq)<br><br>
        <b style='color:#F1ECE9;'>Step 5 — Reporting Lag</b><br>
        ASP published ~2 quarters after the reference period.
        Model uses concurrent ASP for simplification — add lag for sensitivity analysis.
        </div></div>""", unsafe_allow_html=True)

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
    # ASP RESCUE SIMULATOR
    # ═══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#050f05 0%,#050a18 100%);
    border:1px solid #0a4a20;border-radius:12px;padding:16px 22px;margin:8px 0;'>
    <div style='font-family:Syne;font-weight:800;font-size:1.1rem;color:#4ade80;margin-bottom:6px;'>
    🎯 ASP Rescue Simulator</div>
    <div style='font-size:0.82rem;color:#C8C2BE;line-height:1.6;'>
    Adjust contract terms below and watch the 6-month rolling ASP recalculate in real time.
    The goal: find the combination of GPO/IDN discounts and channel mix that lifts ASP
    <b style='color:#4ade80;'>above the IDN acquisition floor</b> — turning 🚩 flags into ✅ clean status.
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
        <div style='font-size:0.7rem;color:#A09A96;font-family:JetBrains Mono;'>
        TRACKED IDN ACQUISITION FLOOR</div>
        <div style='font-family:JetBrains Mono;font-size:1.1rem;font-weight:700;color:#f87171;'>
        {fmt_d(idn_acq_sim)}/unit</div>
        <div style='font-size:0.7rem;color:#A09A96;'>({tracked_idn["discount"]}% off WAC
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
            yaxis_title="$/unit", xaxis_tickangle=-45,
        )
        apply_axes_style(fig_sim)
        st.plotly_chart(fig_sim, use_container_width=True)

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
                <div style='background:#002766;border:1px solid {"#0a4020" if rescued else "#5c1a1a"};
                border-radius:9px;padding:10px 8px;text-align:center;'>
                <div style='font-family:Syne;font-weight:700;color:#C8C2BE;font-size:0.75rem;'>{yr}</div>
                <div style='font-size:1.1rem;margin:4px 0;'>{icon}</div>
                <div style='font-family:JetBrains Mono;font-size:0.75rem;color:{color};
                font-weight:700;'>{status}</div>
                <div style='font-size:0.68rem;color:#A09A96;margin-top:4px;font-family:JetBrains Mono;'>
                Base: {fmt_d(b_asp)}</div>
                <div style='font-size:0.68rem;color:#F1ECE9;font-family:JetBrains Mono;'>
                Scen: {fmt_d(s_asp)}</div>
                <div style='font-size:0.68rem;color:{delta_color};font-family:JetBrains Mono;'>
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
                <div style='background:#002766;border:1px solid #6AB4F0;border-radius:8px;
                padding:14px 18px;'>
                <span style='color:#C8C2BE;font-size:0.8rem;'>To make <b style='color:#A8D5FF;'>
                Scenario ASP ≥ {fmt_d(idn_acq_sim)}</b> (IDN floor), GPO discount must be
                <b style='color:{be_color};font-family:JetBrains Mono;'>≤ {be_disc:.1f}%</b>
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
                          height=380, **PLOTLY_LAYOUT, yaxis_title="$M", legend_font_size=11)
    apply_axes_style(fig_wf)
    st.plotly_chart(fig_wf, use_container_width=True)

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
                                  **PLOTLY_LAYOUT, margin=dict(t=40,b=20,l=10,r=20))
        fig_gtnpct.update_yaxes(title_text="GTN %", secondary_y=False)
        fig_gtnpct.update_yaxes(title_text="Net $/Unit", secondary_y=True)
        apply_axes_style(fig_gtnpct)
        st.plotly_chart(fig_gtnpct, use_container_width=True)

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
                                **PLOTLY_LAYOUT, yaxis_title="%", legend_font_size=10)
        apply_axes_style(fig_dmix)
        st.plotly_chart(fig_dmix, use_container_width=True)

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
                              yaxis=dict(title="$M", gridcolor="#003A8C", zerolinecolor="#003A8C"),
                              yaxis2=dict(title="GTN %", overlaying="y", side="right",
                                          gridcolor="#003A8C", zerolinecolor="#003A8C"))
    st.plotly_chart(fig_mo_gtn, use_container_width=True)


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

    st.markdown("""<div class='info-box'>
    <b>Buy & Bill mechanics:</b> Provider purchases drug at IDN/GPO contract price,
    administers to patient, then bills Medicare at <b>ASP + 6%</b>.
    Manufacturer revenue = IDN acquisition price. Provider margin = ASP+6% − Acquisition.
    When acquisition &lt; ASP the provider earns an above-average spread, which also
    gradually erodes future ASP through the 6-month rolling calculation.
    </div>""", unsafe_allow_html=True)

    # ── IDN Configuration ─────────────────────────────────────────────
    st.markdown('<div class="sec-header">⚙️ IDN Configuration — Add / Edit Customers</div>', unsafe_allow_html=True)

    # Init IDN list
    if "idn_list" not in st.session_state:
        st.session_state.idn_list = [
            {"name": "IDN-A (Academic Medical)",   "discount": 20.0, "volume_pct": 30.0, "is_340b": False},
            {"name": "IDN-B (Community Hospital)", "discount": 18.0, "volume_pct": 25.0, "is_340b": False},
            {"name": "IDN-C (340B Entity)",        "discount": 25.6, "volume_pct": 15.0, "is_340b": True},
            {"name": "IDN-D (GPO Member)",         "discount": 15.0, "volume_pct": 20.0, "is_340b": False},
            {"name": "IDN-E (VA Affiliate)",       "discount": 24.0, "volume_pct": 10.0, "is_340b": False},
        ]

    btn_cols = st.columns([1, 1, 4])
    with btn_cols[0]:
        if st.button("➕ Add IDN", use_container_width=True):
            st.session_state.idn_list.append({
                "name": f"IDN-{chr(65+len(st.session_state.idn_list))} (New)",
                "discount": 15.0, "volume_pct": 10.0, "is_340b": False,
            })
    with btn_cols[1]:
        if st.button("🗑️ Remove Last", use_container_width=True) and len(st.session_state.idn_list) > 1:
            st.session_state.idn_list.pop()

    # IDN editor — one row per IDN
    idn_list = st.session_state.idn_list
    n_idn    = len(idn_list)

    # Column headers
    hdr_c = st.columns([0.3, 2.2, 1.2, 1.2, 0.8])
    for hc, lbl in zip(hdr_c, ["#", "IDN Name", "Discount % off WAC", "% of B&B Volume", "340B"]):
        hc.markdown(f"<div style='font-size:0.68rem;color:#A09A96;text-transform:uppercase;"
                    f"font-family:JetBrains Mono;padding:4px 2px;'>{lbl}</div>",
                    unsafe_allow_html=True)

    updated_idn = []
    for i, idn in enumerate(idn_list):
        row_c = st.columns([0.3, 2.2, 1.2, 1.2, 0.8])
        with row_c[0]:
            st.markdown(f"<div style='font-family:Syne;font-weight:700;color:#A8D5FF;"
                        f"font-size:0.85rem;padding:8px 4px;'>#{i+1}</div>",
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

    # Vol % validation
    total_vol = sum(x["volume_pct"] for x in updated_idn)
    if abs(total_vol - 100) > 1:
        st.markdown(f"<div class='card card-warn' style='padding:8px 14px;'>⚠️ IDN volume %s sum to {total_vol:.1f}% — should be 100%</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='card card-success' style='padding:8px 14px;'>✅ IDN volume allocation = {total_vol:.1f}%</div>", unsafe_allow_html=True)

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
            below_asp    = acq < asp
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
            # Flag years where acquisition < ASP
            for _, r in sub[sub["Below_ASP"]].iterrows():
                fig_all.add_vrect(
                    x0=r["Year"]-0.45, x1=r["Year"]+0.45,
                    fillcolor=color, opacity=0.05, line_width=0,
                )
        fig_all.update_layout(
            title="Price Comparison: WAC / ASP / All IDN Acquisitions",
            height=400, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT, yaxis_title="$/unit",
        )
        fig_all.update_layout(legend=dict(
            bgcolor="#002766", bordercolor="#003A8C", font_size=10,
            orientation="v", x=1.01, xanchor="left",
        ))
        apply_axes_style(fig_all)
        st.plotly_chart(fig_all, use_container_width=True)

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
            colorscale=[[0,"#3d0a0a"],[0.4,"#fbbf24"],[1,"#4ade80"]],
            text=[[fmt_d(v) for v in row] for row in spread_matrix],
            texttemplate="%{text}",
            textfont=dict(size=9, family="JetBrains Mono"),
            hovertemplate="<b>%{y}</b><br>%{x}: Spread %{z:.0f}<extra></extra>",
            colorbar=dict(title="Spread $", tickfont=dict(size=9)),
        ))
        fig_heat.update_layout(
            title="Provider Spread (ASP+6% − Acq.) Heatmap",
            height=280, margin=PLOTLY_MARGIN, **PLOTLY_LAYOUT,
        )
        apply_axes_style(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)

    # ── Per-IDN Flag Cards ────────────────────────────────────────────
    st.markdown('<div class="sec-header">🚩 ASP vs Acquisition Flags — Per IDN Per Year</div>', unsafe_allow_html=True)
    flag_cols = st.columns(n_idn)
    for i, idn in enumerate(updated_idn):
        sub = idn_df[idn_df["IDN"]==idn["name"]].sort_values("Year")
        with flag_cols[i]:
            any_flag = sub["Below_ASP"].any()
            header_color = "#f87171" if any_flag else "#4ade80"
            st.markdown(f"""
            <div style='border:1px solid {"#5c1a1a" if any_flag else "#0a3020"};
            background:{"#140505" if any_flag else "#05130c"};
            border-radius:9px;padding:10px 12px;margin-bottom:4px;'>
            <div style='font-family:Syne;font-size:0.8rem;font-weight:700;
            color:{header_color};margin-bottom:6px;'>{idn["name"]}</div>
            <div style='font-size:0.68rem;color:#A09A96;margin-bottom:6px;'>
            {"🟡 340B" if idn["is_340b"] else "🔵 GPO"} · {idn["discount"]}% off WAC</div>
            """, unsafe_allow_html=True)
            for _, row in sub.iterrows():
                flag  = row["Below_ASP"]
                color = "#f87171" if flag else "#4ade80"
                icon  = "🚩" if flag else "✅"
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                padding:3px 0;border-bottom:1px solid #003A8C;font-size:0.73rem;'>
                <span style='color:#C8C2BE;font-family:JetBrains Mono;'>{int(row["Year"])}</span>
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
            yaxis=dict(title="$M", gridcolor="#003A8C", zerolinecolor="#003A8C"),
            legend_font_size=9,
        )
        apply_axes_style(fig_mfr)
        st.plotly_chart(fig_mfr, use_container_width=True)

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
            yaxis=dict(title="$M", gridcolor="#003A8C", zerolinecolor="#003A8C"),
            legend_font_size=9,
        )
        apply_axes_style(fig_prov2)
        st.plotly_chart(fig_prov2, use_container_width=True)

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
        col_h.markdown(f"<div style='font-size:0.7rem;color:#A09A96;text-transform:uppercase;"
                       f"font-family:JetBrains Mono;padding:4px 0;'>{label}</div>",
                       unsafe_allow_html=True)

    # Reference row
    ref_row = st.columns([2.2, 1, 1, 1, 1, 1, 1])
    for rc, val in zip(ref_row, ["── Reference ──", fmt_d(wac_sel), fmt_d(asp_sel),
                                  fmt_d(asp6_sel), "—", "—", "—"]):
        rc.markdown(f"<div style='font-size:0.75rem;color:#A09A96;padding:4px 2px;"
                    f"font-family:JetBrains Mono;'>{val}</div>", unsafe_allow_html=True)

    for _, row in yr_sub.iterrows():
        flag   = row["Below_ASP"]
        color  = "#f87171" if flag else "#4ade80"
        icon   = "🚩 ACQ < ASP" if flag else "✅ Clean"
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
        colors = ["#F1ECE9","#fbbf24","#4ade80","#A8D5FF","#f87171",
                  "#4ade80" if row["Spread"]>0 else "#f87171", color]
        for rc, v, c in zip(r_cols, vals, colors):
            rc.markdown(f"<div style='font-size:0.78rem;color:{c};padding:5px 2px;"
                        f"font-family:JetBrains Mono;border-bottom:1px solid #003A8C;'>{v}</div>",
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
            flag = " 🚩" if acq < asp_base*(1+s/100) else ""
            spreads.append(f"{fmt_d(sp)}{flag}")
        sens_data[label] = spreads
    st.dataframe(pd.DataFrame(sens_data), use_container_width=True, hide_index=True)

# ── Footer ──
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#003A8C;font-size:0.72rem;padding:6px;font-family:JetBrains Mono;'>
PharmGTN Pro v3 · Dynamic Multi-Year GTN Engine · For internal forecasting use only
</div>""", unsafe_allow_html=True)