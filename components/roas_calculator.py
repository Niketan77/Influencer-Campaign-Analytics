import streamlit as st
import pandas as pd
from utils.calculations import calculate_roas, calculate_incremental_roas

def show_roas_calculator():
    st.title("💰 ROAS Calculator")
    st.markdown("### Return on Ad Spend analysis and profitability insights")
    dm = st.session_state.data_manager
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ **No Data Loaded**")
        st.info("👆 Navigate to **Data Management** page first to load your data or demo data")
        st.markdown("---")
        st.markdown("""
        **ROAS Calculator provides:**
        - 💵 Overall portfolio ROAS
        - 📊 Campaign-level ROAS breakdown
        - 📈 Incremental ROAS calculations  
        - ⚖️ Break-even analysis per campaign
        - 🎯 ROI optimization insights
        """)
        return

    # Help section
    with st.expander("ℹ️ **Understanding ROAS Metrics**"):
        st.markdown("""
        - **ROAS**: Return on Ad Spend = Revenue ÷ Cost
        - **Good ROAS**: Typically 4:1 or higher (400% return)
        - **Incremental ROAS**: Additional return from specific campaigns
        - **Break-even**: Point where revenue equals cost (1:1 ratio)
        """)

    # Overall ROAS
    total_revenue = dm.tracking_df['revenue'].sum()
    total_cost = dm.payouts_df['total_payout'].sum()
    overall_roas = calculate_roas(total_revenue, total_cost)
    st.metric("Overall ROAS", f"{overall_roas:.2f}x")

    st.markdown("---")
    st.subheader("Campaign-level ROAS")
    # Calculate campaign ROAS
    rev_by_campaign = dm.tracking_df.groupby('campaign')['revenue'].sum()
    cost_by_campaign = dm.payouts_df.groupby('campaign')['total_payout'].sum()
    camp_df = pd.DataFrame({'revenue': rev_by_campaign, 'total_payout': cost_by_campaign}).fillna(0)
    # Basic ROAS
    camp_df['roas'] = camp_df.apply(lambda x: calculate_roas(x['revenue'], x['total_payout']), axis=1)
    # Incremental ROAS: baseline = total revenue - campaign revenue
    total_rev = dm.tracking_df['revenue'].sum()
    camp_df = camp_df.reset_index()
    camp_df['incremental_roas'] = camp_df.apply(
        lambda x: calculate_incremental_roas(x['revenue'], total_rev - x['revenue'], x['total_payout']),
        axis=1
    )
    camp_df['incremental_roas'] = camp_df['incremental_roas'].round(2)
    # Break-even revenue equal to cost
    camp_df['break_even'] = camp_df['total_payout']
    st.dataframe(camp_df)
