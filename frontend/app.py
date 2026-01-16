import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
from datetime import datetime
# Page Config
st.set_page_config(
    page_title="Aadhaar Lifecycle Risk Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page config
st.set_page_config(
    page_title="UIDAI Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Color Palette - Modern Professional */
    :root {
        /* UIDAI-inspired palette */
        --primary: #0b4f8c;
        --primary-dark: #083b67;
        --secondary: #ff9933;
        --accent: #f59e0b;
        --success: #15803d;
        --warning: #b45309;
        --danger: #b91c1c;
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #334155;
        --text-muted: #64748b;
        --border: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    /* Global Base Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .stApp, body, [data-testid="stAppViewContainer"], .block-container {
        background-color: var(--bg-main) !important;
        background-image: 
            radial-gradient(at 40% 20%, hsla(215, 90%, 92%, 1) 0px, transparent 50%),
            radial-gradient(at 80% 0%, hsla(18, 100%, 93%, 1) 0px, transparent 50%),
            radial-gradient(at 0% 50%, hsla(220, 100%, 96%, 1) 0px, transparent 50%),
            radial-gradient(at 80% 50%, hsla(210, 100%, 96%, 1) 0px, transparent 50%),
            radial-gradient(at 0% 100%, hsla(22, 100%, 96%, 1) 0px, transparent 50%),
            radial-gradient(at 80% 100%, hsla(220, 100%, 96%, 1) 0px, transparent 50%);
        background-attachment: fixed;
        color: var(--text-primary) !important;
    }

 
    /* Header Section */
    .main-header {
        background: linear-gradient(135deg, #083b67 0%, #0b4f8c 50%, #2b6cb0 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    .main-header h1 {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 0 0.5rem 0 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .main-header p {
        color: #e0f2fe !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }

    /* --- VISIBILITY FIXES FOR INPUTS & DROPDOWNS --- */
    /* 1. Main Content Area Inputs (Light Background, Dark Text) */
    .stTextInput input, 
    div[data-testid="stAppViewContainer"] .stSelectbox div[data-baseweb="select"] div {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        caret-color: #0f172a !important;
    }

    /* 2. Sidebar Inputs (Dark Background, Light Text) */
    [data-testid="stSidebar"] .stTextInput input, 
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div {
        color: #f1f5f9 !important;
        -webkit-text-fill-color: #f1f5f9 !important;
        caret-color: #f1f5f9 !important;
    }

    /* 3. Dropdown Menus (Popovers) - Always Light Background, Dark Text */
    div[data-baseweb="popover"], div[data-baseweb="menu"], [data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: var(--shadow-lg) !important;
    }
    div[data-baseweb="option"], li[role="option"] {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }
    div[data-baseweb="option"]:hover, li[role="option"]:hover {
        background-color: #eff6ff !important;
        color: #0b4f8c !important;
    }
    div[data-baseweb="option"][aria-selected="true"], li[role="option"][aria-selected="true"] {
        background-color: #e0f2fe !important;
        color: #0b4f8c !important;
        font-weight: 600 !important;
    }

    /* Fix Dataframe text visibility */
    [data-testid="stDataFrame"] * {
        color: #1e293b !important;
        background-color: #ffffff !important;
    }
    [data-testid="stDataFrame"] th {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(12px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: var(--primary);
    }
    
    /* Custom Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }

    /* Info Boxes */
    .info-box, .warning-box, .success-box, .danger-box {
        padding: 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }
    .info-box {
        background: #eff6ff;
        border-color: var(--primary);
        color: #1e40af;
    }
    .warning-box {
        background: #fffbeb;
        border-color: var(--warning);
        color: #92400e;
    }
    .success-box {
        background: #f0fdf4;
        border-color: var(--success);
        color: #065f46;
    }
    .danger-box {
        background: #fef2f2;
        border-color: var(--danger);
        color: #991b1b;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid var(--primary);
        display: inline-block;
    }

    /* Risk Badges */
    .risk-badge {
        display: inline-block;
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.025em;
    }
    .risk-critical {
        background: #fef2f2;
        color: #991b1b;
        border: 1.5px solid #fecaca;
    }
    .risk-high {
        background: #fff7ed;
        color: #9a3412;
        border: 1.5px solid #fed7aa;
    }
    .risk-moderate {
        background: #fffbeb;
        color: #92400e;
        border: 1.5px solid #fde68a;
    }
    .risk-low {
        background: #f0fdf4;
        color: #065f46;
        border: 1.5px solid #86efac;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-md) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #1e293b !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }

    /* Charts & Visualizations */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    /* DataFrames */
    .stDataFrame {
        border-radius: 10px;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow-sm);
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--bg-card) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        font-weight: 600 !important;
    }

    /* District Banner */
    .district-banner {
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-lg);
        border: 2px solid rgba(255,255,255,0.2);
    }
    .district-banner h2 {
        color: white !important;
        margin: 0 0 0.5rem 0 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.025em !important;
    }
    .district-banner p {
        color: rgba(255,255,255,0.9) !important;
        margin: 0 !important;
        font-weight: 600 !important;
        font-size: 1.125rem !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-card);
        border-radius: 8px 8px 0 0;
        border: 1px solid var(--border);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #1e293b !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: white !important;
    }

    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes slowGradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .metric-card, .info-box, .warning-box, .success-box {
        animation: fadeInUp 0.4s ease-out;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.75rem !important;
        }
        .main-header {
            padding: 1.5rem 1rem;
        }
        .metric-card {
            padding: 1.25rem;
        }
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return pd.read_csv("backend/UIDAI_Dashboard_Dataset.csv")

# COMPONENT LIBRARY
def render_header():
    st.markdown("""
    <div class="main-header" style="animation: fadeInUp 0.8s ease-out;">
        <h1>🛡️ Aadhaar Lifecycle Intelligence Hub</h1>
        <p>Early Warning System for Enrolment, Demographic & Biometric Stability</p>
        <div style="position:absolute; right:1.5rem; top:1.5rem; opacity:0.9;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/61/Emblem_of_India.svg" style="height:36px; filter:brightness(0) invert(1); border-radius:4px;"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_insights(df):
    """Generate dynamic text insights from the dataframe."""
    insights = []
    if df.empty: return insights

    # 1. State Risk
    if 'State' in df.columns:
        state_risk = df.groupby('State')['ALHS_Score'].mean().sort_values(ascending=False)
        top_state = state_risk.index[0]
        insights.append(f"📍 **Geographic Alert:** **{top_state}** currently exhibits the highest average risk score ({state_risk.iloc[0]:.3f}), requiring immediate zonal review.")

    # 2. Biometric Backlog
    if 'Pending_Biometrics' in df.columns:
        total_pending = df['Pending_Biometrics'].sum()
        if total_pending > 0:
            insights.append(f"⏳ **Operational Bottleneck:** A cumulative backlog of **{total_pending:,}** biometric updates detected across the network.")

    # 3. Success Story
    if 'Enrolment_Health_Index' in df.columns:
        best_dist = df.sort_values('Enrolment_Health_Index', ascending=False).iloc[0]
        insights.append(f"🏆 **Performance Spotlight:** **{best_dist['District']}** is leading with a {best_dist['Enrolment_Health_Index']*100:.1f}% enrolment health efficiency rating.")

    # 4. Critical Mass
    critical_count = len(df[df['ALHS_Score'] > 0.7])
    if critical_count > 0:
        insights.append(f"🚨 **Critical Mass:** **{critical_count}** districts are currently flagged as 'Critical' (ALHS > 0.7), representing {(critical_count/len(df)*100):.1f}% of the network.")

    return insights

def render_kpis(metrics):
    if not metrics:
        st.error("⚠️ **Connection Error:** Backend is offline. Please run `python main.py` in a separate terminal.")
        return

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🚨 Critical Risk Districts",
            value=metrics.get('critical_districts', 0),
            delta=f"{metrics.get('high_risk_districts', 0)} High Risk",
            delta_color="inverse",
            help="Districts with ALHS Score > 0.7 requiring immediate intervention."
        )
    
    with col2:
        compliance = metrics.get('avg_compliance', 0) * 100
        st.metric(
            label="📊 Avg BCI (Bio Coverage)",
            value=f"{compliance:.1f}%",
            delta=f"{95 - compliance:.1f}% to target",
            delta_color="normal" if compliance >= 95 else "inverse",
            help="Biometric Compliance Index: Measure of biometric update completeness."
        )
    
    with col3:
        health = metrics.get('system_health', 0)
        st.metric(
            label="🛡️ ALHS (Lifecycle Health)",
            value=f"{health:.2f}",
            delta="Good" if health > 0.7 else "Needs Attention",
            delta_color="normal" if health > 0.7 else "inverse",
            help="Aadhaar Lifecycle Health Score: Composite score of ecosystem health (0-1)."
        )
    
    with col4:
        st.metric(
            label="⏳ Pending Updates",
            value=f"{metrics.get('pending_updates', 0):,}",
            delta=f"{metrics.get('total_districts', 0)} districts",
            help="Total count of biometric updates currently pending processing."
        )

# VISUALIZATION FUNCTIONS
def plot_risk_matrix(df):
    """Replaced the dense scatter matrix with two clearer visuals:
    - Left: Bar chart of top risk districts
    - Right: Sunburst showing risk share by State -> Risk Level
    Returns a single subplot figure.
    """
    # Top N risky districts
    top_n = 12
    df_sorted = df.sort_values(by='ALHS_Score', ascending=False).head(top_n)

    # Bar chart
    bar = px.bar(
        df_sorted[::-1],
        x='ALHS_Score',
        y='District',
        orientation='h',
        color='ALHS_Score',
        color_continuous_scale=['#ff9933', '#0b4f8c'],
        title='Top Risk Districts',
        labels={'ALHS_Score': 'Risk Score', 'District': 'District'}
    )

    # Sunburst by State -> Risk_Level to show concentration
    df = df.copy()
    def bucket(r):
        if r > 0.7: return 'Critical'
        if r > 0.4: return 'High'
        return 'Low'
    df['Risk_Level'] = df['ALHS_Score'].apply(bucket)

    sun = px.sunburst(
        df,
        path=['State', 'Risk_Level'],
        values='Total_Enrolment',
        color='Risk_Level',
        color_discrete_map={'Critical':'#dc2626','High':'#d97706','Low':'#16a34a'},
        title='Risk Concentration by State and Level'
    )

    # Combine into subplot
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], specs=[[{"type":"xy"},{"type":"domain"}]])
    for trace in bar.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in sun.data:
        fig.add_trace(trace, row=1, col=2)

    fig.update_layout(
        height=560,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_text="<b>Top Risks & State Concentration</b>",
        margin=dict(t=70, b=30, l=30, r=30),
        font=dict(family="Inter, sans-serif", size=13, color="#0f172a"),
        title_font=dict(color="#0f172a")
    )

    return fig

def plot_radar_chart(record):
    """Enhanced spider chart with better styling"""
    categories = ['Enrolment<br>Health', 'DSI (Demo<br>Saturation)', 'BCI (Bio<br>Coverage)']
    values = [
        record.get('Enrolment_Health_Index', 0),
        record.get('Demographic_Stability_Index', 0),
        record.get('Biometric_Compliance_Index', 0)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=record['District'],
        line=dict(color='#2563eb', width=3),
        fillcolor='rgba(37, 99, 235, 0.4)',
        marker=dict(size=8, color='#2563eb')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=12),
                gridcolor='#e2e8f0'
            ),
            angularaxis=dict(
                gridcolor='#e2e8f0',
                linecolor='#cbd5e1'
            ),
            bgcolor="rgba(255, 255, 255, 0.5)"
        ),
        showlegend=False,
        title=dict(
            text=f"<b>{record['District']} Health Profile</b>",
            font=dict(size=16, color="#0f172a", family="Inter")
        ),
        height=450,
        margin=dict(t=60, b=40, l=60, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13, color="#0f172a")
    )
    return fig

def plot_risk_distribution(df):
    """Enhanced histogram with better styling"""
    fig = px.histogram(
        df,
        x="ALHS_Score",
        nbins=25,
        title="<b>Risk Score Distribution</b>",
        labels={"ALHS_Score": "ALHS Risk Score"},
        color_discrete_sequence=['#2563eb']
    )
    
    fig.update_layout(
        height=350,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#0f172a"),
        title_font=dict(size=16, color="#0f172a"),
        margin=dict(t=50, b=40, l=40, r=40),
        showlegend=False
    )
    
    fig.update_traces(marker=dict(line=dict(width=1, color='white')))
    
    return fig

# PAGE LOGIC
def page_executive(df, metrics):
    # Strategic Value Banner for Jury
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(to right, #eff6ff, #ffffff); border-left: 5px solid #0b4f8c;">
        <h4 style="margin:0; color:#0b4f8c;">🎯 Strategic Value Proposition</h4>
        <p style="margin:5px 0 0 0; color:#334155;">
            This dashboard transforms raw enrolment logs into <strong>actionable lifecycle intelligence</strong>. By shifting focus from simple "volume" to <strong>"Lifecycle Health (ALHS)"</strong>, we identify silent exclusion risks and biometric failures <em>before</em> they become systemic crises.
        </p>
    </div>
    """, unsafe_allow_html=True)
    render_kpis(metrics)

    # --- AI Insights Section ---
    st.markdown("### 🧠 AI-Driven Daily Briefing")
    insights = generate_insights(df)
    if insights:
        for i in insights:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.6); backdrop-filter:blur(5px); padding:1rem; border-radius:8px; border-left:4px solid #f59e0b; margin-bottom:0.5rem; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
                {i}
            </div>
            """, unsafe_allow_html=True)
        
        st.download_button(
            label="📄 Download Executive Briefing",
            data="\n\n".join(insights),
            file_name=f"uidai_briefing_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    st.markdown('<p class="section-header">🌍 Systemic Risk Overview</p>', unsafe_allow_html=True)
    
    if not df.empty:
        st.plotly_chart(plot_risk_matrix(df), use_container_width=True)

    # --- State Comparison Section ---
    st.markdown("---")
    st.markdown('<p class="section-header">⚖️ State Comparative Analysis</p>', unsafe_allow_html=True)
    
    if df.empty:
        st.warning("No data available for comparison.")
        return

    # Selectors
    state_list = sorted(df['State'].unique())
    c1, c2 = st.columns(2)
    with c1:
        s1 = st.selectbox("Select State A", state_list, index=0, key='s1')
    with c2:
        # Try to select a different state by default if possible
        default_idx = 1 if len(state_list) > 1 else 0
        s2 = st.selectbox("Select State B", state_list, index=default_idx, key='s2')

    # Prepare Data
    d1 = df[df['State'] == s1]
    d2 = df[df['State'] == s2]

    # 1. KPI Row
    k1, k2, k3, k4 = st.columns(4)
    
    # Helper for KPI display
    def show_comp_kpi(col, label, val1, val2, fmt="{:.2f}", inverse=False):
        diff = val1 - val2
        color = "normal"
        if inverse:
            color = "inverse" if diff > 0 else "normal" # Higher is bad
        else:
            color = "normal" if diff > 0 else "inverse" # Higher is good
            
        with col:
            st.metric(
                label=label,
                value=fmt.format(val1),
                delta=f"{diff:+.2f} vs {s2}",
                delta_color=color
            )

    show_comp_kpi(k1, "Avg Risk Score (ALHS)", d1['ALHS_Score'].mean(), d2['ALHS_Score'].mean(), inverse=True)
    show_comp_kpi(k2, "Avg BCI (Bio Coverage)", d1['Biometric_Compliance_Index'].mean(), d2['Biometric_Compliance_Index'].mean())
    show_comp_kpi(k3, "Avg Enrolment Health", d1['Enrolment_Health_Index'].mean(), d2['Enrolment_Health_Index'].mean())
    
    # Critical Districts Count
    crit1 = len(d1[d1['ALHS_Score'] > 0.7])
    crit2 = len(d2[d2['ALHS_Score'] > 0.7])
    with k4:
        st.metric("🚨 Critical Districts", f"{crit1}", delta=f"{crit1 - crit2} vs {s2}", delta_color="inverse")

    # 2. Line Chart (Profile Comparison) & Intervention Priority
    st.markdown("#### 📊 Performance Profile & Intervention Needs")
    g1, g2 = st.columns([1.5, 1])

    with g1:
        # Create comparison data for Line Chart
        metrics_map = {
            'ALHS Risk': 'ALHS_Score',
            'BCI (Bio Coverage)': 'Biometric_Compliance_Index',
            'Enrolment Health': 'Enrolment_Health_Index',
            'DSI (Saturation)': 'Demographic_Stability_Index'
        }
        
        comp_data = []
        for label, col in metrics_map.items():
            comp_data.append({'Metric': label, 'State': s1, 'Score': d1[col].mean()})
            comp_data.append({'Metric': label, 'State': s2, 'Score': d2[col].mean()})
        
        cdf = pd.DataFrame(comp_data)
        
        fig_line = px.line(
            cdf, 
            x='Metric', 
            y='Score', 
            color='State', 
            markers=True,
            title=f"Metric Profile: {s1} vs {s2}",
            color_discrete_sequence=['#0b4f8c', '#f59e0b']
        )
        fig_line.update_yaxes(range=[0, 1.1])
        fig_line.update_layout(
            height=380,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            font=dict(color="#0f172a")
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with g2:
        # Fetch intervention data to show priority breakdown
        st.info("Intervention data is derived within the dashboard for hackathon deployment.")

def page_tableau_integration():
    st.markdown('<p class="section-header">🗺️ Tableau Public Dashboards</p>', unsafe_allow_html=True)
    st.markdown("Explore interactive state-level heatmaps and geospatial insights.")

    # Hardcoded Dashboard Configuration
    # REPLACE these URLs with your actual Tableau Public embed links
    dashboards = [
        {
            "title": "Future Risk Score Heatmap",
            "desc": "Displays district-wise composite future enrolment risk\nHigher intensity indicates higher likelihood of future exclusion or system stress\nDerived from lifecycle imbalance, biometric risk, saturation, and trend signals",
            "url": " https://public.tableau.com/views/UIDAIDashboard/FutureRiskScore?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link" 
        },
        {
            "title": "Intervention Priority Heatmap",
            "desc": "Categorizes districts by recommended action urgency:\nImmediate Intervention\nMonitor Closely\nRoutine Monitoring\nTranslates analytics into operational decision signals",
            "url": "https://public.tableau.com/views/UIDAIDashboard/InterventionPriority?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
        },
        {
            "title": "Lifecycle Risk Level Heatmap",
            "desc": "Categorical representation of enrolment risk:\nHealthy\nWatchlist\nCritical\nSimplifies complex risk scores into executive-ready insights",
            "url": " https://public.tableau.com/views/UIDAIDashboard/LifecycleRiskLevel?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
        },
        {
            "title": "Primary Failure Domain Heatmap ",
            "desc": "Highlights the dominant root cause of risk in each district:\nLate Enrolment\nSilent Exclusion\nBiometric Stress\nSaturation Stress\nGrowth Collapse\nPrimary Use:\nTargeted policy and operational interventions",
            "url": "https://public.tableau.com/views/UIDAIDashboard/PrimaryFailureDomain?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
        },
        {
            "title": "The Friction Monitor In Urban City ",
            "desc": "Near-zero processing delay but extremely high rejection — system is rejecting at the gate itself",
            "url": "https://public.tableau.com/views/Pr2_17684564882450/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
        },
        {
            "title": "Maintenance Debt Collapse",
            "desc": "Update volume overwhelms infrastructure, blocking enrollments & authentication",
            "url": "https://public.tableau.com/views/Pr1_17684563157220/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
        }
    ]

    st.markdown("---")
    
    # Grid Layout for Embeds
    for i in range(0, len(dashboards), 2):
        c1, c2 = st.columns(2)
        
        # First dashboard
        with c1:
            d = dashboards[i]
            st.markdown(f"#### {d['title']}")
            st.caption(d['desc'])
            components.html(
                f"""
                <div style='width:100%; height:500px; overflow:hidden; border-radius:12px; box-shadow:0 4px 6px rgba(0,0,0,0.1); border:1px solid #e2e8f0;'>
                    <iframe src='{d['url']}?:showVizHome=no&:embed=true' width='100%' height='500' style='border:none;'></iframe>
                </div>
                """,
                height=520
            )

        # Second dashboard
        if i + 1 < len(dashboards):
            with c2:
                d = dashboards[i+1]
                st.markdown(f"#### {d['title']}")
                st.caption(d['desc'])
                components.html(
                    f"""
                    <div style='width:100%; height:500px; overflow:hidden; border-radius:12px; box-shadow:0 4px 6px rgba(0,0,0,0.1); border:1px solid #e2e8f0;'>
                        <iframe src='{d['url']}?:showVizHome=no&:embed=true' width='100%' height='500' style='border:none;'></iframe>
                    </div>
                    """,
                    height=520
                )
        
        st.markdown("---")

def page_methodology():
    st.markdown('<p class="section-header">📚 Metric Definitions & Methodology</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="district-banner" style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 1.5rem; text-align: left;">
        <h3 style="color:white; margin:0;">🛡️ UIDAI Aadhaar Lifecycle Risk Analytics Framework</h3>
        <p style="color:#cbd5e1; margin-top:0.5rem; font-size:1rem;">
            <strong>Design Philosophy:</strong> No "black-box" predictions. All metrics are explainable, policy-aligned, and derived strictly from aggregated UIDAI data to preserve privacy while enabling proactive intervention.
        </p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["📊 Core & Lifecycle", "🚨 Risk & Saturation", "🛠️ Intervention Logic"])

    with t1:
        st.markdown("#### I. Core Enrolment Metrics")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**Total Enrolments**\n\nBase activity measure acting as the foundation for all downstream analysis.")
            st.info("**Growth Rate (MoM)**\n\nPercentage change in enrolments. Positive indicates expansion; negative signals disengagement.")
        with c2:
            st.info("**Enrolment Volatility Score**\n\nStatistical variation in monthly volumes. Low volatility may indicate stagnation; high indicates instability.")
        
        st.markdown("#### II. Age-Based Lifecycle Metrics")
        st.markdown("""
        *   **Child Enrolment Share (0–5)**: High share indicates healthy early onboarding.
        *   **Youth Enrolment Share (5–17)**: Signals school-linked coverage continuity.
        *   **Late Enrolment Ratio (18+)**: Proxy for delayed onboarding. High ratio suggests migration or historical exclusion.
        """)

    with t2:
        st.markdown("#### III. Lifecycle Health & Balance")
        st.markdown("""
        <div class="success-box">
            <strong>9. ALHS — Aadhaar Lifecycle Health Score</strong><br>
            A composite score (0-1) measuring how balanced the enrolment lifecycle is. 
            <br><em>Interpretation:</em> High ALHS = Timely, healthy lifecycle. Low ALHS = Delayed, skewed lifecycle.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### IV. Biometric & Operational Metrics")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            **11. BCI — Biometric Coverage Index**  
            Measures completeness of biometric enrolment.  
            *Low BCI* → Biometric access or quality issues.
            """)
        with c2:
            st.markdown("""
            **12. Biometric Flag Indicator**  
            Binary signal indicating biometric stress or anomalies requiring infrastructure review.
            """)

        st.markdown("#### V. Saturation & Access")
        st.markdown("""
        **13. DSI — Demographic Saturation Index**  
        Measures if enrolment activity is proportionate to district context.  
        *   `DSI ≈ 1`: Balanced
        *   `DSI > 1`: Over-saturation
        *   `DSI < 1`: Under-coverage
        """)

    with t3:
        st.markdown("#### VIII. Composite Risk & Intervention")
        
        st.markdown("""
        <div class="warning-box">
            <strong>21. Future_Risk_Score</strong><br>
            Forward-looking score estimating probability of future stress. Inputs: ALHS, BCI, DSI, and Volatility signals.
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**22. Lifecycle Risk Level**")
            st.caption("Categorical: Healthy, Watchlist, Critical")
        with c2:
            st.markdown("**23. Intervention Priority**")
            st.caption("Action Urgency: Immediate, Monitor, Routine")
        with c3:
            st.markdown("**24. Primary Failure Domain**")
            st.caption("Root Cause: e.g., Silent Exclusion, Bio Failure")

        st.markdown("---")
        st.markdown("#### IX. Governance Principles")
        st.markdown("""
        1.  **No Black-Box ML**: Explainable, auditable logic.
        2.  **District-First**: Governance perspective.
        3.  **Proactive**: Designed for intervention, not just reporting.
        4.  **Privacy**: Ethical, aggregated analysis only.
        """)


def page_district_deep_dive(df):
    st.markdown('<p class="section-header">🔍 District Diagnostics</p>', unsafe_allow_html=True)
    
    if df.empty:
        st.warning("⚠️ No data available for the selected state.")
        return

    col_search, col_blank = st.columns([1, 2])
    with col_search:
        district_list = sorted(df['District'].unique())
        selected_dist = st.selectbox("🎯 Select District to Audit:", district_list)
    
    if selected_dist:
        record = df[df['District'] == selected_dist].iloc[0]
        
        # Risk Banner
        risk_score = record.get('ALHS_Score', 0)
        if risk_score > 0.7:
            bg_color, text_label, emoji = "#dc2626", "CRITICAL RISK", "🚨"
        elif risk_score > 0.4:
            bg_color, text_label, emoji = "#d97706", "MODERATE RISK", "⚠️"
        else:
            bg_color, text_label, emoji = "#059669", "STABLE", "✅"
        
        st.markdown(f"""
        <div class="district-banner" style="background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%);">
            <h2>{emoji} {selected_dist.upper()}</h2>
            <p>Status: {text_label} | ALHS Score: {risk_score:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
            # Fetch intervention metrics for this district (if available)
        im_df = pd.DataFrame()  # Disable backend dependency

        im_record = None
        if not im_df.empty:
                matches = im_df[im_df['District'].str.lower() == selected_dist.lower()]
        if not matches.empty:
                    im_record = matches.iloc[0].to_dict()

            # Show intervention snapshot
        if im_record:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown(f"**Primary Failure Domain:** {im_record.get('Primary_Failure_Domain','N/A')}  ")
                st.markdown(f"**Intervention Priority:** {im_record.get('Intervention_Priority','N/A')}  ")
                st.markdown(f"**Lifecycle Risk Level:** {im_record.get('Lifecycle_Risk_Level','N/A')}  ")
                st.markdown(f"**District Rank:** {im_record.get('District_Rank','N/A')}  ")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
                st.info("No intervention metrics found for this district.")

        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.plotly_chart(plot_radar_chart(record), use_container_width=True)
        
        with col2:
            st.markdown("#### 🚨 Detected Anomalies")
            
            anomalies = []
            
            if record.get('Flag_Future_Surge_Risk') == 1:
                anomalies.append(("danger", "⚠️ **Future Surge Risk:** High pending biometrics indicating upcoming bottleneck."))
            
            if record.get('Flag_Low_Child_Compliance') == 1:
                anomalies.append(("warning", "⚠️ **Low Child Compliance:** Children aged 5-15 not updating biometrics."))
            
            if record.get('Flag_Infra_Stress') == 1:
                anomalies.append(("warning", "⚠️ **Infrastructure Stress:** Enrollment centers operating beyond capacity."))
            
            if record.get('Flag_Catch_Up_Spike') == 1:
                anomalies.append(("success", "✅ **Catch-Up Spike:** Positive trend in clearing backlog detected."))
            
            if anomalies:
                for anom_type, message in anomalies:
                    box_class = f"{anom_type}-box"
                    st.markdown(f'<div class="{box_class}">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ <strong>No critical anomalies detected.</strong> System operating within normal parameters.</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 🛠️ Recommended Actions")
            
            bci = record.get('Biometric_Compliance_Index', 0)
            ehi = record.get('Enrolment_Health_Index', 0)
            
            if bci < 0.5 and ehi < 0.5:
                st.markdown('<div class="danger-box">🔴 <strong>Critical:</strong> Deploy Mobile Biometric Kits AND audit enrollment operators immediately.</div>', unsafe_allow_html=True)
            elif bci < 0.5:
                st.markdown('<div class="warning-box">🟡 <strong>Priority:</strong> Deploy Mobile Biometric Kits to schools and community centers.</div>', unsafe_allow_html=True)
            elif ehi < 0.5:
                st.markdown('<div class="warning-box">🟡 <strong>Priority:</strong> Audit Enrollment Operators for data quality issues.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">🟢 <strong>Routine:</strong> Continue standard monitoring and maintenance.</div>', unsafe_allow_html=True)

def page_data_explorer(df, selected_state):
    st.markdown('<p class="section-header">📁 Data Explorer</p>', unsafe_allow_html=True)
    
    if not df.empty:
        # Summary stats in metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📍 Total Districts", len(df))
        with col2:
            st.metric("🗺️ States Covered", df['State'].nunique())
        with col3:
            st.metric("⚖️ Avg Risk Score", f"{df['ALHS_Score'].mean():.3f}")
        with col4:
            critical_count = len(df[df['ALHS_Score'] > 0.7])
            st.metric("🚨 Critical Districts", critical_count)
        
        st.markdown("---")
        
        # Add filter options
        with st.expander("🔍 Filter Options", expanded=False):
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                risk_filter = st.selectbox(
                    "Filter by Risk Level:",
                    ["All", "Critical (>0.7)", "High (0.4-0.7)", "Low (<0.4)"]
                )
            
            with col_f2:
                sort_by = st.selectbox(
                    "Sort by:",
                    ["ALHS_Score", "District", "State", "Total_Enrolment"]
                )
                sort_order = st.radio("Order:", ["Descending", "Ascending"], horizontal=True)
        
        # Apply filters
        filtered_df = df.copy()
        
        if risk_filter == "Critical (>0.7)":
            filtered_df = filtered_df[filtered_df['ALHS_Score'] > 0.7]
        elif risk_filter == "High (0.4-0.7)":
            filtered_df = filtered_df[(filtered_df['ALHS_Score'] > 0.4) & (filtered_df['ALHS_Score'] <= 0.7)]
        elif risk_filter == "Low (<0.4)":
            filtered_df = filtered_df[filtered_df['ALHS_Score'] <= 0.4]
        
        # Apply sorting
        ascending = True if sort_order == "Ascending" else False
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
        
        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} districts**")
        
        # Display dataframe with custom column configuration
        st.dataframe(
            filtered_df,
            column_config={
                "District": st.column_config.TextColumn("District", width="medium"),
                "State": st.column_config.TextColumn("State", width="medium"),
                "ALHS_Score": st.column_config.ProgressColumn(
                    "Risk Score",
                    format="%.3f",
                    min_value=0,
                    max_value=1,
                ),
                "Total_Enrolment": st.column_config.NumberColumn(
                    "Total Enrolment",
                    format="%d",
                ),
                "Pending_Biometrics": st.column_config.NumberColumn(
                    "Pending Updates",
                    format="%d",
                ),
                "Enrolment_Health_Index": st.column_config.ProgressColumn(
                    "Enrolment Health",
                    format="%.3f",
                    min_value=0,
                    max_value=1,
                ),
                "Biometric_Compliance_Index": st.column_config.ProgressColumn(
                    "BCI (Bio Coverage)",
                    format="%.3f",
                    min_value=0,
                    max_value=1,
                ),
                "Demographic_Stability_Index": st.column_config.ProgressColumn(
                    "DSI (Saturation)",
                    format="%.3f",
                    min_value=0,
                    max_value=1,
                ),
            },
            use_container_width=True,
            height=500
        )
        
        # Download section
        st.markdown("---")
        col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
        
        with col_d1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name=f"uidai_risk_data_{selected_state.replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_d2:
            # Download full dataset
            full_csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download All Data (CSV)",
                data=full_csv,
                file_name="uidai_risk_data_complete.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Additional insights
        st.markdown("---")
        st.markdown("### 📊 Quick Statistics")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("**Risk Distribution**")
            critical = len(df[df['ALHS_Score'] > 0.7])
            high = len(df[(df['ALHS_Score'] > 0.4) & (df['ALHS_Score'] <= 0.7)])
            low = len(df[df['ALHS_Score'] <= 0.4])
            st.write(f"🔴 Critical: {critical} ({critical/len(df)*100:.1f}%)")
            st.write(f"🟡 High: {high} ({high/len(df)*100:.1f}%)")
            st.write(f"🟢 Low: {low} ({low/len(df)*100:.1f}%)")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_s2:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("**Health Indices**")
            st.write(f"📈 Avg Enrolment Health: {df['Enrolment_Health_Index'].mean():.3f}")
            st.write(f"📈 Avg BCI: {df['Biometric_Compliance_Index'].mean():.3f}")
            st.write(f"📈 Avg DSI: {df['Demographic_Stability_Index'].mean():.3f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_s3:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("**System Load**")
            total_enrolment = df['Total_Enrolment'].sum()
            total_pending = df['Pending_Biometrics'].sum()
            st.write(f"👥 Total Enrolment: {total_enrolment:,}")
            st.write(f"⏳ Total Pending: {total_pending:,}")
            st.write(f"📊 Pending Rate: {(total_pending/total_enrolment*100):.2f}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        st.markdown('<div class="danger-box">⚠️ <strong>No data available.</strong> Please check your backend connection.</div>', unsafe_allow_html=True)
        
        if st.session_state.get('last_api_error'):
            with st.expander("🔧 View Error Details"):
                st.code(st.session_state['last_api_error'])

# MAIN APP LOGIC
def main():
    # Initialize session state
    if 'last_api_error' not in st.session_state:
        st.session_state['last_api_error'] = None
    
    # Sidebar: Filters, actions and debug (top tabs handle navigation)
    with st.sidebar:
        st.markdown("## 📊 Navigation")
        selected_page = st.radio(
            "Go to:",
            ["🏠 Executive Dashboard", "📚 Methodology & Definitions", "🔍 District Diagnostics", "🗺️ Tableau Heatmaps", "📁 Raw Data Explorer"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        
        st.markdown("### 🌍 Global Filters")
        
        full_df = load_data()
        if not full_df.empty:
            state_list = ["All India"] + list(sorted(full_df['State'].unique()))
            selected_state = st.selectbox("🗺️ Select State:", state_list)
        else:
            selected_state = "All India"
            if st.session_state.get('last_api_error'):
                with st.expander("⚠️ Backend Error Details", expanded=False):
                    st.code(st.session_state['last_api_error'][:2000])

        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        with col_b:
            pass

    # Main Content
    render_header()

    # Fetch Data once and reuse
    df = load_data()

    if selected_state != "All India":
        df = df[df["State"] == selected_state]

    metrics = {
        "critical_districts": (df["ALHS_Score"] > 0.7).sum(),
        "high_risk_districts": (df["ALHS_Score"] > 0.4).sum(),
        "avg_compliance": df["Biometric_Compliance_Index"].mean(),
        "system_health": 1 - df["ALHS_Score"].mean(),
        "pending_updates": df["Pending_Biometrics"].sum(),
        "total_districts": df["District"].nunique()
    }

    if selected_page == "🏠 Executive Dashboard":
        page_executive(df, metrics)
    elif selected_page == "📚 Methodology & Definitions":
        page_methodology()
    elif selected_page == "🔍 District Diagnostics":
        page_district_deep_dive(df)
    elif selected_page == "🗺️ Tableau Heatmaps":
        page_tableau_integration()
    elif selected_page == "📁 Raw Data Explorer":
        page_data_explorer(df, selected_state)

if __name__ == "__main__":
    main()