"""
💡 Narsby • Live Startup Public Procurement Platform
Smart India Hackathon 2026 | Problem Statement: SIH26136 (Govt of Maharashtra)
Framework: Sandbox Under GFR Rule 194 | Identify -> Pilot -> Validate -> Scale
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64

# -----------------------------------------------------------------------------
# 0. BRANDING & ASSET HANDLING
# -----------------------------------------------------------------------------
LOGO_FULL = "narsby_logo.png"
LOGO_ICON = "narsby_icon.png"

def _img_b64(path):
    if os.path.isfile(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

LOGO_FULL_B64 = _img_b64(LOGO_FULL)
LOGO_ICON_B64 = _img_b64(LOGO_ICON)

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & ENERGETIC, COLOURFUL, BIG-FONT DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Narsby • Maharashtra Startup Procurement Sandbox",
    page_icon=(LOGO_ICON if os.path.isfile(LOGO_ICON) else "💡"),
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #0f172a;
        font-size: 18px;
    }
    h1 { font-family: 'Space Grotesk', sans-serif !important; font-size: 38px !important; font-weight: 800 !important; }
    h2 { font-family: 'Space Grotesk', sans-serif !important; font-size: 30px !important; font-weight: 800 !important; color: #1e1b4b !important; }
    h3 { font-family: 'Space Grotesk', sans-serif !important; font-size: 24px !important; font-weight: 700 !important; color: #312e81 !important; }
    p, span, label, div { font-size: 17.5px; line-height: 1.7; }

    /* Multi-Color Light Theme Canvas */
    [data-testid="stAppViewContainer"], .stApp, body {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0fdf4 100%) !important;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
    [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #ffffff 0%, #eef2ff 60%, #fae8ff 100%) !important;
        border-right: 2px solid #e0e7ff;
    }
    [data-testid="stMainBlockContainer"], .main .block-container {
        background: transparent !important;
        padding-top: 1.5rem !important;
    }

    /* Widget Surfaces */
    [data-testid="stExpander"], [data-testid="stForm"] {
        background: #ffffff !important;
        border-radius: 18px !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.05) !important;
        padding: 24px !important;
    }
    .stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #ffffff !important; 
        border-radius: 12px 12px 0 0 !important;
        border: 2px solid #e2e8f0 !important; 
        color: #334155 !important; 
        font-weight: 800 !important;
        font-size: 18px !important;
        padding: 10px 24px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border-color: #4f46e5 !important;
    }
    .stTabs [aria-selected="true"] p { color: #ffffff !important; }

    /* Inputs with Big Bold Typography */
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] > div {
        background: #ffffff !important; 
        border: 2px solid #cbd5e1 !important;
        border-radius: 12px !important;
        font-size: 17.5px !important;
        font-weight: 600 !important;
        color: #0f172a !important;
    }
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
    }
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label { 
        color: #0f172a !important; 
        font-weight: 800 !important; 
        font-size: 17.5px !important;
    }

    /* Buttons */
    .stButton > button {
        font-size: 17.5px !important;
        font-weight: 800 !important;
        padding: 12px 28px !important;
        border-radius: 14px !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(79, 70, 229, 0.45) !important;
    }
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        color: #1e1b4b !important;
    }

    /* Stat Cards */
    .stat-card-vibrant {
        border-radius: 18px;
        padding: 22px 24px;
        color: #ffffff;
        box-shadow: 0 12px 28px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    .stat-card-vibrant:hover { transform: translateY(-4px); }
    .stat-blue { background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%); }
    .stat-purple { background: linear-gradient(135deg, #7c3aed 0%, #c084fc 100%); }
    .stat-green { background: linear-gradient(135deg, #059669 0%, #34d399 100%); }
    .stat-amber { background: linear-gradient(135deg, #d97706 0%, #fbbf24 100%); }
    .stat-num { font-size: 38px; font-weight: 900; font-family: 'Space Grotesk', sans-serif; }
    .stat-desc { font-size: 15px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; opacity: 0.95; }

    /* Hero Banners */
    .hero-banner-public {
        background: linear-gradient(125deg, #e0e7ff 0%, #fae8ff 45%, #dcfce7 100%);
        border-radius: 26px;
        padding: 36px 40px;
        border: 2.5px solid #c7d2fe;
        box-shadow: 0 16px 36px rgba(99, 102, 241, 0.12);
        margin-bottom: 22px;
    }
    .hero-banner-gov {
        background: linear-gradient(125deg, #dbeafe 0%, #e0e7ff 50%, #ede9fe 100%);
        border-radius: 26px;
        padding: 38px 42px;
        border: 2.5px solid #bfdbfe;
        box-shadow: 0 16px 36px rgba(59, 130, 246, 0.14);
        margin-bottom: 24px;
    }
    .hero-banner-startup {
        background: linear-gradient(125deg, #fae8ff 0%, #fce7f3 50%, #ede9fe 100%);
        border-radius: 26px;
        padding: 38px 42px;
        border: 2.5px solid #f5d0fe;
        box-shadow: 0 16px 36px rgba(192, 38, 211, 0.12);
        margin-bottom: 24px;
    }
    .hero-title { font-size: 34px; font-weight: 900; color: #1e1b4b; letter-spacing: -0.8px; margin-bottom: 10px; font-family: 'Space Grotesk', sans-serif; }
    .hero-subtitle { font-size: 18px; color: #334155; font-weight: 600; line-height: 1.6; margin-bottom: 12px; }
    .hero-pill { background: #ffffff; padding: 6px 16px; border-radius: 30px; font-weight: 800; font-size: 14.5px; color: #4338ca; border: 1.5px solid #c7d2fe; display: inline-block; }

    /* Card Items */
    .item-box {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.06);
        transition: border-color 0.25s ease, transform 0.2s ease;
    }
    .item-box:hover {
        border-color: #818cf8;
        transform: translateY(-3px);
        box-shadow: 0 14px 32px rgba(99, 102, 241, 0.12);
    }
    .pill-tag {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 0.3px;
        margin-right: 8px;
    }
    .tag-water { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
    .tag-drone { background: #ede9fe; color: #5b21b6; border: 1px solid #ddd6fe; }
    .tag-health { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    .tag-agri { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    .tag-gov { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .tag-eligible { background: #ccfbf1; color: #115e59; border: 1.5px solid #5eead4; }

    .login-container {
        background: #ffffff;
        border-radius: 24px;
        border: 2.5px solid #e0e7ff;
        padding: 34px 38px;
        box-shadow: 0 20px 48px rgba(79, 70, 229, 0.12);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. IN-MEMORY DATA STORAGE
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

if 'initialized' not in st.session_state:
    st.session_state['challenges'] = [
        {
            'id': 'CH-01', 'title': 'Smart Water Pipeline Subterranean Acoustic Leakage Detection',
            'dept': 'Water Supply & Sanitation Dept', 'sector': 'Water & Smart City', 'tag': 'water',
            'budget': '₹25 Lakhs', 'budget_val': 25, 'duration': '3 Months',
            'target_kpi': 'Reduce subterranean water loss by ≥ 25% with sub-2m spatial accuracy',
            'description': 'Municipal water networks lose over 35% as non-revenue water. Deploy non-invasive IoT acoustic clamp sensors to detect bursts without tearing up roadways.',
            'posted_by': 'Dr. Rajesh Sharma (IAS)', 'date_posted': '2026-02-10', 'status': 'Active (Accepting Proposals)',
            'district': 'Pune Division', 'proposals_count': 3
        },
        {
            'id': 'CH-02', 'title': 'Automated Aerial Drone Pothole & Road Distress Survey',
            'dept': 'Urban Development & Smart Cities', 'sector': 'AI & Drone Mobility', 'tag': 'drone',
            'budget': '₹35 Lakhs', 'budget_val': 35, 'duration': '4 Months',
            'target_kpi': 'Survey 50 km/day with ≥ 92% automated road distress detection',
            'description': 'Automated drone computer vision survey to map asphalt surface quality, detect potholes, and generate instant GIS work orders for PWD crews.',
            'posted_by': 'Smt. Manisha Verma (IAS)', 'date_posted': '2026-02-14', 'status': 'Active (Accepting Proposals)',
            'district': 'Thane & MMR Region', 'proposals_count': 4
        },
        {
            'id': 'CH-03', 'title': 'Edge-AI Rural PHC Portable Vital Screening Kiosk',
            'dept': 'Public Health & Family Welfare', 'sector': 'HealthTech', 'tag': 'health',
            'budget': '₹30 Lakhs', 'budget_val': 30, 'duration': '3 Months',
            'target_kpi': 'Under 4-min multi-vital patient triage with 100% offline edge capability',
            'description': 'Battery-operated triage kiosk for remote Primary Health Centres with tele-ECG and automated cardiovascular risk grading for rural citizens.',
            'posted_by': 'Dr. Nitin Patil (Director of Health)', 'date_posted': '2026-02-18', 'status': 'Active (Accepting Proposals)',
            'district': 'Nagpur & Vidarbha', 'proposals_count': 2
        },
        {
            'id': 'CH-04', 'title': 'Hyper-Local Solar Optical Pest Early Warning Sensor Traps',
            'dept': 'Agriculture & Farmers Welfare', 'sector': 'Agritech', 'tag': 'agri',
            'budget': '₹20 Lakhs', 'budget_val': 20, 'duration': '3 Months',
            'target_kpi': 'Advance warning ≥ 7 days before major crop infestation',
            'description': 'Low-cost optical/acoustic insect traps with solar battery and vernacular Marathi SMS alerts for cotton & soybean growers.',
            'posted_by': 'Shri. S. K. Kadam (Agri Commissioner)', 'date_posted': '2026-02-22', 'status': 'Active (Accepting Proposals)',
            'district': 'Chhatrapati Sambhaji Nagar', 'proposals_count': 1
        }
    ]

    st.session_state['proposals'] = [
        {
            'id': 'PROP-101', 'challenge_id': 'CH-01', 'challenge_title': 'Smart Water Pipeline Acoustic Leakage Detection',
            'startup_name': 'JalDrishti IoT Pvt Ltd', 'founder_email': 'founder@jaldrishti.io', 'dpiit_id': 'DIPP-MH-44512',
            'bid': '₹23,50,000', 'bid_val': 23.5, 'duration': '3 Months', 'trl': 8, 'match_score': 96,
            'status': 'Work Order Issued (Pilot Live)', 'submitted_date': '2026-02-16',
            'solution': 'Piezoelectric acoustic clamp-on sensors with cellular NB-IoT telemetry to isolate underground water leaks with sub-2.0m precision.',
            'milestones': [
                {'num': 1, 'title': 'Deploy 60 Sensor Nodes in Ward 4', 'amount': '₹7,05,000', 'status': 'Completed & Paid', 'proof': '60 GPS coordinates verified; telemetry latency < 3 min.', 'validator': 'Quality Council of India (QCI)'},
                {'num': 2, 'title': 'Live Acoustic Leak Detection & Verification', 'amount': '₹9,40,000', 'status': 'Under Gov Review', 'proof': 'Identified 9 subterranean leaks. PWD repair crew confirmed 8 bursts.', 'validator': 'IIT-Bombay Technical Cell'},
                {'num': 3, 'title': 'Municipal SCADA System Integration', 'amount': '₹7,05,000', 'status': 'Pending Stage 2', 'proof': 'API schema prepared.', 'validator': None}
            ]
        },
        {
            'id': 'PROP-102', 'challenge_id': 'CH-02', 'challenge_title': 'Automated Aerial Drone Pothole & Road Distress Survey',
            'startup_name': 'AeroVision AI Robotics Pvt Ltd', 'founder_email': 'founder@aerovision.ai', 'dpiit_id': 'DIPP-MH-88124',
            'bid': '₹31,00,000', 'bid_val': 31.0, 'duration': '4 Months', 'trl': 7, 'match_score': 92,
            'status': 'Under Technical Committee Review', 'submitted_date': '2026-02-24',
            'solution': 'Autonomous dual-spectrum camera drones with TensorRT edge AI for sub-5cm pothole classification and automated PWD GIS mapping.',
            'milestones': [
                {'num': 1, 'title': '50 km Pilot Aerial Road Scan & AI Model Validation', 'amount': '₹9,30,000', 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None},
                {'num': 2, 'title': 'Automated PWD Geo-portal Integration', 'amount': '₹12,40,000', 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None},
                {'num': 3, 'title': 'Full Ward Survey & Defect Analytics', 'amount': '₹9,30,000', 'status': 'Awaiting Work Order', 'proof': 'Not started.', 'validator': None}
            ]
        }
    ]

    st.session_state['scale_ups'] = [
        {
            'startup_name': 'JalDrishti IoT Pvt Ltd', 'solution_title': 'Acoustic IoT Water Leak Detection',
            'origin_pilot': 'Pune Municipal Corporation', 'scale_targets': 'Nagpur, Nashik, Chhatrapati Sambhaji Nagar, Thane Municipal Corps',
            'recommended_by': 'Dr. Rajesh Sharma (IAS)', 'date': '2026-03-01',
            'impact_so_far': 'Saved 1.4M litres/day in Pune pilot; 28% water loss reduction.'
        }
    ]

    st.session_state['templates'] = [
        {
            'title': '📋 Outcome-Based Problem Statement Template (GFR 194)',
            'desc': 'Standard format for departments to define challenges by measurable target KPIs rather than restrictive hardware specs.',
            'content': """MAHARASHTRA STATE INNOVATION SANDBOX — GFR 194
1. Sponsoring Department & Officer:
2. Core Operational Bottleneck:
3. Target KPI (e.g., ≥25% efficiency gain in 90 days):
4. Sanctioned Pilot Pool (Max ₹50 Lakhs):
5. Baseline Assets/Data Provided by Department:
6. Independent Verification Authority Assigned:
"""
        },
        {
            'title': '🤝 Milestone Escrow & Tripartite Pilot Agreement',
            'desc': 'Legally-binding agreement linking every payout tranche to verified third-party audit clearances.',
            'content': """TRIPARTITE PILOT AGREEMENT — SANDBOX FRAMEWORK
Parties: Procuring Dept | DPIIT Startup | Independent Auditor (QCI/IIT)
Disbursement Schedule:
- Tranche 1 (30%): Baseline & Setup Verification
- Tranche 2 (40%): Operational Milestone Clearance
- Tranche 3 (30%): Final KPI Attainment & State Scale-Up Handover
"""
        },
        {
            'title': '🛒 Post-Pilot Direct GeM Transition Pathway Note',
            'desc': 'Legal framework exempting validated sandbox pilots from secondary L1 open bidding under Maharashtra GFR 194.',
            'content': """POST-PILOT SCALE-UP TRANSITION PROTOCOL
Step 1: Third-party auditor issues KPI Attainment Certificate.
Step 2: Department Secretary issues Pilot Success Ratification.
Step 3: Direct onboarding as Proprietary Innovative Product on GeM portal.
Step 4: Department-wide multi-year rate contract execution.
"""
        }
    ]

    st.session_state['notifications'] = [
        {'title': '🆕 New Challenge Posted', 'detail': 'Chapter 4: Hyper-Local Solar Pest Early Warning Sensor Traps — ₹20 Lakhs grant open.', 'date': '2026-02-22'},
        {'title': '⏰ Submission Closing Soon', 'detail': 'Chapter 3: Portable Rural PHC Edge-AI Kiosk — proposals close in 5 days.', 'date': '2026-03-05'},
        {'title': '✅ Milestone Independently Validated', 'detail': 'JalDrishti IoT Pvt Ltd — Milestone 1 cleared by QCI auditor.', 'date': '2026-02-28'},
    ]
    st.session_state['show_notifications'] = False
    st.session_state['initialized'] = True

# -----------------------------------------------------------------------------
# 3. STATISTICAL VISUALIZATIONS (WITH UNIQUE KEYS TO PREVENT DUPLICATE ID CRASH)
# -----------------------------------------------------------------------------
def render_rich_analytics(key_suffix="default"):
    st.markdown("## 📊 **Deep Statistical Analysis & Procurement Intelligence**")
    st.caption("Empirical performance data, expenditure allocations, and turnaround metrics across Maharashtra departments.")

    r1, r2 = st.columns(2)
    with r1:
        speed_df = pd.DataFrame({
            'Procurement Stage': ['Problem Definition', 'Evaluation & Review', 'Sanction & Award', 'Payment Release'],
            'Conventional Tender (Days)': [45, 60, 45, 30],
            'Narsby Sandbox (Days)': [3, 6, 4, 2]
        })
        fig_speed = go.Figure()
        fig_speed.add_trace(go.Bar(
            name='Conventional GFR Tender', 
            x=speed_df['Procurement Stage'], 
            y=speed_df['Conventional Tender (Days)'],
            marker=dict(color='#cbd5e1', line=dict(color='#94a3b8', width=1.5)),
            text=speed_df['Conventional Tender (Days)'],
            textposition='auto',
            textfont=dict(size=14, family="Plus Jakarta Sans", color="#1e293b")
        ))
        fig_speed.add_trace(go.Bar(
            name='Narsby Innovation Sandbox (GFR 194)', 
            x=speed_df['Procurement Stage'], 
            y=speed_df['Narsby Sandbox (Days)'],
            marker=dict(color='rgba(99, 102, 241, 0.95)', line=dict(color='#4338ca', width=1.5)),
            text=speed_df['Narsby Sandbox (Days)'],
            textposition='auto',
            textfont=dict(size=14, family="Plus Jakarta Sans", color="#ffffff")
        ))
        fig_speed.update_layout(
            title="⏱️ <b>Turnaround Speed: Conventional Tender vs Narsby (Days)</b>",
            barmode='group',
            template='plotly_white',
            height=370,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans", size=14, color="#0f172a"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_speed, use_container_width=True, key=f"chart_speed_{key_suffix}")

    with r2:
        sec_df = pd.DataFrame({
            'Sector': ['Water Tech', 'AI & Drone Mobility', 'HealthTech', 'Agritech'],
            'Sanctioned Budget (Lakhs)': [25, 35, 30, 20]
        })
        fig_donut = px.pie(
            sec_df, 
            values='Sanctioned Budget (Lakhs)', 
            names='Sector', 
            title="🥧 <b>Open Sandbox Grants Allocation by Sector (₹ Lakhs)</b>",
            hole=0.6,
            color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#10b981']
        )
        fig_donut.update_traces(
            textposition='outside', 
            textinfo='percent+label',
            textfont=dict(size=14, family="Plus Jakarta Sans", color="#0f172a")
        )
        fig_donut.update_layout(
            template='plotly_white', 
            height=370, 
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            font=dict(family="Plus Jakarta Sans", size=14, color="#0f172a")
        )
        st.plotly_chart(fig_donut, use_container_width=True, key=f"chart_donut_{key_suffix}")

    r3, r4 = st.columns(2)
    with r3:
        categories = ['Citizen Impact', 'Deployment Speed', 'Cost Savings', 'Vendor Diversity', 'Data Compliance']
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[92, 88, 95, 85, 96],
            theta=categories,
            fill='toself',
            name='Pune Smart City',
            line_color='#6366f1'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[82, 94, 80, 90, 89],
            theta=categories,
            fill='toself',
            name='Thane Municipal Corp',
            line_color='#ec4899'
        ))
        fig_radar.update_layout(
            title="🎯 <b>District Sandbox Maturity Index (Key Dimensions)</b>",
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            template='plotly_white',
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans", size=14, color="#0f172a")
        )
        st.plotly_chart(fig_radar, use_container_width=True, key=f"chart_radar_{key_suffix}")

    with r4:
        bubble_df = pd.DataFrame({
            'Challenge': ['Water IoT', 'Drone Roads', 'Health Kiosk', 'Agri Sensor', 'Smart Grid'],
            'TRL': [8, 7, 6, 7, 9],
            'Budget': [25, 35, 30, 20, 45],
            'Startups Applied': [4, 6, 3, 2, 8],
            'Sector': ['Water', 'Drone', 'Health', 'Agri', 'Energy']
        })
        fig_bubble = px.scatter(
            bubble_df, 
            x='TRL', 
            y='Budget', 
            size='Startups Applied', 
            color='Sector',
            text='Challenge',
            title="🔬 <b>Technology Readiness Level (TRL) vs Grant Size (₹ Lakhs)</b>",
            color_discrete_sequence=['#2563eb', '#7c3aed', '#db2777', '#059669', '#d97706'],
            size_max=40
        )
        fig_bubble.update_traces(textposition='top center', textfont=dict(size=13, family="Plus Jakarta Sans"))
        fig_bubble.update_layout(
            template='plotly_white', 
            height=380, 
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans", size=14, color="#0f172a")
        )
        st.plotly_chart(fig_bubble, use_container_width=True, key=f"chart_bubble_{key_suffix}")

# -----------------------------------------------------------------------------
# 4. INTERACTIVE ROI & COST-BENEFIT SIMULATOR (WITH UNIQUE KEYS)
# -----------------------------------------------------------------------------
def render_cost_benefit_simulator(key_suffix="default"):
    st.markdown("## 🧮 **Interactive Public Procurement ROI Simulator**")
    st.caption("Calculate quantifiable taxpayer savings, risk mitigation, and cycle-time compression under GFR 194.")

    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.markdown("#### ⚙️ Input Parameters:")
        annual_procurements = st.slider("Number of Innovative Pilot Projects per Year:", 5, 100, 24, step=1, key=f"sim_ann_{key_suffix}")
        avg_pilot_grant = st.slider("Average Sandbox Pilot Grant (₹ Lakhs):", 10, 100, 25, step=5, key=f"sim_grant_{key_suffix}")
        failure_rate = st.slider("Conventional Tender Failure / Rework Risk (%):", 15, 60, 35, step=5, key=f"sim_fail_{key_suffix}")

        conventional_tender_cost = annual_procurements * (avg_pilot_grant * 1.65)
        sandbox_cost = annual_procurements * avg_pilot_grant
        total_savings = conventional_tender_cost - sandbox_cost
        risk_reduction = (failure_rate * 0.72)
        days_saved = annual_procurements * 115

    with col2:
        st.markdown("#### 📈 Projected Public Dividend:")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #eef2ff 0%, #fae8ff 100%); border: 2px solid #c7d2fe; border-radius: 20px; padding: 26px; margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 800; color: #4338ca; text-transform: uppercase;">Direct Public Funds Saved</div>
            <div style="font-size: 38px; font-weight: 900; color: #1e1b4b; font-family: 'Space Grotesk', sans-serif;">₹{total_savings:.2f} Lakhs</div>
            <div style="font-size: 15px; color: #64748b; margin-top: 4px;">Saved via outcome-based milestone tranches instead of L1 upfront commitments.</div>
        </div>
        """, unsafe_allow_html=True)

        sc1, sc2 = st.columns(2)
        with sc1:
            st.metric("⏳ Admin Time Saved", f"{days_saved:,.0f} Days", delta="+92% Faster")
        with sc2:
            st.metric("🛡️ Risk Hedged", f"{risk_reduction:.1f}%", delta="Escrow Protected")

# -----------------------------------------------------------------------------
# 5. PUBLIC TRANSPARENCY VIEWS
# -----------------------------------------------------------------------------
def render_public_overview():
    st.markdown("## 🌍 **Maharashtra Civic Innovation Metrics**")
    
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
        <div class="stat-card-vibrant stat-blue">
            <div class="stat-desc">Active Challenges</div>
            <div class="stat-num">{len(st.session_state['challenges'])}</div>
            <div style="font-size:14px; opacity:0.9;">Across 4 Key Ministries</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="stat-card-vibrant stat-purple">
            <div class="stat-desc">Proposals Screened</div>
            <div class="stat-num">{len(st.session_state['proposals'])}</div>
            <div style="font-size:14px; opacity:0.9;">100% DPIIT Verified</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="stat-card-vibrant stat-green">
            <div class="stat-desc">Total Sandbox Grants</div>
            <div class="stat-num">₹1.10 Cr</div>
            <div style="font-size:14px; opacity:0.9;">Zero Upfront Advance Risk</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown(f"""
        <div class="stat-card-vibrant stat-amber">
            <div class="stat-desc">Avg. Time to Pilot</div>
            <div class="stat-num">14 Days</div>
            <div style="font-size:14px; opacity:0.9;">Down from 180 Days</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    render_rich_analytics(key_suffix="overview_tab")
    st.markdown("---")
    render_cost_benefit_simulator(key_suffix="overview_tab")

def render_public_challenges():
    st.markdown("## 📚 **Open Departmental Problem Statements**")
    st.caption("Civic issues posted by Maharashtra Government departments inviting DPIIT-registered startup pilots.")
    
    search_q = st.text_input("🔍 Search Challenges by Keyword or Sector:", placeholder="e.g., Water, Drone, HealthTech, Agritech...", key="pub_ch_search")
    filtered = [c for c in st.session_state['challenges'] if search_q.lower() in c['title'].lower() or search_q.lower() in c['dept'].lower() or search_q.lower() in c['sector'].lower()]

    col_l, col_r = st.columns(2)
    for idx, ch in enumerate(filtered):
        target = col_l if idx % 2 == 0 else col_r
        with target:
            tag_cls = f"tag-{ch.get('tag', 'gov')}"
            st.markdown(f"""
            <div class="item-box">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <span class="pill-tag {tag_cls}">{ch['sector']}</span>
                    <span class="pill-tag tag-gov">Grant: {ch['budget']}</span>
                </div>
                <div style="font-size:22px; font-weight:800; color:#1e1b4b; margin: 12px 0 6px 0;">{ch['title']}</div>
                <div style="font-size:15px; color:#64748b; margin-bottom:10px;">🏛️ Dept: <strong>{ch['dept']}</strong> · 📍 Division: <strong>{ch.get('district', 'Statewide')}</strong></div>
                <div style="font-size:16px; color:#334155; margin-bottom:12px;">{ch['description']}</div>
                <div style="background:#f1f5f9; border-left:5px solid #6366f1; padding:10px 14px; border-radius:8px; font-size:15px; font-weight:600; color:#1e293b;">
                    🎯 <strong>Target Outcome KPI:</strong> {ch['target_kpi']}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_public_pilots():
    st.markdown("## 🛰️ **Public Live Pilot & Telemetry Tracker**")
    st.caption("Verifiable, transparent monitoring of active pilots with independent validation results.")
    
    for prop in st.session_state['proposals']:
        if 'Work Order Issued' not in prop['status']:
            continue
        done_count = sum(1 for m in prop['milestones'] if m['status'] == 'Completed & Paid')
        st.markdown(f"""
        <div class="item-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0; font-size:24px; color:#1e1b4b;">🚀 {prop['startup_name']}</h3>
                    <div style="font-size:15px; color:#64748b; margin-top:4px;">Challenge: <strong>{prop['challenge_title']}</strong> · Sanctioned: <strong style="color:#4f46e5;">{prop['bid']}</strong></div>
                </div>
                <span class="pill-tag tag-eligible">{done_count}/{len(prop['milestones'])} Milestones Cleared</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        chart_df = pd.DataFrame({
            'Day': [f"Day {i}" for i in range(1, 15)],
            'Measured Water Loss %': [36, 35, 33, 31, 30, 28, 27, 26, 25.5, 25, 24.8, 24.5, 24.2, 24.0],
            'Target Benchmark %': [25] * 14
        })
        fig_telemetry = px.line(
            chart_df, 
            x='Day', 
            y=['Measured Water Loss %', 'Target Benchmark %'], 
            markers=True, 
            color_discrete_sequence=['#4f46e5', '#f43f5e']
        )
        fig_telemetry.update_layout(
            title="📡 <b>Live Sensor Telemetry: Subterranean Non-Revenue Water Loss %</b>",
            template='plotly_white', 
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans", size=13)
        )
        st.plotly_chart(fig_telemetry, use_container_width=True, key=f"telemetry_chart_{prop['id']}")

def render_public_scaleups():
    st.markdown("## 🏆 **Success Stories & Scale-Up Decisions**")
    st.caption("Once an innovative pilot achieves its target KPI, government departments issue direct scale-up sanctions.")
    for su in st.session_state['scale_ups']:
        st.markdown(f"""
        <div class="item-box" style="border-left:8px solid #10b981;">
            <div style="font-size:24px; font-weight:800; color:#065f46;">🚀 {su['solution_title']} — {su['startup_name']}</div>
            <div style="font-size:15px; color:#64748b; margin:6px 0 12px 0;">Origin Pilot: <strong>{su['origin_pilot']}</strong> · Sanctioned by: <strong>{su['recommended_by']}</strong> on {su['date']}</div>
            <div style="background:#f0fdf4; border:1.5px solid #bbf7d0; padding:14px 18px; border-radius:12px; margin-bottom:12px;">
                <strong>🎯 Measured Ground Impact:</strong> {su['impact_so_far']}
            </div>
            <div style="font-size:16px;"><strong>📈 Scale-Up Replication Districts:</strong> <code style="font-size:16px; color:#047857;">{su['scale_targets']}</code></div>
        </div>
        """, unsafe_allow_html=True)

def render_templates_library():
    st.markdown("## 📄 **Compliance & Legal Templates Library (GFR 194)**")
    st.caption("Standardized legal templates for rapid departmental onboarding under the Maharashtra Startup Policy.")
    for idx, t in enumerate(st.session_state['templates']):
        with st.expander(t['title']):
            st.markdown(f"**Purpose:** {t['desc']}")
            st.code(t['content'], language=None)
            st.download_button("⬇️ Download Template", data=t['content'], file_name=f"{t['title'][:20]}.txt", key=f"dl_tpl_{idx}")

# -----------------------------------------------------------------------------
# 6. AUTHENTICATION & LOGIN COMPONENT (PROMINENT & ERROR-FREE)
# -----------------------------------------------------------------------------
def render_login_screen():
    st.markdown("## 🔐 **Access Government / Startup Portals**")
    st.caption("Select your role below or use the 1-click instant login buttons for live judging demonstrations.")
    
    l_col1, l_col2 = st.columns([1, 1.25])
    with l_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4338ca 0%, #6366f1 50%, #8b5cf6 100%); border-radius: 24px; padding: 36px; color: #ffffff; height: 100%;">
            <div style="font-size: 30px; font-weight: 900; font-family: 'Space Grotesk', sans-serif; margin-bottom: 12px;">💡 Narsby Portal</div>
            <div style="font-size: 17px; opacity: 0.95; line-height: 1.6; margin-bottom: 22px;">
                Government of Maharashtra · SIH 2026 Innovation Sandbox under GFR Rule 194.
            </div>
            <div style="display:flex; gap:12px; align-items:center; margin-bottom:14px; font-size:15.5px;">
                ⚡ <span>Post outcome-based problems and sanction pilots in days.</span>
            </div>
            <div style="display:flex; gap:12px; align-items:center; margin-bottom:14px; font-size:15.5px;">
                🔎 <span>Automated DPIIT recognition and turnover screening.</span>
            </div>
            <div style="display:flex; gap:12px; align-items:center; margin-bottom:14px; font-size:15.5px;">
                🧾 <span>Milestone escrow with independent 3rd party audits.</span>
            </div>
            <div style="display:flex; gap:12px; align-items:center; font-size:15.5px;">
                📈 <span>Seamless post-pilot GeM scale-up pathways.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with l_col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("### 🔑 **Sign In**")
        role_select = st.radio("Select Portal Persona:", ["🏛️ Government Official (Dept Head / Procuring Entity)", "🚀 Startup Founder (DPIIT Registered Innovator)"], index=0, key="portal_role_select")
        is_gov = "Government Official" in role_select
        selected_role = "Government Official" if is_gov else "Startup Founder"
        
        default_email = "rajesh.sharma@maharashtra.gov.in" if is_gov else "founder@jaldrishti.io"
        default_pwd = "gov123" if is_gov else "startup123"

        with st.form("auth_form_main"):
            in_email = st.text_input("Registered Email", value=default_email, key="auth_email_in")
            in_pwd = st.text_input("Password", type="password", value=default_pwd, key="auth_pwd_in")
            submit_auth = st.form_submit_button(f"Sign In as {selected_role} →", type="primary", use_container_width=True)
            if submit_auth:
                if in_email in USERS_DB and USERS_DB[in_email]['password'] == in_pwd:
                    user_info = USERS_DB[in_email]
                    st.session_state.update({
                        'logged_in': True, 'user_email': in_email, 'user_role': user_info['role'],
                        'user_name': user_info['name'], 'user_dept': user_info['dept'], 'active_page': 'Dashboard'
                    })
                    st.success(f"Authenticated as {user_info['name']}")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try instant demo buttons below.")

        st.markdown("<div style='margin-top:14px; font-weight:800; color:#475569;'>⚡ 1-Click Instant Demo Access:</div>", unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            if st.button("🏛️ Instant Gov Official Login", use_container_width=True, key="demo_gov_btn"):
                st.session_state.update({
                    'logged_in': True, 'user_email': "rajesh.sharma@maharashtra.gov.in",
                    'user_role': "Government Official", 'user_name': "Dr. Rajesh Sharma (IAS)",
                    'user_dept': "Water Supply & Sanitation Dept, Govt of Maharashtra", 'active_page': 'Dashboard'
                })
                st.rerun()
        with d2:
            if st.button("🚀 Instant Startup Founder Login", use_container_width=True, key="demo_startup_btn"):
                st.session_state.update({
                    'logged_in': True, 'user_email': "founder@jaldrishti.io",
                    'user_role': "Startup Founder", 'user_name': "Ananya Deshmukh (Founder & CEO)",
                    'user_dept': "JalDrishti IoT Pvt Ltd", 'active_page': 'Dashboard'
                })
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. TOP HEADER & INSTANT ACCESS BAR
# -----------------------------------------------------------------------------
top_col1, top_col2, top_col3 = st.columns([5, 1.5, 1])
with top_col1:
    crumb = "🌍 Public Transparency Home" if not st.session_state['logged_in'] else f"{st.session_state['user_role']} / {st.session_state['active_page']}"
    st.markdown(f"<div style='font-size:16px; font-weight:800; color:#4f46e5; padding-top:6px;'>💡 Narsby <span style='color:#94a3b8; font-weight:600;'>/ {crumb}</span></div>", unsafe_allow_html=True)

with top_col2:
    if not st.session_state['logged_in']:
        if st.button("🔐 Quick Sign-In", type="primary", use_container_width=True, key="top_quick_signin_btn"):
            st.session_state['show_login_directly'] = True
            st.rerun()

with top_col3:
    if st.button(f"🔔 {len(st.session_state['notifications'])}", use_container_width=True, key="top_bell_btn"):
        st.session_state['show_notifications'] = not st.session_state['show_notifications']

if st.session_state.get('show_notifications'):
    with st.expander("📬 Live Notifications & Tender Alerts", expanded=True):
        for n in st.session_state['notifications']:
            st.markdown(f"**{n['title']}** — {n['detail']} *({n['date']})*")

# -----------------------------------------------------------------------------
# 8. PUBLIC HOME PAGE (IF NOT LOGGED IN)
# -----------------------------------------------------------------------------
if not st.session_state['logged_in']:
    st.markdown("""
    <div class="hero-banner-public">
        <div class="hero-title">💡 Narsby • Startup-Friendly Public Procurement Platform</div>
        <div class="hero-subtitle">
            Government of Maharashtra · Smart India Hackathon 2026 · Problem Statement SIH26136<br>
            A high-speed innovation sandbox under <strong>GFR Rule 194</strong> bridging startups with municipal & state agencies.
        </div>
        <div class="hero-pill">⚡ Identify Problem ➔ Fast-Track Pilot ➔ Independent Validation ➔ State Scale-Up</div>
    </div>
    """, unsafe_allow_html=True)

    # Clean tabs - LOGIN IS PROMINENTLY IN TAB 0
    pub_tabs = st.tabs([
        "🔐 Sign In / Portals", 
        "🌍 Overview & Stats", 
        "📚 Open Challenges", 
        "🛰️ Live Pilots Tracker", 
        "🏆 Scale-Up Decisions", 
        "📄 Compliance Library"
    ])
    with pub_tabs[0]:
        render_login_screen()
    with pub_tabs[1]:
        render_public_overview()
    with pub_tabs[2]:
        render_public_challenges()
    with pub_tabs[3]:
        render_public_pilots()
    with pub_tabs[4]:
        render_public_scaleups()
    with pub_tabs[5]:
        render_templates_library()

    st.stop()

# -----------------------------------------------------------------------------
# 9. LOGGED-IN SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="font-size:26px; font-weight:900; color:#1e1b4b; font-family:'Space Grotesk',sans-serif;">💡 Narsby</div>
    <div style="font-size:14px; font-weight:700; color:#6366f1; margin-bottom:16px;">Govt of Maharashtra Sandbox</div>
    <div style="background:#ffffff; border:2px solid #e0e7ff; border-radius:14px; padding:12px; margin-bottom:20px;">
        <div style="font-size:16px; font-weight:800; color:#0f172a;">{st.session_state['user_name']}</div>
        <div style="font-size:13.5px; color:#64748b;">{st.session_state['user_role']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state['user_role'] == 'Government Official':
        navs = [
            ("📊 Executive Dashboard", "Dashboard"),
            ("➕ Post New Problem", "Post Challenge"),
            ("📥 Review Proposals", "Review Proposals"),
            ("🛰️ Supervise Pilots", "Active Pilots"),
            ("📈 Deep Analytics", "Analytics"),
            ("📄 Templates Library", "Templates")
        ]
    else:
        navs = [
            ("🚀 Startup Dashboard", "Dashboard"),
            ("📚 Browse Challenges", "Browse Challenges"),
            ("📝 Submit Proposal", "Submit Proposal"),
            ("🛰️ My Active Pilots", "Active Pilots"),
            ("🧮 ROI Calculator", "ROI Calculator"),
            ("📄 Templates Library", "Templates")
        ]

    for lbl, target in navs:
        is_cur = (st.session_state['active_page'] == target)
        if st.button(lbl, key=f"nav_btn_{target}", use_container_width=True, type="primary" if is_cur else "secondary"):
            st.session_state['active_page'] = target
            st.rerun()

    st.markdown("---")
    if st.button("🚪 Sign Out (Log Out)", use_container_width=True, key="sidebar_signout_btn"):
        st.session_state['logged_in'] = False
        st.rerun()

# -----------------------------------------------------------------------------
# 10. ROLE-SPECIFIC WORKSPACES
# -----------------------------------------------------------------------------
if st.session_state['user_role'] == 'Government Official':
    if st.session_state['active_page'] == 'Dashboard':
        st.markdown(f"""
        <div class="hero-banner-gov">
            <div class="hero-title">🏛️ Government Innovation Command Center</div>
            <div class="hero-subtitle">Welcome, <strong>{st.session_state['user_name']}</strong> · {st.session_state['user_dept']}</div>
            <div class="hero-pill">GFR Rule 194 Sandbox Active · Fast-Track Sanctions Enabled</div>
        </div>
        """, unsafe_allow_html=True)
        render_public_overview()

    elif st.session_state['active_page'] == 'Post Challenge':
        st.markdown("## ➕ **Post New Outcome-Based Civic Challenge**")
        st.caption("Frame challenges based on measurable outcome KPIs rather than rigid technical specifications.")
        with st.form("gov_new_ch_form"):
            c_title = st.text_input("Challenge Title", placeholder="e.g., AI Drone Wildlife Conflict Mitigation & Thermal Alert", key="new_ch_title")
            col1, col2 = st.columns(2)
            with col1:
                c_dept = st.selectbox("Department", ["Water Supply & Sanitation", "Urban Development", "Public Health", "Agriculture & Farmers Welfare", "PWD", "Forest & Environment"], key="new_ch_dept")
                c_budget = st.selectbox("Sanctioned Sandbox Grant Pool", ["₹20 Lakhs", "₹25 Lakhs", "₹35 Lakhs", "₹50 Lakhs"], key="new_ch_budget")
            with col2:
                c_sector = st.selectbox("Sector", ["Water & Smart City", "AI & Drone Mobility", "HealthTech", "Agritech", "CleanTech"], key="new_ch_sector")
                c_duration = st.selectbox("Pilot Duration", ["2 Months", "3 Months", "4 Months", "6 Months"], key="new_ch_duration")
            c_kpi = st.text_input("Measurable Target KPI Benchmark", placeholder="e.g., Detect intrusion within 90 seconds with ≥ 95% accuracy", key="new_ch_kpi")
            c_desc = st.text_area("Detailed Problem Context & Existing Bottlenecks", height=120, key="new_ch_desc")
            if st.form_submit_button("🚀 Publish Challenge to Live Sandbox →", type="primary", use_container_width=True):
                if c_title and c_kpi and c_desc:
                    st.session_state['challenges'].append({
                        'id': f"CH-0{len(st.session_state['challenges']) + 1}", 'title': c_title,
                        'dept': c_dept, 'sector': c_sector, 'tag': 'gov', 'budget': c_budget,
                        'duration': c_duration, 'target_kpi': c_kpi, 'description': c_desc,
                        'posted_by': st.session_state['user_name'], 'date_posted': datetime.now().strftime('%Y-%m-%d')
                    })
                    st.success(f"🎉 Challenge '{c_title}' published successfully!")
                    st.rerun()

    elif st.session_state['active_page'] == 'Review Proposals':
        st.markdown("## 📥 **Review Startup Proposals & Sanction Pilots**")
        for prop in st.session_state['proposals']:
            st.markdown(f"""
            <div class="item-box">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <h3 style="margin:0; font-size:24px; color:#1e1b4b;">{prop['startup_name']}</h3>
                        <div style="font-size:15px; color:#64748b; margin-top:4px;">Challenge: <strong>{prop['challenge_title']}</strong> · DPIIT: <strong>{prop['dpiit_id']}</strong></div>
                    </div>
                    <span class="pill-tag tag-eligible">Match Score: {prop['match_score']}%</span>
                </div>
                <div style="background:#f8fafc; padding:16px; border-radius:12px; margin:14px 0; font-size:16px;">
                    <strong>Solution Approach:</strong> {prop['solution']}
                </div>
                <div style="display:flex; gap:20px; font-size:15px; color:#475569;">
                    <span>💰 Bid: <strong>{prop['bid']}</strong></span>
                    <span>⏱️ Duration: <strong>{prop['duration']}</strong></span>
                    <span>🔬 Readiness: <strong>TRL {prop['trl']}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if prop['status'] != 'Work Order Issued (Pilot Live)':
                if st.button(f"✅ Sanction Work Order & Fund Escrow ({prop['id']})", key=f"award_{prop['id']}", type="primary"):
                    prop['status'] = 'Work Order Issued (Pilot Live)'
                    st.success("Work Order sanctioned! Pilot sandbox activated.")
                    st.rerun()

    elif st.session_state['active_page'] == 'Active Pilots':
        render_public_pilots()
    elif st.session_state['active_page'] == 'Analytics':
        render_rich_analytics(key_suffix="gov_analytics_page")
    elif st.session_state['active_page'] == 'Templates':
        render_templates_library()

else:  # Startup Founder
    if st.session_state['active_page'] == 'Dashboard':
        st.markdown(f"""
        <div class="hero-banner-startup">
            <div class="hero-title">🚀 Welcome back, {st.session_state['user_name']}!</div>
            <div class="hero-subtitle">{st.session_state['user_dept']} · DPIIT Recognised Innovator</div>
            <div class="hero-pill">Zero EMD · Zero Tender Fee · GFR 194 Direct Pilot Route</div>
        </div>
        """, unsafe_allow_html=True)
        render_public_overview()
    elif st.session_state['active_page'] == 'Browse Challenges':
        render_public_challenges()
    elif st.session_state['active_page'] == 'Submit Proposal':
        st.markdown("## 📝 **Submit Pilot Proposal under GFR 194**")
        with st.form("st_submit_prop_form"):
            ch_choice = st.selectbox("Select Target Challenge", [f"{c['id']} — {c['title']}" for c in st.session_state['challenges']], key="st_prop_ch_choice")
            col1, col2 = st.columns(2)
            with col1:
                bid_amt = st.selectbox("Proposed Fast-Track Pilot Budget", ["₹18,50,000", "₹23,50,000", "₹31,00,000"], key="st_prop_bid")
            with col2:
                trl_val = st.slider("Demonstrated TRL Level", 5, 9, 8, key="st_prop_trl")
            tech_sol = st.text_area("Technical Architecture & Deployment Strategy", height=130, key="st_prop_sol")
            if st.form_submit_button("🚀 Submit Proposal to Technical Committee →", type="primary", use_container_width=True):
                st.session_state['proposals'].append({
                    'id': f"PROP-{100 + len(st.session_state['proposals']) + 1}",
                    'challenge_id': ch_choice.split(' — ')[0],
                    'challenge_title': ch_choice.split(' — ')[1],
                    'startup_name': st.session_state['user_dept'],
                    'founder_email': st.session_state['user_email'],
                    'dpiit_id': 'DIPP-MH-44512',
                    'bid': bid_amt, 'duration': '3 Months', 'trl': trl_val, 'match_score': 94,
                    'status': 'Under Technical Committee Review',
                    'solution': tech_sol,
                    'milestones': []
                })
                st.success("🎉 Proposal submitted successfully!")
                st.balloons()
    elif st.session_state['active_page'] == 'Active Pilots':
        render_public_pilots()
    elif st.session_state['active_page'] == 'ROI Calculator':
        render_cost_benefit_simulator(key_suffix="startup_calc_page")
    elif st.session_state['active_page'] == 'Templates':
        render_templates_library()
