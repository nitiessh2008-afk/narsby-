"""
💡 Narsby • Live Startup Public Procurement Platform
Smart India Hackathon 2026 | Problem Statement: SIH26136 (Govt of Maharashtra)
Startup-friendly public procurement mechanism: identify -> pilot -> validate -> scale.
Light, colourful UI. Public Transparency Home (no login) + role-based Govt / Startup portals.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & LIGHT, COLOURFUL THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Narsby • Startup Procurement Platform",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #0f172a;
        font-size: 17.5px;
    }
    p, span, label, div { font-size: 16.5px; line-height: 1.65; }

    /* ---------- FORCE LIGHT BACKGROUND ON STREAMLIT'S OWN CONTAINERS ---------- */
    /* Streamlit wraps everything in these data-testid containers, which is what
       was actually showing navy — overriding body/html background alone doesn't reach them. */
    [data-testid="stAppViewContainer"], .stApp, body {
        background: linear-gradient(180deg, #f5f7ff 0%, #fbfbff 100%) !important;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }
    [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #ffffff 0%, #f5f3ff 100%) !important;
        border-right: 1px solid #eef2ff;
    }
    [data-testid="stMainBlockContainer"], .main .block-container, .block-container {
        background: transparent !important;
    }
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }
    /* Widget surfaces (selects, inputs, expanders, tabs) — keep them white/light, not dark */
    [data-testid="stExpander"], [data-testid="stForm"] {
        background: #ffffff !important;
        border-radius: 14px !important;
        border: 1.5px solid #eef2ff !important;
    }
    .stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background: #ffffff !important; border-radius: 10px 10px 0 0 !important;
        border: 1.5px solid #eef2ff !important; color: #334155 !important; font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] { background: #eef2ff !important; color: #4338ca !important; }

    /* ---------- FORCE READABLE DARK TEXT EVERYWHERE (fixes leftover white/invisible text
       inherited from Streamlit's dark theme defaults on widgets, labels, tabs, metrics) ---------- */
    :root, .stApp, .main { color: #0f172a; }
    h1, h2, h3, h4, h5, h6 { color: #0f172a !important; }
    [data-testid="stMarkdownContainer"] * { color: #0f172a; }
    [data-testid="stMarkdownContainer"] a { color: #4f46e5; }
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label { color: #0f172a !important; font-weight: 600 !important; }
    [data-testid="stCaptionContainer"], .stCaption { color: #475569 !important; }
    [data-testid="stSelectbox"] div, [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
    [data-testid="stRadio"] label, [data-testid="stRadio"] p, [data-testid="stCheckbox"] label, [data-testid="stCheckbox"] p {
        color: #0f172a !important;
    }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] > div {
        background: #ffffff !important; border: 1.5px solid #dbeafe !important;
    }
    /* ---------- FILE UPLOADER (portfolio / pitch-deck uploads) — fix dark/invisible text ---------- */
    [data-testid="stFileUploader"] {
        background: #ffffff !important; border: 1.5px dashed #c7d2fe !important;
        border-radius: 14px !important; padding: 10px !important;
    }
    [data-testid="stFileUploaderDropzone"] { background: #f8fafc !important; }
    [data-testid="stFileUploaderDropzone"] *, [data-testid="stFileUploaderDropzoneInstructions"] * {
        color: #0f172a !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] svg { fill: #6366f1 !important; }
    [data-testid="stFileUploader"] section button {
        color: #1e1b4b !important; background: #eef2ff !important; border: 1.5px solid #c7d2fe !important;
    }
    [data-testid="stFileUploaderFile"] { background: #ffffff !important; }
    [data-testid="stFileUploaderFile"] * { color: #0f172a !important; }
    [data-testid="stFileUploaderFileName"] { color: #0f172a !important; font-weight: 600 !important; }
    small { color: #64748b !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; }
    [data-testid="stMetricLabel"] { color: #475569 !important; }
    [data-testid="stMetricDelta"] { color: #059669 !important; }
    .stTabs [data-baseweb="tab"] p { color: inherit !important; }
    .stButton button p, .stButton button div, .stButton button span { color: inherit !important; }
    .stButton > button[kind="secondary"] { color: #1e1b4b !important; background: #ffffff !important; border: 1.5px solid #dbeafe !important; }
    .stButton > button[kind="primary"] { color: #ffffff !important; }
    [data-testid="stAlert"] { color: #0f172a !important; }
    [data-testid="stAlert"] p { color: #0f172a !important; }
    [data-testid="stExpander"] summary, [data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span { color: #0f172a !important; font-weight: 700 !important; }
    code { color: #4338ca !important; background: #f1f5ff !important; }
    .stDataFrame, .stTable { color: #0f172a !important; }

    /* ---------- NOTIFICATION BELL ---------- */
    .notif-bell-btn button {
        border-radius: 50px !important; font-size: 20px !important; padding: 6px 16px !important;
        background: #ffffff !important; border: 1.5px solid #eef2ff !important;
    }
    .notif-panel {
        background: #ffffff; border: 1.5px solid #eef2ff; border-radius: 16px; padding: 16px 20px;
        margin-bottom: 18px; box-shadow: 0 8px 24px rgba(99,102,241,0.08);
    }
    .notif-item { padding: 10px 4px; border-bottom: 1px solid #f1f5f9; font-size: 14.5px; color: #0f172a; }
    .notif-item:last-child { border-bottom: none; }
    .notif-date { color: #64748b; font-size: 12.5px; }

    /* ---------- LIGHT, COLOURFUL HERO BANNERS ---------- */
    .hero-banner-public {
        background: linear-gradient(120deg, #ecfeff 0%, #eff6ff 35%, #f5f3ff 70%, #fdf4ff 100%);
        border-radius: 22px;
        padding: 34px 40px;
        color: #1e1b4b;
        margin-bottom: 22px;
        border: 1.5px solid #dbeafe;
        box-shadow: 0 10px 28px rgba(99, 102, 241, 0.08);
    }
    .hero-banner-gov {
        background: linear-gradient(120deg, #eff6ff 0%, #dbeafe 45%, #ede9fe 100%);
        border-radius: 22px;
        padding: 32px 38px;
        color: #1e1b4b;
        margin-bottom: 26px;
        border: 1.5px solid #bfdbfe;
        box-shadow: 0 10px 28px rgba(59, 130, 246, 0.10);
    }
    .hero-banner-startup {
        background: linear-gradient(120deg, #fdf4ff 0%, #fae8ff 40%, #eff6ff 100%);
        border-radius: 22px;
        padding: 32px 38px;
        color: #581c87;
        margin-bottom: 26px;
        border: 1.5px solid #f5d0fe;
        box-shadow: 0 10px 28px rgba(192, 38, 211, 0.08);
    }
    .hero-title { font-size: 30px; font-weight: 900; margin-bottom: 10px; letter-spacing: -0.5px; }
    .hero-subtitle { font-size: 16.5px; margin-bottom: 12px; line-height: 1.6; font-weight: 500; color:#334155;}
    .hero-quote {
        font-size: 14px; font-style: italic; padding: 8px 16px; border-radius: 10px;
        display: inline-block; background: rgba(255,255,255,0.6);
        border-left: 3px solid #6366f1; color:#4338ca;
    }

    .logged-in-pill {
        background: linear-gradient(120deg, #dcfce7 0%, #d1fae5 100%);
        color: #14532d; border: 1.5px solid #86efac; border-radius: 12px;
        padding: 12px 16px; font-weight: 800; font-size: 14.5px; margin-bottom: 20px;
        display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 12px rgba(34,197,94,0.10);
    }
    .gov-badge { background: #fde68a; color: #78350f; font-weight: 800; font-size: 12px; padding: 3px 8px; border-radius: 6px; text-transform: uppercase; }
    .startup-badge { background: #ddd6fe; color: #4c1d95; font-weight: 800; font-size: 12px; padding: 3px 8px; border-radius: 6px; text-transform: uppercase; }
    .public-badge { background: #a7f3d0; color: #065f46; font-weight: 800; font-size: 12px; padding: 3px 8px; border-radius: 6px; text-transform: uppercase; }

    .action-card {
        background: #ffffff; border: 2px solid #eef2ff; border-radius: 18px; padding: 22px;
        height: 100%; display:flex; flex-direction:column; justify-content:space-between;
        box-shadow: 0 4px 14px rgba(99,102,241,0.05); transition: all .2s ease-in-out;
    }
    .action-card:hover { transform: translateY(-4px); border-color:#a5b4fc; box-shadow:0 12px 28px rgba(99,102,241,0.14);}
    .action-title { font-size: 18.5px; font-weight: 800; color:#0f172a; margin-bottom:8px; }
    .action-desc { font-size: 14px; color:#475569; margin-bottom:16px; line-height:1.5; }

    .item-box {
        background:#ffffff; border:1.8px solid #eef2ff; border-radius:16px; padding:22px 26px;
        margin-bottom:18px; box-shadow:0 4px 12px rgba(99,102,241,0.04); transition: border-color .2s ease;
    }
    .item-box:hover { border-color:#c7d2fe; }

    .portfolio-card {
        background: linear-gradient(120deg,#ffffff 0%, #f8fafc 100%);
        border:1.8px solid #e0e7ff; border-left:6px solid #6366f1; border-radius:14px;
        padding:20px 24px; margin-bottom:16px; box-shadow:0 4px 14px rgba(0,0,0,0.03);
    }

    .stat-box { background:#ffffff; border:1.8px solid #eef2ff; border-radius:16px; padding:18px 20px; text-align:left; box-shadow:0 2px 10px rgba(99,102,241,0.05);}
    .stat-label { font-size:13.5px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:.6px; margin-bottom:4px;}
    .stat-val { font-size:26px; font-weight:900; color:#0f172a; }

    .pill-tag { display:inline-block; padding:4px 12px; border-radius:20px; font-size:12.5px; font-weight:800; margin-right:6px;}
    .tag-water { background:#dbeafe; color:#1e40af; }
    .tag-drone { background:#ede9fe; color:#5b21b6; }
    .tag-health { background:#fee2e2; color:#991b1b; }
    .tag-agri { background:#dcfce7; color:#166534; }
    .tag-gov { background:#fef3c7; color:#92400e; }
    .tag-eligible { background:#d1fae5; color:#065f46; }
    .tag-flagged { background:#fee2e2; color:#991b1b; }
    .tag-validated { background:#e0e7ff; color:#3730a3; }

    .template-card {
        background:#ffffff; border:1.8px solid #eef2ff; border-left:6px solid #06b6d4;
        border-radius:14px; padding:18px 22px; margin-bottom:14px; box-shadow:0 4px 12px rgba(6,182,212,0.06);
    }

    .login-shell {
        background: linear-gradient(135deg, #eef2ff 0%, #fdf4ff 100%);
        border-radius: 24px; padding: 6px; box-shadow: 0 20px 45px rgba(99,102,241,0.12);
    }
    .login-hero-panel {
        background: linear-gradient(160deg, #4338ca 0%, #6366f1 45%, #06b6d4 100%);
        border-radius: 20px; padding: 40px 34px; color:#fff; height:100%;
    }
    .login-card {
        background:#ffffff; border-radius:20px; padding: 30px 32px; box-shadow: 0 4px 20px rgba(15,23,42,0.06);
    }
    .login-feature { display:flex; gap:10px; align-items:flex-start; margin-bottom:14px; font-size:14.5px; color:#eef2ff;}

    .stButton > button { font-size:16.5px !important; font-weight:700 !important; padding:10px 22px !important; border-radius:12px !important;}
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        font-size:16.5px !important; border-radius:10px !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. AUTH STORE & IN-MEMORY DATA
# -----------------------------------------------------------------------------
USERS_DB = {
    "rajesh.sharma@maharashtra.gov.in": {
        "password": "gov123", "name": "Dr. Rajesh Sharma (IAS)", "role": "Government Official",
        "dept": "Water Supply & Sanitation Dept, Govt of Maharashtra", "avatar": "🏛️"
    },
    "urban.dev@maharashtra.gov.in": {
        "password": "gov123", "name": "Smt. Manisha Verma (IAS)", "role": "Government Official",
        "dept": "Urban Development & Smart Cities, Govt of Maharashtra", "avatar": "🏛️"
    },
    "founder@jaldrishti.io": {
        "password": "startup123", "name": "Ananya Deshmukh (Founder & CEO)", "role": "Startup Founder",
        "dept": "JalDrishti IoT Pvt Ltd", "dpiit_id": "DIPP-MH-44512", "avatar": "🚀"
    },
    "founder@aerovision.ai": {
        "password": "startup123", "name": "Karan Malhotra (CTO & Co-Founder)", "role": "Startup Founder",
        "dept": "AeroVision AI Robotics Pvt Ltd", "dpiit_id": "DIPP-MH-88124", "avatar": "🚀"
    }
}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_email'] = None
    st.session_state['user_role'] = None
    st.session_state['user_name'] = None
    st.session_state['user_dept'] = None
    st.session_state['active_page'] = 'Dashboard'
    st.session_state['public_tab'] = 'Overview'

if 'initialized' not in st.session_state:
    st.session_state['challenges'] = [
        {
            'id': 'CH-01', 'title': 'Chapter 1: Smart Water Pipeline Leakage & Non-Revenue Loss',
            'dept': 'Water Supply & Sanitation Dept', 'sector': 'Water & Smart City', 'tag': 'water',
            'budget': '₹25 Lakhs', 'duration': '3 Months',
            'target_kpi': 'Reduce subterranean water loss by >= 25% with sub-2m accuracy',
            'description': 'Municipal water distribution loses over 35% non-revenue water. We need non-invasive acoustic IoT sensors to detect bursts without digging whole roads.',
            'posted_by': 'Dr. Rajesh Sharma (IAS)', 'date_posted': '2026-02-10', 'status': 'Active (Accepting Proposals)',
            'eligibility': {'dpiit_required': True, 'max_turnover': '₹50 Cr (last FY)', 'max_age': '10 years since incorporation', 'sector_fit': 'Water/IoT/Sensors'},
            'scale_status': 'Scaling to 4 municipal corporations'
        },
        {
            'id': 'CH-02', 'title': 'Chapter 2: Automated Aerial Drone Road Quality & Pothole Survey',
            'dept': 'Urban Development & Smart Cities', 'sector': 'AI & Drone Mobility', 'tag': 'drone',
            'budget': '₹35 Lakhs', 'duration': '4 Months',
            'target_kpi': 'Survey 50 km/day with >= 90% distress detection accuracy',
            'description': 'Automated drone/camera computer vision survey to map asphalt surface quality, detect potholes, and generate instant repair work orders.',
            'posted_by': 'Smt. Manisha Verma (IAS)', 'date_posted': '2026-02-14', 'status': 'Active (Accepting Proposals)',
            'eligibility': {'dpiit_required': True, 'max_turnover': '₹50 Cr (last FY)', 'max_age': '10 years since incorporation', 'sector_fit': 'Drones/Computer Vision'},
            'scale_status': 'Under technical review'
        },
        {
            'id': 'CH-03', 'title': 'Chapter 3: Portable Rural PHC Edge-AI Vital Screening Kiosk',
            'dept': 'Public Health & Family Welfare', 'sector': 'HealthTech', 'tag': 'health',
            'budget': '₹30 Lakhs', 'duration': '3 Months',
            'target_kpi': 'Under 4-min patient vital screening with 100% offline edge support',
            'description': 'Battery-operated triage kiosk for remote Primary Health Centres with instant tele-ECG and automated cardiovascular risk grading.',
            'posted_by': 'Dr. Nitin Patil (Director of Health)', 'date_posted': '2026-02-18', 'status': 'Active (Accepting Proposals)',
            'eligibility': {'dpiit_required': True, 'max_turnover': '₹50 Cr (last FY)', 'max_age': '10 years since incorporation', 'sector_fit': 'HealthTech/MedTech'},
            'scale_status': 'Not yet piloted'
        },
        {
            'id': 'CH-04', 'title': 'Chapter 4: Hyper-Local Solar Pest Early Warning Sensor Traps',
            'dept': 'Agriculture & Farmers Welfare', 'sector': 'Agritech', 'tag': 'agri',
            'budget': '₹20 Lakhs', 'duration': '3 Months',
            'target_kpi': 'Advance warning >= 7 days before major crop infestation',
            'description': 'Low-cost optical/acoustic insect traps with solar battery and vernacular SMS alerts for Vidarbha cotton & soybean farmers.',
            'posted_by': 'Shri. S. K. Kadam (Agri Commissioner)', 'date_posted': '2026-02-22', 'status': 'Active (Accepting Proposals)',
            'eligibility': {'dpiit_required': True, 'max_turnover': '₹50 Cr (last FY)', 'max_age': '10 years since incorporation', 'sector_fit': 'Agritech/IoT'},
            'scale_status': 'Not yet piloted'
        }
    ]

    st.session_state['proposals'] = [
        {
            'id': 'PROP-101', 'challenge_id': 'CH-01', 'challenge_title': 'Chapter 1: Smart Water Pipeline Leakage & Non-Revenue Loss',
            'startup_name': 'JalDrishti IoT Pvt Ltd', 'founder_email': 'founder@jaldrishti.io', 'dpiit_id': 'DIPP-MH-44512',
            'bid': '₹23,50,000', 'duration': '3 Months', 'trl': 8, 'match_score': 96,
            'status': 'Work Order Issued (Pilot Live)', 'submitted_date': '2026-02-16',
            'solution': 'Piezoelectric acoustic clamp-on sensors with cellular NB-IoT telemetry to isolate underground water leaks with sub-2.0m spatial precision, saving 28% water loss.',
            'proof_attachment': 'JalDrishti_Architecture_Doc.pdf',
            'past_work_ref': 'Municipal Water Leakage Telemetry System for PMC (Pune)',
            'eligibility_check': {'DPIIT Recognised': True, 'Turnover under cap': True, 'Indian-owned & controlled': True, 'Sector fit confirmed': True},
            'eligibility_status': 'Eligible ✅',
            'milestones': [
                {'num': 1, 'title': 'Deploy 60 Sensor Nodes in Ward 4', 'amount': '₹7,05,000', 'status': 'Completed & Paid', 'proof': '60 GPS coordinates verified; telemetry ping latency < 3 mins.', 'validator': 'Quality Council of India (QCI) empanelled auditor'},
                {'num': 2, 'title': 'Live Acoustic Leak Detection & Verification', 'amount': '₹9,40,000', 'status': 'Under Gov Review', 'proof': 'Identified 9 leak points. PWD repair crew confirmed 8 pipe crack repairs.', 'validator': None},
                {'num': 3, 'title': 'Municipal SCADA System Integration', 'amount': '₹7,05,000', 'status': 'Pending Stage 2', 'proof': 'Awaiting Milestone 2 clearance.', 'validator': None}
            ]
        },
        {
            'id': 'PROP-102', 'challenge_id': 'CH-02', 'challenge_title': 'Chapter 2: Automated Aerial Drone Road Quality & Pothole Survey',
            'startup_name': 'AeroVision AI Robotics Pvt Ltd', 'founder_email': 'founder@aerovision.ai', 'dpiit_id': 'DIPP-MH-88124',
            'bid': '₹31,00,000', 'duration': '4 Months', 'trl': 7, 'match_score': 92,
            'status': 'Under Technical Committee Review', 'submitted_date': '2026-02-24',
            'solution': 'Autonomous dual-spectrum camera drones with onboard TensorRT edge AI for sub-5cm pothole classification and automated PWD GIS work order generation.',
            'proof_attachment': 'AeroVision_Pothole_AI_Whitepaper.pdf',
            'past_work_ref': 'Drone Road Condition Mapping for TMC (Thane)',
            'eligibility_check': {'DPIIT Recognised': True, 'Turnover under cap': True, 'Indian-owned & controlled': True, 'Sector fit confirmed': True},
            'eligibility_status': 'Eligible ✅',
            'milestones': [
                {'num': 1, 'title': '50 km Pilot Aerial Road Scan & AI Model Validation', 'amount': '₹9,30,000', 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None},
                {'num': 2, 'title': 'Automated PWD Geo-portal Integration', 'amount': '₹12,40,000', 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None},
                {'num': 3, 'title': 'Full Ward Survey & Defect Analytics', 'amount': '₹9,30,000', 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None}
            ]
        }
    ]

    st.session_state['startup_past_works'] = [
        {
            'title': 'Municipal Water Leakage Telemetry System for PMC (Pune)', 'startup_name': 'JalDrishti IoT Pvt Ltd',
            'client': 'Pune Municipal Corporation (PMC)', 'year': '2024 - 2025', 'sector': 'Water & Smart City',
            'outcome': 'Saved 1.4 Million Litres/day; detected 42 hidden underground bursts.',
            'proof_file': 'PMC_Project_Completion_Certificate.pdf', 'trl_demonstrated': 'TRL 8',
            'live_url': 'https://smartwater.pune.gov.in/jaldrishti-case-study', 'verified': True
        },
        {
            'title': 'Drone Road Condition Mapping for TMC (Thane)', 'startup_name': 'AeroVision AI Robotics Pvt Ltd',
            'client': 'Thane Municipal Corporation (TMC)', 'year': '2024', 'sector': 'AI & Drone Mobility',
            'outcome': 'Mapped 140 km arterial roads; reduced physical survey duration by 85%.',
            'proof_file': 'TMC_Work_Completion_Letter.pdf', 'trl_demonstrated': 'TRL 7',
            'live_url': 'https://smartthane.gov.in/drone-surveys', 'verified': True
        }
    ]

    # NEW: Scale-up recommendations (populated by Government after a pilot succeeds)
    st.session_state['scale_ups'] = [
        {
            'startup_name': 'JalDrishti IoT Pvt Ltd', 'solution_title': 'Acoustic IoT Water Leak Detection',
            'origin_pilot': 'Pune Municipal Corporation', 'scale_targets': 'Nagpur, Nashik, Aurangabad, Thane Municipal Corporations',
            'recommended_by': 'Dr. Rajesh Sharma (IAS)', 'date': '2026-03-01',
            'impact_so_far': 'Saved 1.4M litres/day in Pune pilot; 28% non-revenue water loss reduction.'
        }
    ]

    # NEW: Standard compliance / procurement templates (per SIH26136 expected outcome)
    st.session_state['templates'] = [
        {
            'title': '📋 Outcome-Based Problem Statement Template',
            'desc': 'Standard format for departments to frame a challenge around a measurable outcome/KPI rather than a fixed technical specification.',
            'content': """OUTCOME-BASED PROBLEM STATEMENT TEMPLATE — Narsby / GFR 194 Sandbox

1. Department & Sponsoring Officer:
2. Sector / Theme:
3. Current Operational Problem (2-3 lines, no solution bias):
4. Target Outcome KPI (must be measurable, e.g. ">=25% reduction in X within Y months"):
5. Sanctioned Sandbox Grant Pool (Rs.):
6. Pilot Duration:
7. Data/Assets the Department will provide to startups:
8. Constraints (regulatory, safety, site-access):
9. Evaluation Weightage: Innovation | Feasibility | Cost | Past Track Record | TRL
10. Contact for Clarifications:
"""
        },
        {
            'title': '🧮 Expert Evaluation & Scoring Rubric',
            'desc': 'Weighted scoring rubric used by the departmental technical committee to evaluate startup proposals fairly and transparently.',
            'content': """EXPERT EVALUATION RUBRIC — Narsby Startup Procurement Sandbox

Criteria                              Weight
--------------------------------------------
Outcome KPI Alignment                  35%
Technology Readiness Level (TRL)       25%
Verified Past Work / Track Record      25%
Cost Competitiveness                   15%
--------------------------------------------
Minimum qualifying score: 70/100
Committee: min. 3 members incl. 1 external domain expert (conflict-of-interest declaration mandatory)
Scores + justification must be published to the startup within 10 working days.
"""
        },
        {
            'title': '🤝 Milestone-Based Pilot / Sandbox Agreement',
            'desc': 'Legally-structured pilot agreement that ties every disbursement to a verifiable milestone rather than upfront payment.',
            'content': """MILESTONE-BASED PILOT AGREEMENT (SANDBOX) — TEMPLATE

Parties: [Government Department] and [Startup Entity, DPIIT No.]
Pilot Duration: ____   Total Sanctioned Grant: Rs. ____
Milestones (min. 3): each with Deliverable, Verifiable Proof, Amount %, Independent Validation requirement.
Exit Clause: Either party may terminate on written notice if a milestone is missed twice.
Liability Cap: Limited to sanctioned grant amount. No penal liability during sandbox phase (GFR 194).
Governing Framework: General Financial Rules 194 (Innovation/Startup procurement exemption).
"""
        },
        {
            'title': '🔐 Data Sharing & IP Ownership Clause',
            'desc': 'Clarifies who owns the background IP, foreground IP created during the pilot, and how government data may be used.',
            'content': """DATA SHARING & IP CLAUSE — TEMPLATE

1. Background IP (pre-existing startup technology) remains with the Startup.
2. Foreground IP (jointly developed during the pilot) is jointly owned unless otherwise agreed in writing.
3. Government data shared for the pilot remains Government property; Startup may not resell, sublicense
   or use it beyond the pilot scope without written consent.
4. On successful scale-up, licensing terms for department-wide/state-wide use to be renegotiated
   under a separate commercial agreement.
5. Data localization: all citizen/operational data must be stored on servers located within India.
"""
        },
        {
            'title': '🛡️ Cybersecurity & Risk Compliance Checklist',
            'desc': 'Minimum security and risk-management bar every pilot must clear before touching government data or infrastructure.',
            'content': """CYBERSECURITY & RISK COMPLIANCE CHECKLIST

[ ] Data encryption at rest and in transit
[ ] No storage of citizen PII outside India
[ ] Role-based access control on all department-facing dashboards
[ ] Vulnerability assessment / penetration test report (for software pilots) before go-live
[ ] Incident response and breach-notification plan (72-hour disclosure)
[ ] Business continuity / data backup plan
[ ] Named Data Protection Officer / point of contact
"""
        },
        {
            'title': '🛒 Procurement Transition & GeM Pathway Note',
            'desc': 'What happens after a pilot succeeds: how it moves from sandbox to compliant procurement / GeM listing / scale-up.',
            'content': """PROCUREMENT TRANSITION PATHWAY — SANDBOX TO SCALE

Step 1: Independent Validation Report confirms KPI achievement.
Step 2: Department issues a Pilot Success Certificate.
Step 3: Startup solution is on-boarded to Government e-Marketplace (GeM) as a listed innovative product/service,
        OR a direct procurement order is issued citing GFR 194 (Innovation exemption from L1 tendering).
Step 4: Scale-up committee reviews replication potential across other districts/departments.
Step 5: Multi-year rate contract may be issued for state-wide scale-up.
"""
        }
    ]
    # NEW: Notifications — upcoming tenders/challenges, deadlines, and pilot milestones
    st.session_state['notifications'] = [
        {'title': '🆕 New Challenge Posted', 'detail': 'Chapter 4: Hyper-Local Solar Pest Early Warning Sensor Traps (Agritech) — ₹20 Lakhs sandbox grant open.', 'date': '2026-02-22'},
        {'title': '⏰ Submission Window Closing Soon', 'detail': 'Chapter 3: Portable Rural PHC Edge-AI Vital Screening Kiosk — proposals close in 5 days.', 'date': '2026-03-05'},
        {'title': '🆕 New Challenge Posted', 'detail': 'Chapter 2: Automated Aerial Drone Road Quality & Pothole Survey (AI & Drone Mobility) — ₹35 Lakhs sandbox grant open.', 'date': '2026-02-14'},
        {'title': '✅ Milestone Independently Validated', 'detail': 'JalDrishti IoT Pvt Ltd — Milestone 1 (Sensor Deployment) cleared by QCI empanelled auditor.', 'date': '2026-02-28'},
        {'title': '🚀 Scale-Up Recommended', 'detail': 'Acoustic IoT Water Leak Detection recommended for scale-up to Nagpur, Nashik, Aurangabad, Thane.', 'date': '2026-03-01'},
    ]
    st.session_state['show_notifications'] = False
    st.session_state['initialized'] = True

# -----------------------------------------------------------------------------
# 3. SHARED SMALL HELPERS
# -----------------------------------------------------------------------------
TAG_CLASS = {'water': 'tag-water', 'drone': 'tag-drone', 'health': 'tag-health', 'agri': 'tag-agri'}

def sector_pill(ch):
    cls = TAG_CLASS.get(ch.get('tag', ''), 'tag-gov')
    return f"<span class='pill-tag {cls}'>{ch['sector']}</span>"

def render_public_overview():
    all_ch = st.session_state['challenges']
    all_props = st.session_state['proposals']
    total_grant_words = "₹1.12 Cr"
    st.markdown("## 🌍 **Public Transparency Overview**")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"<div class='stat-box'><div class='stat-label'>Live Challenges</div><div class='stat-val' style='color:#2563eb;'>{len(all_ch)}</div></div>", unsafe_allow_html=True)
    with s2:
        st.markdown(f"<div class='stat-box'><div class='stat-label'>Proposals Received</div><div class='stat-val' style='color:#7c3aed;'>{len(all_props)}</div></div>", unsafe_allow_html=True)
    with s3:
        st.markdown(f"<div class='stat-box'><div class='stat-label'>Total Sandbox Grants</div><div class='stat-val' style='color:#059669;'>{total_grant_words}</div></div>", unsafe_allow_html=True)
    with s4:
        st.markdown(f"<div class='stat-box'><div class='stat-label'>Avg. Time to Pilot</div><div class='stat-val' style='color:#d97706;'>14 Days</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:22px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        speed_df = pd.DataFrame({
            'Stage': ['Problem Posting', 'Technical Review', 'Sanction Award', 'Payment Release'],
            'Conventional Tender (Days)': [45, 60, 45, 30],
            'Narsby Sandbox (Days)': [2, 5, 4, 3]
        })
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Conventional GFR Tender', x=speed_df['Stage'], y=speed_df['Conventional Tender (Days)'], marker_color='#c7d2fe'))
        fig_bar.add_trace(go.Bar(name='Narsby Sandbox', x=speed_df['Stage'], y=speed_df['Narsby Sandbox (Days)'], marker_color='#6366f1'))
        fig_bar.update_layout(title="Procurement Speed: Conventional vs Sandbox", barmode='group', template='plotly_white', height=340, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)
    with c2:
        sec_df = pd.DataFrame({'Sector': ['Water Tech', 'Drone & AI', 'HealthTech', 'Agritech'], 'Budget (Lakhs)': [25, 35, 30, 20]})
        fig_pie = px.pie(sec_df, values='Budget (Lakhs)', names='Sector', title="Open Grant Allocation by Sector (₹ Lakhs)", hole=0.55,
                          color_discrete_sequence=['#60a5fa', '#a78bfa', '#f472b6', '#34d399'])
        fig_pie.update_layout(template='plotly_white', height=340, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.info("🔗 **Ecosystem Integrations (prototype scope):** DPIIT / Startup India registry for eligibility checks · Government e-Marketplace (GeM) for post-pilot procurement transition · GFR Rule 194 as the legal sandbox basis.")


def render_public_challenges():
    st.markdown("## 📚 **Open Departmental Problem Statements**")
    search_q = st.text_input("🔍 Search open challenges:", placeholder="e.g. Water, Drone, HealthTech, Agritech...", key="pub_search")
    filtered = [c for c in st.session_state['challenges'] if search_q.lower() in c['title'].lower()
                or search_q.lower() in c['dept'].lower() or search_q.lower() in c['sector'].lower()]
    col_l, col_r = st.columns(2)
    for idx, ch in enumerate(filtered):
        target = col_l if idx % 2 == 0 else col_r
        with target:
            elig = ch.get('eligibility', {})
            st.markdown(f"""
            <div class="item-box">
                <div style="font-size:19px; font-weight:800; color:#1e1b4b; margin-bottom:6px;">📖 {ch['title']}</div>
                <div style="margin-bottom:8px;">{sector_pill(ch)} <span class='pill-tag tag-gov'>{ch['budget']}</span></div>
                <div style="font-size:14px; color:#64748b; margin-bottom:8px;">Dept: <strong style="color:#0f172a;">{ch['dept']}</strong> · Duration: <strong>{ch['duration']}</strong></div>
                <div style="font-size:14.5px; color:#334155; margin-bottom:10px;">{ch['description']}</div>
                <div style="background:#f8fafc; border-left:4px solid #6366f1; padding:8px 12px; font-size:14px; margin-bottom:10px;">🎯 <strong>Target KPI:</strong> {ch['target_kpi']}</div>
                <div style="font-size:13px; color:#0f172a;">✅ <strong>Eligibility:</strong> DPIIT-recognised · Turnover ≤ {elig.get('max_turnover','—')} · Age ≤ {elig.get('max_age','—')}</div>
            </div>
            """, unsafe_allow_html=True)


def render_public_pilots():
    st.markdown("## 🛰️ **Public Pilot Tracker**")
    st.caption("Independent, milestone-level visibility into every live sandbox pilot — no login required.")
    for prop in st.session_state['proposals']:
        if 'Work Order Issued' not in prop['status']:
            continue
        done = sum(1 for m in prop['milestones'] if m['status'] == 'Completed & Paid')
        st.markdown(f"""
        <div class="item-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0; color:#1e1b4b; font-size:20px; font-weight:800;">{prop['startup_name']}</h3>
                <span class="pill-tag tag-eligible">{done}/{len(prop['milestones'])} Milestones Cleared</span>
            </div>
            <div style="font-size:14.5px; color:#64748b; margin-top:6px;">Challenge: <strong>{prop['challenge_title']}</strong> · Grant: <strong style="color:#4f46e5;">{prop['bid']}</strong></div>
        </div>
        """, unsafe_allow_html=True)
        for m in prop['milestones']:
            badge = "tag-eligible" if m['status'] == 'Completed & Paid' else ("tag-validated" if 'Validation' in m['status'] else "tag-gov")
            val_line = f" · Independently validated by {m['validator']}" if m.get('validator') else ""
            st.markdown(f"<div style='padding:8px 4px; font-size:14.5px;'>▫️ <strong>M{m['num']}: {m['title']}</strong> — <span class='pill-tag {badge}'>{m['status']}</span>{val_line}</div>", unsafe_allow_html=True)


def render_public_scaleups():
    st.markdown("## 🏆 **Success Stories & Scale-Up Decisions**")
    st.caption("Once a pilot independently validates its outcome KPI, departments can formally recommend it for scale-up.")
    if not st.session_state['scale_ups']:
        st.info("No scale-up recommendations issued yet.")
    for su in st.session_state['scale_ups']:
        st.markdown(f"""
        <div class="portfolio-card">
            <div style="font-size:20px; font-weight:800; color:#1e1b4b;">🚀 {su['solution_title']} — {su['startup_name']}</div>
            <div style="font-size:14.5px; color:#64748b; margin:6px 0;">Originating Pilot: <strong>{su['origin_pilot']}</strong> · Recommended by: <strong>{su['recommended_by']}</strong> on {su['date']}</div>
            <div style="background:#ffffff; border:1.5px solid #e0e7ff; padding:12px 16px; border-radius:10px; margin:10px 0;"><strong>🎯 Impact So Far:</strong> {su['impact_so_far']}</div>
            <div style="font-size:14.5px;"><strong>📈 Scale-Up Targets:</strong> {su['scale_targets']}</div>
        </div>
        """, unsafe_allow_html=True)


def render_templates_library(readonly=True):
    st.markdown("## 📄 **Procurement & Compliance Templates Library**")
    st.caption("Standard templates required by SIH26136: problem statement, evaluation rubric, pilot agreement, IP/data clauses, cybersecurity checklist, and the GeM transition pathway.")
    for i, t in enumerate(st.session_state['templates']):
        st.markdown(f"""
        <div class="template-card">
            <div style="font-size:18px; font-weight:800; color:#0f172a;">{t['title']}</div>
            <div style="font-size:14px; color:#475569; margin:6px 0 10px 0;">{t['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("View template content"):
            st.code(t['content'], language=None)
            st.download_button("⬇️ Download as .txt", data=t['content'], file_name=f"{t['title'].split(' ',1)[-1].strip().replace(' ','_')}.txt",
                                key=f"dl_{i}", use_container_width=True)


def render_notification_bell():
    """Top notification bell — shown on every page (public + both logged-in portals)."""
    count = len(st.session_state.get('notifications', []))
    top_l, top_r = st.columns([6, 1])
    with top_l:
        crumb = "🌍 Public Transparency Home" if not st.session_state.get('logged_in') else st.session_state.get('active_page', 'Dashboard')
        st.markdown(
            f"<div style='font-size:14.5px; font-weight:800; color:#6366f1; padding-top:8px;'>"
            f"💡 Narsby <span style='color:#94a3b8; font-weight:600;'>/ {crumb}</span></div>",
            unsafe_allow_html=True
        )
    with top_r:
        st.markdown("<div class='notif-bell-btn'>", unsafe_allow_html=True)
        label = f"🔔 {count}" if count else "🔔"
        if st.button(label, key="notif_bell_toggle", use_container_width=True):
            st.session_state['show_notifications'] = not st.session_state['show_notifications']
        st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.get('show_notifications'):
        st.markdown("<div class='notif-panel'>", unsafe_allow_html=True)
        st.markdown("#### 🔔 Notifications — Upcoming Tenders, Deadlines & Pilot Updates")
        if not st.session_state['notifications']:
            st.caption("No notifications yet.")
        for n in st.session_state['notifications']:
            st.markdown(f"<div class='notif-item'><strong>{n['title']}</strong><br>{n['detail']}<br><span class='notif-date'>{n['date']}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_login_section():
    st.markdown("<div style='margin-top:34px;'></div>", unsafe_allow_html=True)
    st.markdown("## 🔐 **Sign In to Narsby**")
    st.caption("Government officials and DPIIT-recognised startups sign in below. Everything above is public — no login needed to research the platform.")

    st.markdown("<div class='login-shell'>", unsafe_allow_html=True)
    lp1, lp2 = st.columns([1, 1.35])
    with lp1:
        st.markdown("""
        <div class="login-hero-panel">
            <div style="font-size:26px; font-weight:900; margin-bottom:6px;">💡 Narsby</div>
            <div style="font-size:14px; opacity:0.9; margin-bottom:22px;">Govt of Maharashtra · SIH 2026 · GFR 194 Innovation Sandbox</div>
            <div class="login-feature">⚡ <div>Post outcome-based challenges & sanction pilots in days, not months.</div></div>
            <div class="login-feature">🔎 <div>Automated DPIIT eligibility screening for every applicant startup.</div></div>
            <div class="login-feature">🧾 <div>Milestone-based escrow with independent third-party validation.</div></div>
            <div class="login-feature">📈 <div>One-click scale-up recommendation once a pilot succeeds.</div></div>
        </div>
        """, unsafe_allow_html=True)
    with lp2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("#### 👤 Step 1 — Select your portal")
        role_select = st.radio("Select your Portal Persona:",
                                ["🏛️ Government Official (Dept Secretary / Procuring Entity)", "🚀 Startup Founder / DPIIT Innovator"],
                                index=0, label_visibility="collapsed")
        is_gov = "Government Official" in role_select
        selected_role_str = "Government Official" if is_gov else "Startup Founder"

        if is_gov:
            st.markdown("<div style='background:#eff6ff; border:1.5px solid #bfdbfe; border-radius:14px; padding:14px 18px; margin:12px 0;'><strong style='color:#1e40af;'>🏛️ Government Official Access</strong><br><span style='font-size:13.5px; color:#3b82f6;'>Post challenges, screen & evaluate proposals, run independent validation, sanction escrow, and approve scale-ups.</span></div>", unsafe_allow_html=True)
            default_email, default_pwd = "rajesh.sharma@maharashtra.gov.in", "gov123"
        else:
            st.markdown("<div style='background:#fdf4ff; border:1.5px solid #f5d0fe; border-radius:14px; padding:14px 18px; margin:12px 0;'><strong style='color:#86198f;'>🚀 Startup Founder Access</strong><br><span style='font-size:13.5px; color:#a21caf;'>Browse challenges, self-certify eligibility, submit milestone proposals, and track escrow payouts.</span></div>", unsafe_allow_html=True)
            default_email, default_pwd = "founder@jaldrishti.io", "startup123"

        with st.form("secure_login_form"):
            st.markdown("##### Step 2 — Enter credentials")
            login_email = st.text_input("📧 Registered Email ID", value=default_email)
            login_pwd = st.text_input("🔑 Password", type="password", value=default_pwd)
            submit_login = st.form_submit_button(f"Sign In as {selected_role_str} →", type="primary", use_container_width=True)
            if submit_login:
                if login_email in USERS_DB:
                    user_info = USERS_DB[login_email]
                    if user_info["password"] == login_pwd:
                        if user_info["role"] == selected_role_str:
                            st.session_state.update({
                                'logged_in': True, 'user_email': login_email, 'user_role': user_info['role'],
                                'user_name': user_info['name'], 'user_dept': user_info['dept'], 'active_page': 'Dashboard'
                            })
                            st.success(f"✅ Authenticated as {user_info['name']} ({user_info['role']})")
                            st.rerun()
                        else:
                            st.error(f"❌ Account role mismatch: this account belongs to '{user_info['role']}'.")
                    else:
                        st.error("❌ Incorrect Password.")
                else:
                    st.error("❌ Email not registered in Narsby database.")

        st.markdown("<div style='margin:14px 0 6px 0; font-weight:800; color:#475569; font-size:14px;'>⚡ Quick demo login (judging / hackathon)</div>", unsafe_allow_html=True)
        q1, q2 = st.columns(2)
        with q1:
            if st.button("🏛️ Instant: Gov Official", use_container_width=True):
                st.session_state.update({'logged_in': True, 'user_email': "rajesh.sharma@maharashtra.gov.in",
                                          'user_role': "Government Official", 'user_name': "Dr. Rajesh Sharma (IAS)",
                                          'user_dept': "Water Supply & Sanitation Dept, Govt of Maharashtra", 'active_page': 'Dashboard'})
                st.rerun()
        with q2:
            if st.button("🚀 Instant: Startup Founder", use_container_width=True):
                st.session_state.update({'logged_in': True, 'user_email': "founder@jaldrishti.io",
                                          'user_role': "Startup Founder", 'user_name': "Ananya Deshmukh (Founder & CEO)",
                                          'user_dept': "JalDrishti IoT Pvt Ltd", 'active_page': 'Dashboard'})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. PUBLIC HOME PAGE (NO LOGIN — RESEARCHER / PUBLIC VIEW)
# -----------------------------------------------------------------------------
if not st.session_state['logged_in']:
    render_notification_bell()
    st.markdown("""
    <div class="hero-banner-public">
        <div class="hero-title">💡 Narsby — Startup-Friendly Public Procurement Platform</div>
        <div class="hero-subtitle">Government of Maharashtra · SIH 2026 · Problem Statement SIH26136 · Sandbox under GFR Rule 194</div>
        <div class="hero-quote">"A transparent, competitive, and legally compliant pathway from government problem to scaled startup solution — open for anyone to research."</div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🌍 Overview", "📚 Open Challenges", "🛰️ Public Pilot Tracker", "🏆 Success & Scale-Ups", "📄 Templates Library"])
    with tabs[0]:
        render_public_overview()
    with tabs[1]:
        render_public_challenges()
    with tabs[2]:
        render_public_pilots()
    with tabs[3]:
        render_public_scaleups()
    with tabs[4]:
        render_templates_library()

    render_login_section()
    st.stop()

# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION (ROLE-ISOLATED)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
        <span style="font-size:32px;">💡</span>
        <div>
            <div style="font-size:24px; font-weight:900; color:#1e1b4b; line-height:1.1;">Narsby</div>
            <div style="font-size:13px; font-weight:700; color:#6366f1; letter-spacing:.4px;">Govt of Maharashtra</div>
        </div>
    </div>
    <div style="font-size:13.5px; color:#64748b; margin-bottom:18px;">SIH 2026 · SIH26136 Sandbox</div>
    """, unsafe_allow_html=True)

    role_badge_html = '<span class="gov-badge">🏛️ GOVT OFFICIAL</span>' if st.session_state['user_role'] == 'Government Official' else '<span class="startup-badge">🚀 STARTUP FOUNDER</span>'
    st.markdown(f"""
    <div class="logged-in-pill">
        <span style="font-size:24px;">👤</span>
        <div><div style="font-size:14.5px; font-weight:800;">{st.session_state['user_name']}</div><div style="margin-top:2px;">{role_badge_html}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:13.5px; font-weight:800; color:#64748b; text-transform:uppercase; margin:16px 0 10px 0; letter-spacing:.6px;'>🧭 Navigation Menu</div>", unsafe_allow_html=True)

    if st.session_state['user_role'] == 'Government Official':
        nav_items = [
            ("🏛️ Government Dashboard", "Dashboard"),
            ("➕ Post New Problem Statement", "Post Challenge"),
            ("📥 Review Startup Proposals", "Review Proposals"),
            ("🛰️ Pilot Supervision & Escrow", "Active Pilots"),
            ("📄 Templates & Compliance Library", "Templates"),
            ("📊 Departmental Analytics", "Analytics"),
            ("🌍 Public Transparency Portal", "Public Portal"),
        ]
    else:
        nav_items = [
            ("🏠 Startup Dashboard", "Dashboard"),
            ("📚 Browse Open Challenges", "Browse Challenges"),
            ("📝 Submit Pilot Proposal", "Submit Proposal"),
            ("📁 My Past Works & Portfolio", "Startup Portfolio"),
            ("🧮 TRL & Viability Calculator", "Accuracy Calculator"),
            ("🛰️ My Active Pilot Milestones", "Active Pilots"),
            ("📄 Templates & Compliance Library", "Templates"),
            ("🌍 Public Transparency Portal", "Public Portal"),
        ]

    for label, page_key in nav_items:
        is_active = (st.session_state['active_page'] == page_key)
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state['active_page'] = page_key
            st.rerun()

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:14px; color:#334155; line-height:1.7; background:#ffffff; padding:14px; border-radius:12px; border:1.5px solid #eef2ff;">
        <div><strong>Role:</strong> {st.session_state['user_role']}</div>
        <div><strong>Entity:</strong> {st.session_state['user_dept'].split(',')[0]}</div>
        <div><strong>Framework:</strong> <span style="color:#059669; font-weight:700;">GFR 194 Exempted</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Sign Out (Log Out)", use_container_width=True):
        st.session_state.update({'logged_in': False, 'user_role': None, 'user_name': None, 'user_email': None, 'active_page': 'Dashboard'})
        st.rerun()

render_notification_bell()

# =============================================================================
# 6. SHARED PAGE: PUBLIC PORTAL (accessible from inside either logged-in role)
# =============================================================================
if st.session_state['active_page'] == 'Public Portal':
    st.markdown("# 🌍 **Public Transparency Portal**")
    st.caption("The same view researchers and the public see without logging in.")
    tabs = st.tabs(["🌍 Overview", "📚 Open Challenges", "🛰️ Public Pilot Tracker", "🏆 Success & Scale-Ups"])
    with tabs[0]:
        render_public_overview()
    with tabs[1]:
        render_public_challenges()
    with tabs[2]:
        render_public_pilots()
    with tabs[3]:
        render_public_scaleups()

elif st.session_state['active_page'] == 'Templates':
    render_templates_library()

# =============================================================================
# 7. GOVERNMENT PORTAL VIEWS
# =============================================================================
elif st.session_state['user_role'] == 'Government Official':

    if st.session_state['active_page'] == 'Dashboard':
        st.markdown(f"""
        <div class="hero-banner-gov">
            <div class="hero-title">🏛️ Government Innovation & Sandbox Command Center</div>
            <div class="hero-subtitle">Welcome, <strong>{st.session_state['user_name']}</strong> · {st.session_state['user_dept']}.
            Publish problem statements, screen startup eligibility, run independent validation, and approve scale-up decisions under GFR Rule 194.</div>
            <div class="hero-quote">"Procure outcomes, not just specifications."</div>
        </div>
        """, unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)
        with s1: st.markdown(f"<div class='stat-box'><div class='stat-label'>Published Challenges</div><div class='stat-val' style='color:#1e40af;'>{len(st.session_state['challenges'])} Active</div></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='stat-box'><div class='stat-label'>Proposals Received</div><div class='stat-val' style='color:#6366f1;'>{len(st.session_state['proposals'])} Submissions</div></div>", unsafe_allow_html=True)
        with s3: st.markdown("<div class='stat-box'><div class='stat-label'>Sanctioned Pilot Grants</div><div class='stat-val' style='color:#059669;'>₹54.5 Lakhs</div></div>", unsafe_allow_html=True)
        with s4: st.markdown(f"<div class='stat-box'><div class='stat-label'>Scale-Ups Recommended</div><div class='stat-val' style='color:#d97706;'>{len(st.session_state['scale_ups'])} 🚀</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin:30px 0 16px 0;'></div>", unsafe_allow_html=True)
        st.markdown("## ⚡ **Departmental Quick Actions**")
        qa1, qa2, qa3, qa4 = st.columns(4)
        actions = [
            ("➕ Post New Problem", "Define a new departmental challenge with target KPIs and sanctioned budget.", "Post Challenge", "btn_gov_add", True),
            ("📥 Review Proposals", "Screen eligibility, evaluate technical proposals, and award work orders.", "Review Proposals", "btn_gov_rev", False),
            ("🛰️ Monitor Active Pilots", "Verify milestone proofs, trigger independent validation, and release escrow.", "Active Pilots", "btn_gov_pilot", False),
            ("📊 Executive Analytics", "View procurement speed gains, cost savings, and sectoral grant allocations.", "Analytics", "btn_gov_ana", False),
        ]
        for col, (title, desc, target, key, primary) in zip([qa1, qa2, qa3, qa4], actions):
            with col:
                st.markdown(f"<div class='action-card'><div><div class='action-title'>{title}</div><div class='action-desc'>{desc}</div></div></div>", unsafe_allow_html=True)
                if st.button(f"{title.split(' ',1)[1]} →", key=key, use_container_width=True, type="primary" if primary else "secondary"):
                    st.session_state['active_page'] = target
                    st.rerun()

        st.markdown("<div style='margin:32px 0 14px 0;'></div>", unsafe_allow_html=True)
        st.markdown("## 📋 **Your Published Departmental Challenges**")
        for ch in st.session_state['challenges']:
            st.markdown(f"""
            <div class="item-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#1e1b4b; font-size:20px; font-weight:800;">{ch['title']}</h3>
                    <span class="pill-tag tag-gov">Budget: {ch['budget']}</span>
                </div>
                <div style="margin:8px 0;">{sector_pill(ch)}</div>
                <div style="font-size:14.5px; color:#64748b; margin-bottom:10px;">Dept: <strong style="color:#0f172a;">{ch['dept']}</strong> · Duration: <strong>{ch['duration']}</strong> · Posted By: <strong>{ch['posted_by']}</strong></div>
                <p style="font-size:15.5px; color:#334155; margin:0 0 10px 0;">{ch['description']}</p>
                <div style="background:#f8fafc; border-left:4px solid #0284c7; padding:8px 14px; border-radius:6px; font-size:15px;">🎯 <strong>Target KPI:</strong> {ch['target_kpi']}</div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state['active_page'] == 'Post Challenge':
        st.markdown("# ➕ **Post New Departmental Problem Statement**")
        st.markdown("Define a civic or administrative challenge to invite pilot solutions from DPIIT-registered startups under **GFR Rule 194**.")

        with st.form("new_challenge_form"):
            st.markdown("### 🏛️ **1. Department & Challenge Overview**")
            c_t1, c_t2 = st.columns(2)
            with c_t1:
                new_title = st.text_input("Challenge / Problem Statement Title", placeholder="e.g. Chapter 5: AI Drone Wildlife Conflict Mitigation")
                new_dept = st.selectbox("Procuring Department", ["Water Supply & Sanitation Dept", "Urban Development & Smart Cities", "Public Health & Family Welfare", "Agriculture & Farmers Welfare", "Environment & Climate Change", "Public Works Department (PWD)", "Energy & Non-Conventional Energy"])
            with c_t2:
                new_sector = st.selectbox("Sector Domain", ["Water & Smart City", "AI & Drone Mobility", "HealthTech & Triage", "Agritech & Sensors", "CleanTech & Energy", "GovTech & Civic AI"])
                new_duration = st.selectbox("Pilot Execution Duration", ["2 Months (60 Days)", "3 Months (90 Days)", "4 Months (120 Days)", "6 Months"])

            st.markdown("### 💰 **2. Budget & Target KPI Benchmark**")
            b_c1, b_c2 = st.columns(2)
            with b_c1:
                new_budget = st.selectbox("Sanctioned Sandbox Grant Pool", ["₹15 Lakhs", "₹20 Lakhs", "₹25 Lakhs", "₹35 Lakhs", "₹50 Lakhs"])
            with b_c2:
                new_kpi = st.text_input("Target Success KPI Benchmark", placeholder="e.g. Reduce crop damage by >= 30% with sub-10 minute alert latency")

            st.markdown("### ✅ **3. Startup Eligibility Criteria (auto-screened at proposal stage)**")
            e_c1, e_c2 = st.columns(2)
            with e_c1:
                elig_dpiit = st.checkbox("Require DPIIT / Startup India recognition", value=True)
                elig_turnover = st.selectbox("Maximum annual turnover cap", ["₹25 Cr (last FY)", "₹50 Cr (last FY)", "₹100 Cr (last FY)"])
            with e_c2:
                elig_age = st.selectbox("Maximum age since incorporation", ["7 years", "10 years", "15 years"])
                elig_sector = st.text_input("Sector-fit keyword for auto-screening", placeholder="e.g. Water/IoT/Sensors")

            st.markdown("### 📝 **4. Detailed Problem Statement & Constraints**")
            new_desc = st.text_area("Describe the existing ground problem, current limitations, and required technological capabilities:", height=130)

            submit_ch = st.form_submit_button("🚀 Publish Challenge to Live Portal →", type="primary", use_container_width=True)
            if submit_ch:
                if new_title and new_kpi and new_desc:
                    new_id = f"CH-0{len(st.session_state['challenges']) + 1}"
                    st.session_state['challenges'].append({
                        'id': new_id, 'title': new_title, 'dept': new_dept, 'sector': new_sector, 'tag': 'gov',
                        'budget': new_budget, 'duration': new_duration.split('(')[0].strip(), 'target_kpi': new_kpi,
                        'description': new_desc, 'posted_by': st.session_state['user_name'],
                        'date_posted': datetime.now().strftime('%Y-%m-%d'), 'status': 'Active (Accepting Proposals)',
                        'eligibility': {'dpiit_required': elig_dpiit, 'max_turnover': elig_turnover, 'max_age': elig_age, 'sector_fit': elig_sector or new_sector},
                        'scale_status': 'Not yet piloted'
                    })
                    st.session_state['notifications'].insert(0, {
                        'title': '🆕 New Challenge Posted', 'detail': f"{new_title} ({new_sector}) — {new_budget} sandbox grant open.",
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                    st.success(f"🎉 Challenge '{new_title}' published! Eligibility criteria will auto-screen every incoming proposal.")
                    st.balloons()
                else:
                    st.error("Please fill in the Challenge Title, Target KPI, and Detailed Description.")

    elif st.session_state['active_page'] == 'Review Proposals':
        st.markdown("# 📥 **Review Startup Proposals & Sanction Pilots**")
        st.markdown("Every proposal is auto-screened for eligibility before evaluation, keeping the process transparent and defensible.")

        if not st.session_state['proposals']:
            st.info("No startup proposals submitted yet.")
        for prop in st.session_state['proposals']:
            elig_ok = prop.get('eligibility_status', 'Not Screened')
            elig_cls = "tag-eligible" if 'Eligible' in elig_ok else "tag-flagged"
            st.markdown(f"""
            <div class="item-box">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <h3 style="margin:0; color:#1e1b4b; font-size:22px; font-weight:800;">{prop['startup_name']}</h3>
                        <div style="font-size:15px; color:#64748b; margin-top:4px;">Challenge: <strong style="color:#0f172a;">{prop['challenge_title']}</strong> · DPIIT: <strong>{prop['dpiit_id']}</strong></div>
                        <div style="margin-top:8px;"><span class="pill-tag {elig_cls}">Eligibility: {elig_ok}</span> <span class="pill-tag tag-validated">AI Match: {prop['match_score']}%</span></div>
                    </div>
                    <div style="text-align:right; font-size:13px; color:#059669; font-weight:700;">Status: {prop['status']}</div>
                </div>
                <div style="background:#f8fafc; border:1.5px solid #eef2ff; border-radius:12px; padding:16px 20px; margin:16px 0;">
                    <div style="font-size:16px; color:#1e293b; margin-bottom:8px;"><strong>Technical Solution:</strong> {prop['solution']}</div>
                    <div style="display:flex; gap:20px; font-size:14.5px; color:#475569; flex-wrap:wrap;">
                        <span>💰 <strong>Bid:</strong> <code style="color:#4f46e5;">{prop['bid']}</code></span>
                        <span>⏱️ <strong>Duration:</strong> <code>{prop['duration']}</code></span>
                        <span>🏷️ <strong>TRL:</strong> <code>TRL {prop['trl']}</code></span>
                        <span>📁 <strong>Past Work:</strong> <code>{prop.get('past_work_ref','Attached')}</code></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("🔍 View Eligibility Self-Certification Checklist"):
                for k, v in prop.get('eligibility_check', {}).items():
                    st.write(("✅ " if v else "❌ ") + k)

            c_a1, c_a2, _ = st.columns([1.2, 1.2, 2])
            with c_a1:
                if prop['status'] != 'Work Order Issued (Pilot Live)':
                    if st.button(f"✅ Sanction Work Order ({prop['id']})", key=f"award_{prop['id']}", type="primary", use_container_width=True):
                        prop['status'] = 'Work Order Issued (Pilot Live)'
                        st.success(f"Work order issued to {prop['startup_name']}! Pilot sandbox activated.")
                        st.rerun()
                else:
                    st.success("✓ Work Order Sanctioned & Escrow Funded")
            with c_a2:
                st.button("📄 View Full Pitch Deck", key=f"view_deck_{prop['id']}", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state['active_page'] == 'Active Pilots':
        st.markdown("# 🛰️ **Pilot Supervision, Independent Validation & Escrow**")
        st.markdown("Every milestone now needs **Government verification + Independent Third-Party Validation** before funds are released — matching the SIH26136 requirement for evidence-based, low-risk procurement.")

        for prop in st.session_state['proposals']:
            if 'Work Order Issued' not in prop['status']:
                continue
            st.markdown(f"""
            <div class="item-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#1e1b4b; font-size:22px; font-weight:800;">{prop['startup_name']} — Active Sandbox Pilot</h3>
                    <span class="pill-tag tag-eligible">Live Sandbox Active</span>
                </div>
                <div style="font-size:15px; color:#64748b; margin-top:6px;">Challenge: <strong>{prop['challenge_title']}</strong> · Total Grant: <strong style="color:#4f46e5;">{prop['bid']}</strong></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📊 **Live Telemetry (Outcome KPI Trend):**")
            chart_df = pd.DataFrame({
                'Day': [f"Day {i}" for i in range(1, 15)],
                'Measured Water Loss %': [36, 35, 33, 31, 30, 28, 27, 26, 25.5, 25, 24.8, 24.5, 24.2, 24.0],
                'Target Benchmark %': [25] * 14
            })
            fig = px.line(chart_df, x='Day', y=['Measured Water Loss %', 'Target Benchmark %'], markers=True, color_discrete_sequence=['#6366f1', '#f472b6'])
            fig.update_layout(template='plotly_white', height=300, margin=dict(l=15, r=15, t=20, b=20),
                               legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 🎯 **Milestone Deliverables → Independent Validation → Fund Clearance:**")
            for m in prop['milestones']:
                st.markdown(f"""
                <div style="background:#ffffff; border:1.5px solid #eef2ff; border-radius:12px; padding:16px 20px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:17px; font-weight:800; color:#1e1b4b;">Milestone {m['num']}: {m['title']}</span>
                            <span style="font-size:15px; color:#4f46e5; font-weight:700; margin-left:10px;">({m['amount']})</span>
                            <div style="font-size:14.5px; color:#64748b; margin-top:4px;"><strong>Proof Submitted:</strong> {m['proof']}</div>
                            {"<div style='font-size:13.5px; color:#3730a3; margin-top:4px;'>🛡️ Validated by: " + m['validator'] + "</div>" if m.get('validator') else ""}
                        </div>
                        <div><span style="font-size:14px; font-weight:700; color:{'#059669' if m['status']=='Completed & Paid' else '#d97706'};">{m['status']}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if m['status'] == 'Under Gov Review':
                    col_rel, _ = st.columns([1.8, 3])
                    with col_rel:
                        if st.button(f"🔎 Verify Proof → Send for Independent Validation", key=f"gov_verify_{prop['id']}_{m['num']}", type="secondary", use_container_width=True):
                            m['status'] = 'Pending Independent Validation'
                            st.info(f"Milestone {m['num']} government-verified. Routed to an empanelled third-party validator.")
                            st.rerun()
                elif m['status'] == 'Pending Independent Validation':
                    col_v1, col_v2 = st.columns([2, 1.6])
                    with col_v1:
                        validator = st.selectbox("Assign Independent Validator", ["Quality Council of India (QCI) empanelled auditor", "IIT-Bombay Technical Assessment Cell", "Third-Party Chartered Engineer Panel"], key=f"validator_{prop['id']}_{m['num']}")
                    with col_v2:
                        if st.button(f"✅ Confirm Validation & Disburse {m['amount']}", key=f"rel_{prop['id']}_{m['num']}", type="primary", use_container_width=True):
                            m['status'] = 'Completed & Paid'
                            m['validator'] = validator
                            st.session_state['notifications'].insert(0, {
                                'title': '✅ Milestone Independently Validated',
                                'detail': f"{prop['startup_name']} — Milestone {m['num']} ({m['title']}) cleared by {validator}. {m['amount']} disbursed.",
                                'date': datetime.now().strftime('%Y-%m-%d')
                            })
                            st.success(f"Milestone {m['num']} independently validated by {validator}! Escrow payout of {m['amount']} disbursed.")
                            st.rerun()

            if all(m['status'] == 'Completed & Paid' for m in prop['milestones']):
                already_scaled = any(su['startup_name'] == prop['startup_name'] for su in st.session_state['scale_ups'])
                if not already_scaled:
                    st.success("🎉 All milestones independently validated — this pilot qualifies for scale-up recommendation!")
                    with st.form(f"scaleup_form_{prop['id']}"):
                        s_targets = st.text_input("Recommend scale-up to (departments/districts):", placeholder="e.g. Nagpur, Nashik, Aurangabad Municipal Corporations")
                        s_impact = st.text_input("Impact summary to publish:", placeholder="e.g. Saved 1.4M litres/day; 28% water loss reduction")
                        if st.form_submit_button("🚀 Recommend for Scale-Up (publishes to Public Portal)", type="primary", use_container_width=True):
                            st.session_state['scale_ups'].append({
                                'startup_name': prop['startup_name'], 'solution_title': prop['challenge_title'],
                                'origin_pilot': prop['challenge_title'], 'scale_targets': s_targets or "To be finalized",
                                'recommended_by': st.session_state['user_name'], 'date': datetime.now().strftime('%Y-%m-%d'),
                                'impact_so_far': s_impact or "Pilot successfully validated."
                            })
                            st.session_state['notifications'].insert(0, {
                                'title': '🚀 Scale-Up Recommended',
                                'detail': f"{prop['challenge_title']} ({prop['startup_name']}) recommended for scale-up to: {s_targets or 'TBD'}.",
                                'date': datetime.now().strftime('%Y-%m-%d')
                            })
                            st.balloons()
                            st.success("Scale-up recommendation published to the Public Transparency Portal!")
                            st.rerun()
                else:
                    st.info("✅ This solution has already been recommended for scale-up. See the Public Transparency Portal.")

    elif st.session_state['active_page'] == 'Analytics':
        st.markdown("# 📊 **Departmental Procurement & Innovation Analytics**")
        st.markdown("Public efficiency metrics and turnaround speed comparison under Maharashtra GFR 194.")
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.metric("⚡ Procurement Speed", "14 Days", "-92% vs Conventional GFR")
        with k2: st.metric("💰 Total Grants Awarded", "₹1.12 Cr", "8 Pilots")
        with k3: st.metric("🚀 Startups Engaged", "42 Startups", "100% DPIIT Verified")
        with k4: st.metric("📉 Cost Savings", "38.5%", "vs Legacy Tenders")
        st.markdown("---")
        render_public_overview()

# =============================================================================
# 8. STARTUP PORTAL VIEWS
# =============================================================================
elif st.session_state['user_role'] == 'Startup Founder':

    if st.session_state['active_page'] == 'Dashboard':
        st.markdown(f"""
        <div class="hero-banner-startup">
            <div class="hero-title">🚀 Welcome back, {st.session_state['user_name']}!</div>
            <div class="hero-subtitle">{st.session_state['user_dept']} · DPIIT Recognized Sandbox Innovator. Browse challenges, self-certify eligibility, submit milestone pilot proposals, or upload past execution proofs.</div>
            <div class="hero-quote">"Direct government pilots with zero tendering friction and milestone escrow protection."</div>
        </div>
        """, unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)
        with s1: st.markdown(f"<div class='stat-box'><div class='stat-label'>Open Challenges</div><div class='stat-val' style='color:#7c3aed;'>{len(st.session_state['challenges'])} Live</div></div>", unsafe_allow_html=True)
        with s2: st.markdown("<div class='stat-box'><div class='stat-label'>My Submissions</div><div class='stat-val' style='color:#059669;'>1 Active Pilot</div></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='stat-box'><div class='stat-label'>Verified Past Works</div><div class='stat-val' style='color:#d97706;'>{len(st.session_state['startup_past_works'])} Proofs 🏆</div></div>", unsafe_allow_html=True)
        with s4: st.markdown("<div class='stat-box'><div class='stat-label'>Escrow Sanctioned</div><div class='stat-val' style='color:#2563eb;'>₹23.5 Lakhs</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin:30px 0 16px 0;'></div>", unsafe_allow_html=True)
        st.markdown("## 🚀 **Startup Quick Actions**")
        sq1, sq2, sq3, sq4 = st.columns(4)
        actions = [
            ("📚 Browse Challenges", "Explore live departmental problem statements open for pilot solutions.", "Browse Challenges", "btn_st_brw", True),
            ("📝 Submit Proposal", "Self-certify eligibility, then draft an outcome-based milestone proposal.", "Submit Proposal", "btn_st_prop", False),
            ("📁 Past Work Portfolio", "Upload past project certificates, patents, and live case studies.", "Startup Portfolio", "btn_st_port", False),
            ("🛰️ My Active Pilots", "Track live sensor feeds, independent validation status, and payouts.", "Active Pilots", "btn_st_plt", False),
        ]
        for col, (title, desc, target, key, primary) in zip([sq1, sq2, sq3, sq4], actions):
            with col:
                st.markdown(f"<div class='action-card'><div><div class='action-title'>{title}</div><div class='action-desc'>{desc}</div></div></div>", unsafe_allow_html=True)
                if st.button(f"{title.split(' ',1)[1]} →", key=key, use_container_width=True, type="primary" if primary else "secondary"):
                    st.session_state['active_page'] = target
                    st.rerun()

        st.markdown("<div style='margin:32px 0 14px 0;'></div>", unsafe_allow_html=True)
        st.markdown("## 📋 **Featured Open Departmental Problem Statements**")
        for ch in st.session_state['challenges'][:3]:
            st.markdown(f"""
            <div class="item-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#1e1b4b; font-size:20px; font-weight:800;">{ch['title']}</h3>
                    <span class="pill-tag tag-gov">{ch['budget']}</span>
                </div>
                <div style="margin:6px 0;">{sector_pill(ch)}</div>
                <div style="font-size:14.5px; color:#64748b; margin:6px 0 10px 0;">Dept: <strong>{ch['dept']}</strong> · Duration: <strong>{ch['duration']}</strong></div>
                <p style="font-size:15.5px; color:#334155; margin:0 0 10px 0;">{ch['description']}</p>
                <div style="background:#f8fafc; padding:8px 14px; border-radius:8px; font-size:14.5px;">🎯 <strong>Target KPI:</strong> {ch['target_kpi']}</div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state['active_page'] == 'Browse Challenges':
        render_public_challenges()
        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
        for ch in st.session_state['challenges']:
            if st.button(f"🚀 Apply with Pilot Proposal ({ch['id']} — {ch['title'][:40]}...)", key=f"apply_{ch['id']}", use_container_width=True):
                st.session_state['active_page'] = 'Submit Proposal'
                st.rerun()

    elif st.session_state['active_page'] == 'Submit Proposal':
        st.markdown("# 📝 **Submit Innovative Pilot Solution Proposal**")
        st.markdown("Step 1 self-certifies eligibility (per SIH26136's requirement for a transparent screening step); Step 2 captures your technical solution.")

        st.markdown("### ✅ **Step 1 — Eligibility Self-Certification**")
        ec1, ec2 = st.columns(2)
        with ec1:
            e_dpiit = st.checkbox("We are DPIIT / Startup India recognised", value=True)
            e_turnover = st.checkbox("Our turnover in the last FY is within the challenge's stated cap", value=True)
        with ec2:
            e_owned = st.checkbox("We are an Indian-owned & controlled entity", value=True)
            e_sector = st.checkbox("Our solution fits the challenge's sector/technology scope", value=True)
        elig_all = all([e_dpiit, e_turnover, e_owned, e_sector])
        if elig_all:
            st.success("✅ Eligible — you may proceed to submit a proposal.")
        else:
            st.warning("⚠️ One or more eligibility conditions are unmet. You can still submit, but it will be flagged for manual government review.")

        st.markdown("### 📝 **Step 2 — Proposal Details**")
        with st.form("st_proposal_form"):
            st.markdown("#### 🏢 Startup Information")
            p1, p2 = st.columns(2)
            with p1:
                p_name = st.text_input("Startup Entity Name", value=st.session_state['user_dept'])
                p_ch_target = st.selectbox("Select Target Problem Statement", [f"{c['id']} — {c['title']}" for c in st.session_state['challenges']])
            with p2:
                p_trl = st.selectbox("Demonstrated TRL", ["TRL 8: System Qualified & Ready for Operational Pilot", "TRL 7: System Prototype Demonstration in Operational Environment", "TRL 6: Technology Demonstrated in Relevant Environment", "TRL 9: Full Mission Proven"])
                p_bid = st.selectbox("Proposed Fast-Track Grant Bid", ["₹18,50,000", "₹23,50,000", "₹29,00,000", "₹35,00,000"])

            st.markdown("#### ⚙️ Technical Solution Architecture")
            p_tech = st.text_area("Technical Approach & Methodology:", value="We deploy 60 piezoelectric clamp-on acoustic sensors with cellular NB-IoT telemetry to isolate underground water leaks with sub-2.0 meter spatial precision, reducing non-revenue water loss by 28%.", height=110)

            st.markdown("#### 📁 Upload Pitch Deck & Link Past Works")
            up1, up2 = st.columns(2)
            with up1:
                st.file_uploader("📄 Upload Pitch Deck / Architecture Drawing (PDF)", type=["pdf", "docx"])
            with up2:
                st.selectbox("Link Existing Verified Past Work from Portfolio:", ["None (New Application)"] + [pw['title'] for pw in st.session_state['startup_past_works']])

            st.markdown("#### 🔐 Compliance Acknowledgement")
            ack_ip = st.checkbox("We accept the standard Data Sharing & IP Ownership Clause (see Templates Library)")
            ack_cyber = st.checkbox("We meet the minimum Cybersecurity & Risk Compliance Checklist")

            submit_prop_btn = st.form_submit_button("🚀 Submit Pilot Proposal to Government Committee →", type="primary", use_container_width=True)
            if submit_prop_btn:
                elig_label = "Eligible ✅" if elig_all else "Flagged for Manual Review ⚠️"
                st.session_state['proposals'].append({
                    'id': f"PROP-{100 + len(st.session_state['proposals']) + 1}",
                    'challenge_id': p_ch_target.split(' — ')[0], 'challenge_title': p_ch_target.split(' — ', 1)[-1],
                    'startup_name': p_name, 'founder_email': st.session_state['user_email'],
                    'dpiit_id': USERS_DB.get(st.session_state['user_email'], {}).get('dpiit_id', 'PENDING'),
                    'bid': p_bid, 'duration': '3 Months', 'trl': int(p_trl.split(':')[0].replace('TRL', '').strip()),
                    'match_score': 90, 'status': 'Under Technical Committee Review', 'submitted_date': datetime.now().strftime('%Y-%m-%d'),
                    'solution': p_tech, 'proof_attachment': 'Uploaded_Pitch_Deck.pdf', 'past_work_ref': 'Linked from Portfolio',
                    'eligibility_check': {'DPIIT Recognised': e_dpiit, 'Turnover under cap': e_turnover, 'Indian-owned & controlled': e_owned, 'Sector fit confirmed': e_sector},
                    'eligibility_status': elig_label,
                    'milestones': [
                        {'num': 1, 'title': 'Pilot Deployment & Baseline', 'amount': p_bid, 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None},
                        {'num': 2, 'title': 'Mid-Pilot Verification', 'amount': p_bid, 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None},
                        {'num': 3, 'title': 'Final Outcome & Handover', 'amount': p_bid, 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None},
                    ]
                })
                st.success(f"🎉 Proposal submitted! Eligibility status: **{elig_label}**. AI Match Score calculated: **96% Match**.")
                st.balloons()

    elif st.session_state['active_page'] == 'Startup Portfolio':
        st.markdown("# 📁 **Startup Previous Works & Execution Portfolio**")
        st.markdown("Upload past government work orders, completion certificates, and patents to increase proposal credibility score.")
        tab_showcase, tab_upload = st.tabs(["🏆 Verified Past Works Showcase", "📤 Upload New Past Work / Project Proof"])
        with tab_showcase:
            for pw in st.session_state['startup_past_works']:
                st.markdown(f"""
                <div class="portfolio-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <h3 style="margin:0; color:#1e1b4b; font-size:20px; font-weight:800;">{pw['title']}</h3>
                            <div style="font-size:15px; color:#64748b; margin-top:4px;">Client: <strong style="color:#0f172a;">{pw['client']}</strong> · Year: <strong>{pw['year']}</strong> · Sector: <strong style="color:#6366f1;">{pw['sector']}</strong></div>
                        </div>
                        <span class="pill-tag tag-eligible">✓ Verified Credential</span>
                    </div>
                    <div style="background:#ffffff; border:1.5px solid #eef2ff; padding:14px 16px; border-radius:10px; margin:12px 0;"><strong>🎯 Measured Impact:</strong> {pw['outcome']}</div>
                    <div style="display:flex; gap:14px; font-size:14px; color:#475569;">
                        <span>📎 Proof: <code>{pw['proof_file']}</code></span>
                        <span>🏷️ Level: <code>{pw['trl_demonstrated']}</code></span>
                        <span>🔗 <a href="{pw['live_url']}" target="_blank" style="color:#2563eb; font-weight:700; text-decoration:none;">View Live Case Study ↗</a></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        with tab_upload:
            with st.form("add_work_form"):
                pw_title = st.text_input("Project / Solution Title", placeholder="e.g. Drone Road Condition Mapping for Thane Municipal Corp")
                c1, c2 = st.columns(2)
                with c1:
                    pw_client = st.text_input("Client / Government Body", placeholder="e.g. Thane Municipal Corporation (TMC)")
                    pw_year = st.text_input("Year of Execution", placeholder="e.g. 2024 - 2025")
                with c2:
                    pw_sector = st.selectbox("Domain Sector", ["Water & Smart City", "AI & Drone Mobility", "HealthTech", "Agritech", "CleanTech"])
                    pw_trl = st.selectbox("TRL Level", ["TRL 7: Field Tested", "TRL 8: Fully Operational", "TRL 9: Mission Proven"])
                pw_outcome = st.text_area("Key Quantifiable Outcomes Achieved", placeholder="e.g. Analyzed 120 km of asphalt roads, identified 340 potholes with 93% accuracy...")
                uploaded_doc = st.file_uploader("📄 Upload Project Completion Letter / Work Order (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "docx"])
                pw_url = st.text_input("🔗 Live Video Demo / Case Study Link", placeholder="https://...")
                if st.form_submit_button("💾 Save to Portfolio & Generate Credential", type="primary", use_container_width=True):
                    if pw_title and pw_client and pw_outcome:
                        doc_name = uploaded_doc.name if uploaded_doc else "Verified_Summary.pdf"
                        st.session_state['startup_past_works'].append({
                            'title': pw_title, 'startup_name': st.session_state['user_dept'], 'client': pw_client,
                            'year': pw_year or "2025", 'sector': pw_sector, 'outcome': pw_outcome, 'proof_file': doc_name,
                            'trl_demonstrated': pw_trl.split(':')[0], 'live_url': pw_url or "#", 'verified': True
                        })
                        st.success(f"✅ Successfully added '{pw_title}' to your verified portfolio!")
                        st.rerun()
                    else:
                        st.error("Please fill in the Project Title, Client Name, and Key Outcomes.")

    elif st.session_state['active_page'] == 'Accuracy Calculator':
        st.markdown("# 🧮 **Proposal Viability & TRL Accuracy Calculator**")
        st.markdown("Test how government evaluators score your technology readiness level and past work track record.")
        col_c1, col_c2 = st.columns([1.1, 1])
        with col_c1:
            t_trl = st.slider("1. Technology Readiness Level (TRL 1-9)", 1, 9, 8)
            t_kpi = st.slider("2. Outcome KPI Coverage Alignment (%)", 50, 100, 95)
            t_past = st.slider("3. Verified Past Work Track Record Score (%)", 40, 100, 90)
            t_cost = st.slider("4. Cost Competitiveness & Value (%)", 50, 100, 92)
            score = min(99.4, (t_kpi * 0.35) + (t_trl * 11.0 * 0.25) + (t_past * 0.25) + (t_cost * 0.15))
        with col_c2:
            st.markdown("### 🎯 **Viability Score**")
            st.metric("🏆 Proposal Match Score", f"{score:.1f} / 100", delta="+18.4% above GFR Sandbox Threshold")
            st.progress(score / 100.0)
            st.info("💡 **Fast-Track Status:** Green Channel Approved. Fast turnaround in 7-10 business days.")

    elif st.session_state['active_page'] == 'Active Pilots':
        st.markdown("# 🛰️ **My Active Pilot Milestones, Validation & Telemetry**")
        st.markdown("Track government verification, independent validation, and escrow release for every milestone.")
        for prop in st.session_state['proposals']:
            if prop.get('founder_email') != st.session_state['user_email']:
                continue
            if 'Work Order Issued' not in prop['status']:
                continue
            st.markdown(f"""
            <div class="item-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#1e1b4b; font-size:22px; font-weight:800;">{prop['challenge_title']}</h3>
                    <span class="pill-tag tag-eligible">Work Order Sanctioned</span>
                </div>
                <div style="font-size:15px; color:#64748b; margin-top:6px;">Total Sanctioned Grant: <strong style="color:#4f46e5;">{prop['bid']}</strong></div>
            </div>
            """, unsafe_allow_html=True)
            for m in prop['milestones']:
                badge_color = '#059669' if m['status'] == 'Completed & Paid' else ('#7c3aed' if 'Validation' in m['status'] else '#d97706')
                val_line = f"<div style='font-size:13.5px; color:#3730a3; margin-top:4px;'>🛡️ Validated by: {m['validator']}</div>" if m.get('validator') else ""
                st.markdown(f"""
                <div style="background:#ffffff; border:1.5px solid #eef2ff; border-radius:12px; padding:16px 20px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:17px; font-weight:800; color:#1e1b4b;">Milestone {m['num']}: {m['title']}</span>
                            <span style="font-size:15px; color:#4f46e5; font-weight:700; margin-left:10px;">({m['amount']})</span>
                            <div style="font-size:14.5px; color:#64748b; margin-top:4px;"><strong>Proof:</strong> {m['proof']}</div>
                            {val_line}
                        </div>
                        <div><span style="font-size:14.5px; font-weight:800; color:{badge_color};">{m['status']}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)