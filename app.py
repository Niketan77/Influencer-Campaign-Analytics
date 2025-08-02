import streamlit as st
from data_processing.data_manager import DataManager
from data_processing.sample_data_generator import generate_sample_data
import components.data_management as dm
import components.export as export
import components.insights as insights
import components.overview as overview
import components.campaigns as campaigns
import components.influencers as influencers
import components.roas_calculator as roas_calculator
import components.payouts as payouts
# ... import other components as they are implemented

def initialize_session_state():
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


def show_tool_description():
    """Display comprehensive tool description and usage guide"""
    st.title("🚀 Influencer Campaign Analytics Dashboard")
    st.markdown("### Transform Your Influencer Marketing with Data-Driven Insights")
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3>🎯 Purpose</h3>
        <p>Consolidate scattered influencer campaign data into a unified analytics platform that delivers actionable insights, automates reporting, and optimizes ROI tracking.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # What it solves
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 🔍 **Problems Solved**
        - **Data Fragmentation**: Eliminates manual spreadsheet juggling
        - **Time-Consuming Analysis**: Reduces hours of work to minutes  
        - **ROI Blindness**: Provides clear campaign performance visibility
        - **Manual Reporting**: Automates export generation
        - **Budget Misallocation**: Identifies top-performing campaigns/influencers
        """)
    
    with col2:
        st.markdown("""
        #### ✨ **Key Benefits**
        - **90% Time Savings** on campaign analysis
        - **Real-time ROAS Tracking** across all campaigns
        - **Interactive Filtering** by date, campaign, platform
        - **One-Click Exports** in CSV, Excel, PDF formats
        - **Automated Insights** and recommendations
        """)
    
    # Feature overview
    st.markdown("---")
    st.subheader("🛠️ **Tool Features & Usage Guide**")
    
    features = [
        {
            "icon": "📁",
            "title": "Data Management",
            "purpose": "Upload your CSV files or generate sample data to get started",
            "usage": "Start here first! Either upload your influencer, posts, tracking, and payout CSVs or click 'Load Demo Data' to explore with sample data.",
            "best_for": "Initial setup, data validation, testing with demo data"
        },
        {
            "icon": "📊", 
            "title": "Overview Dashboard",
            "purpose": "Get high-level KPIs and performance trends at a glance",
            "usage": "View total revenue, active campaigns, influencer count, and average ROAS. Analyze revenue trends over time and top-performing influencers.",
            "best_for": "Executive summaries, quick health checks, stakeholder presentations"
        },
        {
            "icon": "📈",
            "title": "Campaign Performance", 
            "purpose": "Deep-dive into individual campaign metrics and comparisons",
            "usage": "Filter by date range, campaign, or platform. Compare influencer performance within campaigns using scatter plots and timeline analysis.",
            "best_for": "Campaign optimization, budget reallocation, performance analysis"
        },
        {
            "icon": "👥",
            "title": "Influencer Analytics",
            "purpose": "Evaluate individual influencer ROI and engagement metrics", 
            "usage": "Filter by category and follower count. Identify top performers by ROAS, engagement rates, and revenue generation.",
            "best_for": "Influencer selection, contract negotiations, partnership decisions"
        },
        {
            "icon": "💰",
            "title": "ROAS Calculator",
            "purpose": "Calculate Return on Ad Spend for campaigns and overall performance",
            "usage": "View overall ROAS and drill down to campaign-level ROAS. Includes incremental ROAS calculations and break-even analysis.", 
            "best_for": "ROI analysis, budget planning, campaign profitability assessment"
        },
        {
            "icon": "💳",
            "title": "Payout Tracker",
            "purpose": "Monitor influencer payments and cash flow analysis",
            "usage": "Filter payouts by date range. Track monthly payout trends and identify top earners. Monitor payment status distribution.",
            "best_for": "Financial planning, cash flow management, influencer payment tracking"
        },
        {
            "icon": "💡", 
            "title": "Automated Insights",
            "purpose": "Get AI-powered recommendations and trend analysis",
            "usage": "Review automatically generated insights about top performers, growth trends, and optimization recommendations.",
            "best_for": "Strategic planning, quick wins identification, data-driven recommendations"
        },
        {
            "icon": "📤",
            "title": "Export Data", 
            "purpose": "Generate professional reports for stakeholders",
            "usage": "Select any dataset and download in CSV, Excel, or PDF format. Perfect for sharing with teams or external stakeholders.",
            "best_for": "Reporting, data sharing, offline analysis, stakeholder presentations"
        }
    ]
    
    for feature in features:
        with st.expander(f"{feature['icon']} **{feature['title']}** - {feature['purpose']}"):
            st.markdown(f"**How to Use:** {feature['usage']}")
            st.markdown(f"**Best For:** {feature['best_for']}")
    
    # Quick start guide
    st.markdown("---")
    st.subheader("🚀 **Quick Start Guide**")
    
    st.markdown("""
    1. **📁 Start with Data Management** → Load demo data or upload your CSVs
    2. **📊 Check Overview** → Get familiar with your data and key metrics  
    3. **📈 Analyze Campaigns** → Dive deep into campaign performance
    4. **👥 Evaluate Influencers** → Identify your top performers
    5. **💰 Calculate ROAS** → Understand your return on investment
    6. **📤 Export Results** → Share insights with your team
    """)
    
    # Technical specs
    st.markdown("---")
    st.subheader("⚙️ **Technical Specifications**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Data Formats**\n- CSV files\n- Excel imports\n- Date range filtering")
    with col2:
        st.markdown("**Export Options**\n- CSV downloads\n- Excel files\n- PDF reports")  
    with col3:
        st.markdown("**Visualizations**\n- Interactive charts\n- Real-time filtering\n- Responsive design")

def main():
    st.set_page_config(
        page_title="Influencer Campaign Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    initialize_session_state()
    
    # Enhanced sidebar with better organization
    st.sidebar.markdown("### 🧭 **Navigation**")
    page = st.sidebar.selectbox(
        "Choose a section:",
        [
            "🏠 Home & Guide",
            "📁 Data Management", 
            "📊 Overview Dashboard",
            "📈 Campaign Performance",
            "👥 Influencer Analytics",
            "💰 ROAS Calculator",
            "💳 Payout Tracker",
            "💡 Automated Insights",
            "📤 Export Data"
        ]
    )
    
    # Add data status indicator in sidebar
    st.sidebar.markdown("---")
    if st.session_state.get('data_loaded', False):
        st.sidebar.success("✅ Data Loaded")
        dm_obj = st.session_state.data_manager
        st.sidebar.markdown(f"""
        **Data Summary:**
        - 👥 {len(dm_obj.influencers_df)} Influencers
        - 📝 {len(dm_obj.posts_df)} Posts  
        - 📊 {len(dm_obj.tracking_df)} Tracking Records
        - 💳 {len(dm_obj.payouts_df)} Payouts
        """)
    else:
        st.sidebar.warning("⚠️ No Data Loaded")
        st.sidebar.info("👆 Start with Data Management to load your data")
    
    # Add quick tips in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 **Quick Tips**")
    tips = [
        "Start with Data Management to load demo data",
        "Use Overview for executive summaries", 
        "Filter by date ranges for specific periods",
        "Export data for offline analysis",
        "Check Insights for AI recommendations"
    ]
    
    for tip in tips:
        st.sidebar.markdown(f"• {tip}")
    
    # Route to appropriate page
    if page == "🏠 Home & Guide":
        show_tool_description()
    elif page == "📁 Data Management":
        dm.show_data_management()
    elif page == "📊 Overview Dashboard":
        overview.show_overview()
    elif page == "📈 Campaign Performance":
        campaigns.show_campaign_performance()
    elif page == "👥 Influencer Analytics":
        influencers.show_influencers()
    elif page == "💰 ROAS Calculator":
        roas_calculator.show_roas_calculator()
    elif page == "💳 Payout Tracker":
        payouts.show_payouts()
    elif page == "💡 Automated Insights":
        insights.show_insights()
    elif page == "📤 Export Data":
        export.show_export_data()

if __name__ == "__main__":
    main()
