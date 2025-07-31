import streamlit as st
import pandas as pd
from utils.calculations import calculate_roas, calculate_incremental_roas

def show_roas_calculator():
    st.title("💰 ROAS Calculator")
    dm = st.session_state.data_manager
    if not st.session_state.get('data_loaded', False):
        st.info("Load data on Data Management page first.")
        return

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
