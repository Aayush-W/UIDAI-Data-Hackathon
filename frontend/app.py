"""
UIDAI Aadhaar Lifecycle Risk Dashboard
Streamlit Frontend - Main Landing Page
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="UIDAI Aadhaar Lifecycle Risk Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .info-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# API connection helper
def check_api_connection():
    """Check if backend API is accessible"""
    api_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
    try:
        response = requests.get(f"{api_url}/", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

# Main content
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Aadhaar Lifecycle Risk & Intervention Dashboard</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.95;">
            Policy-Grade Early-Warning Intelligence System | UIDAI Data Hackathon 2026
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API status
    api_connected = check_api_connection()
    
    if api_connected:
        st.success("✅ Backend API connected successfully")
    else:
        st.error("❌ Backend API not reachable. Please start the FastAPI server first.")
        st.code("python -m uvicorn backend.api.main:app --reload", language="bash")
        st.stop()
    
    # Introduction
    st.markdown("## 🎯 System Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Traditional Approach</h4>
            <ul>
                <li>Siloed analysis</li>
                <li>Reactive response</li>
                <li>Failure detection</li>
                <li>Post-incident reporting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #22c55e;">
            <h4>✨ Our Approach</h4>
            <ul>
                <li><strong>Unified lifecycle modeling</strong></li>
                <li><strong>Predictive signals</strong></li>
                <li><strong>Risk propagation analysis</strong></li>
                <li><strong>Pre-failure intervention</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #8b5cf6;">
            <h4>🎯 Impact</h4>
            <ul>
                <li>Intervene before failure</li>
                <li>Resource optimization</li>
                <li>Strategic planning</li>
                <li>Exclusion prevention</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key differentiators
    st.markdown("## 🔬 What Makes This System Different")
    
    st.markdown("""
    <div class="info-box">
        <h3 style="margin-top: 0;">This is NOT a descriptive analytics dashboard.</h3>
        <p style="font-size: 1.05rem;">
            This is a <strong>predictive risk intelligence system</strong> that models Aadhaar as a three-stage lifecycle:
        </p>
        <ol style="font-size: 1.05rem; line-height: 1.8;">
            <li><strong>Enrolment Health (EHI)</strong> → Captures late registration patterns and age imbalances</li>
            <li><strong>Demographic Stability (DSI)</strong> → Tracks update volatility and migration signals</li>
            <li><strong>Biometric Compliance (BCI)</strong> → Monitors mandatory update adherence and infrastructure stress</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        <h4>🔥 Critical Insight: Risk Propagation</h4>
        <p style="font-size: 1.05rem;">
            Failures propagate forward through the lifecycle. Poor enrolment creates demographic instability, 
            which cascades into biometric compliance failures and eventual authentication exclusion.
        </p>
        <p style="font-size: 1.05rem; margin-bottom: 0;">
            The <strong>Aadhaar Lifecycle Health Score (ALHS)</strong> quantifies this compound risk at the district level, 
            enabling UIDAI to intervene <strong>before</strong> citizens are excluded from essential services.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation guide
    st.markdown("## 📚 Dashboard Navigation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 **Executive Overview**
        - National KPIs and risk distribution
        - Top intervention priorities
        - State-wise comparative analysis
        
        ### 🔄 **Lifecycle Analysis**
        - EHI → DSI → BCI propagation patterns
        - Correlation analysis
        - Risk cascade visualization
        
        ### 🎯 **Risk Hotspots**
        - State/district filtering
        - Intervention priority matrix
        - Decision-ready tables
        """)
    
    with col2:
        st.markdown("""
        ### ⚠️ **Early-Warning System**
        - Predictive flag analysis
        - LOW_CHILD_COMPLIANCE
        - INFRA_STRESS
        - CATCH_UP_SPIKE
        - FUTURE_SURGE_RISK
        
        ### 🔍 **District Deep Dive**
        - Individual district analysis
        - Flag breakdown
        - Actionable intervention strategies
        """)
    
    st.markdown("---")
    
    # Technical architecture
    with st.expander("🏗️ Technical Architecture"):
        st.markdown("""
        ### System Components
        
        **Backend (FastAPI)**
        - RESTful API endpoints
        - Data processing pipeline
        - Metric computation engine
        - Caching layer
        
        **Frontend (Streamlit)**
        - Interactive visualizations
        - Multi-page navigation
        - Real-time API integration
        - Responsive design
        
        **Data Pipeline**
        - Stage 1: Aggregation (Daily → Monthly)
        - Stage 2: Metric Derivation (Ratios, Z-scores)
        - Stage 3: Flagging (Early-warning thresholds)
        """)
    
    # Data compliance
    st.markdown("---")
    st.markdown("""
    <div class="success-box">
        <h3 style="margin-top: 0;">✅ UIDAI Data Compliance</h3>
        <p style="font-size: 1.05rem; margin-bottom: 0;">
            All analysis uses <strong>aggregated, district-level, monthly data</strong> with no personal information. 
            This dashboard is built for policy decision-making, not individual tracking.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    st.markdown("## 👉 Get Started")
    
    st.info("""
    **Select a page from the sidebar to explore specific analysis modules →**
    
    Start with **Executive Overview** for a high-level summary, then dive deeper into specific areas of interest.
    """)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pages", "5", "Comprehensive Analysis")
    with col2:
        st.metric("API Endpoints", "10+", "Real-time Data")
    with col3:
        st.metric("Districts Analyzed", "150+", "National Coverage")

if __name__ == "__main__":
    main()
"""
UIDAI Aadhaar Lifecycle Risk Dashboard
Streamlit Frontend - Main Landing Page
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="UIDAI Aadhaar Lifecycle Risk Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .info-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# API connection helper
def check_api_connection():
    """Check if backend API is accessible"""
    api_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
    try:
        response = requests.get(f"{api_url}/", timeout=2)
        return response.status_code == 200
    except:
        return False

# Main content
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Aadhaar Lifecycle Risk & Intervention Dashboard</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.95;">
            Policy-Grade Early-Warning Intelligence System | UIDAI Data Hackathon 2026
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API status
    api_connected = check_api_connection()
    
    if api_connected:
        st.success("✅ Backend API connected successfully")
    else:
        st.error("❌ Backend API not reachable. Please start the FastAPI server first.")
        st.code("python backend/main.py", language="bash")
        st.stop()
    
    # Introduction
    st.markdown("## 🎯 System Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Traditional Approach</h4>
            <ul>
                <li>Siloed analysis</li>
                <li>Reactive response</li>
                <li>Failure detection</li>
                <li>Post-incident reporting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #22c55e;">
            <h4>✨ Our Approach</h4>
            <ul>
                <li><strong>Unified lifecycle modeling</strong></li>
                <li><strong>Predictive signals</strong></li>
                <li><strong>Risk propagation analysis</strong></li>
                <li><strong>Pre-failure intervention</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-left: 4px solid #8b5cf6;">
            <h4>🎯 Impact</h4>
            <ul>
                <li>Intervene before failure</li>
                <li>Resource optimization</li>
                <li>Strategic planning</li>
                <li>Exclusion prevention</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key differentiators
    st.markdown("## 🔬 What Makes This System Different")
    
    st.markdown("""
    <div class="info-box">
        <h3 style="margin-top: 0;">This is NOT a descriptive analytics dashboard.</h3>
        <p style="font-size: 1.05rem;">
            This is a <strong>predictive risk intelligence system</strong> that models Aadhaar as a three-stage lifecycle:
        </p>
        <ol style="font-size: 1.05rem; line-height: 1.8;">
            <li><strong>Enrolment Health (EHI)</strong> → Captures late registration patterns and age imbalances</li>
            <li><strong>Demographic Stability (DSI)</strong> → Tracks update volatility and migration signals</li>
            <li><strong>Biometric Compliance (BCI)</strong> → Monitors mandatory update adherence and infrastructure stress</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        <h4>🔥 Critical Insight: Risk Propagation</h4>
        <p style="font-size: 1.05rem;">
            Failures propagate forward through the lifecycle. Poor enrolment creates demographic instability, 
            which cascades into biometric compliance failures and eventual authentication exclusion.
        </p>
        <p style="font-size: 1.05rem; margin-bottom: 0;">
            The <strong>Aadhaar Lifecycle Health Score (ALHS)</strong> quantifies this compound risk at the district level, 
            enabling UIDAI to intervene <strong>before</strong> citizens are excluded from essential services.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation guide
    st.markdown("## 📚 Dashboard Navigation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 **Executive Overview**
        - National KPIs and risk distribution
        - Top intervention priorities
        - State-wise comparative analysis
        
        ### 🔄 **Lifecycle Analysis**
        - EHI → DSI → BCI propagation patterns
        - Correlation analysis
        - Risk cascade visualization
        
        ### 🎯 **Risk Hotspots**
        - State/district filtering
        - Intervention priority matrix
        - Decision-ready tables
        """)
    
    with col2:
        st.markdown("""
        ### ⚠️ **Early-Warning System**
        - Predictive flag analysis
        - LOW_CHILD_COMPLIANCE
        - INFRA_STRESS
        - CATCH_UP_SPIKE
        - FUTURE_SURGE_RISK
        
        ### 🔍 **District Deep Dive**
        - Individual district analysis
        - Flag breakdown
        - Actionable intervention strategies
        """)
    
    st.markdown("---")
    
    # Technical architecture
    with st.expander("🏗️ Technical Architecture"):
        st.markdown("""
        ### System Components
        
        **Backend (FastAPI)**
        - RESTful API endpoints
        - Data processing pipeline
        - Metric computation engine
        - Caching layer
        
        **Frontend (Streamlit)**
        - Interactive visualizations
        - Multi-page navigation
        - Real-time API integration
        - Responsive design
        
        **Data Pipeline**
        - Stage 1: Aggregation (Daily → Monthly)
        - Stage 2: Metric Derivation (Ratios, Z-scores)
        - Stage 3: Flagging (Early-warning thresholds)
        """)
    
    # Data compliance
    st.markdown("---")
    st.markdown("""
    <div class="success-box">
        <h3 style="margin-top: 0;">✅ UIDAI Data Compliance</h3>
        <p style="font-size: 1.05rem; margin-bottom: 0;">
            All analysis uses <strong>aggregated, district-level, monthly data</strong> with no personal information. 
            This dashboard is built for policy decision-making, not individual tracking.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    st.markdown("## 👉 Get Started")
    
    st.info("""
    **Select a page from the sidebar to explore specific analysis modules →**
    
    Start with **Executive Overview** for a high-level summary, then dive deeper into specific areas of interest.
    """)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pages", "5", "Comprehensive Analysis")
    with col2:
        st.metric("API Endpoints", "10+", "Real-time Data")
    with col3:
        st.metric("Districts Analyzed", "150+", "National Coverage")

if __name__ == "__main__":
    main()