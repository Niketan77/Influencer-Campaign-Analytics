import streamlit as st
from data_processing.data_manager import DataManager
from data_processing.sample_data_generator import generate_sample_data
import pages.data_management as dm
import pages.export as export
import pages.insights as insights
import pages.overview as overview
import pages.campaigns as campaigns
import pages.influencers as influencers
import pages.roas_calculator as roas_calculator
import pages.payouts as payouts
# ... import other pages as they are implemented

def initialize_session_state():
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


def main():
    st.set_page_config(
        page_title="Influencer Campaign Dashboard",
        page_icon="📊",
        layout="wide"
    )
    initialize_session_state()
    page = st.sidebar.selectbox(
        "Navigate to",
        [
            "Overview",
            "Campaign Performance",
            "Influencer Analytics",
            "ROAS Calculator",
            "Payout Tracker",
            "Insights",
            "Export Data",
            "Data Management"
        ]
    )
    if page == "Overview":
        overview.show_overview()
    elif page == "Campaign Performance":
        campaigns.show_campaign_performance()
    elif page == "Influencer Analytics":
        influencers.show_influencers()
    elif page == "ROAS Calculator":
        roas_calculator.show_roas_calculator()
    elif page == "Payout Tracker":
        payouts.show_payouts()
    elif page == "Insights":
        insights.show_insights()
    elif page == "Export Data":
        export.show_export_data()
    elif page == "Data Management":
        dm.show_data_management()
    # elif other pages

if __name__ == "__main__":
    main()
