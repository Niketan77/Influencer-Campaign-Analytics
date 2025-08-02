import streamlit as st
import pandas as pd
from data_processing.data_manager import DataManager
from utils.calculations import calculate_roas


def show_insights():
    st.title("💡 Automated Insights")
    dm: DataManager = st.session_state.data_manager
    if not st.session_state.get('data_loaded', False):
        st.info("Load data on Data Management page first.")
        return

    # Merge and prepare data
    _, tracking_df = dm.get_merged_data()
    tracking_df['date'] = pd.to_datetime(tracking_df['date'])

    # Overall metrics
    total_rev = tracking_df['revenue'].sum()
    total_cost = dm.payouts_df['total_payout'].sum()
    overall_roas = calculate_roas(total_rev, total_cost)

    st.subheader("Overall Performance")
    st.markdown(f"- Total Revenue: ₹{total_rev:,.2f}")
    st.markdown(f"- Total Cost: ₹{total_cost:,.2f}")
    st.markdown(f"- Overall ROAS: {overall_roas:.2f}x")

    # Top 5 influencers by ROAS
    perf = tracking_df.groupby('influencer_id').agg({'revenue': 'sum'}).reset_index()
    cost_df = dm.payouts_df.groupby('influencer_id')['total_payout'].sum().reset_index()
    perf = perf.merge(cost_df, on='influencer_id', how='left').fillna(0)
    perf['roas'] = perf.apply(lambda x: calculate_roas(x['revenue'], x['total_payout']), axis=1)
    top_inf = perf.sort_values('roas', ascending=False).head(5)
    inf_df = dm.influencers_df[['id', 'name']]
    top_inf = top_inf.merge(inf_df, left_on='influencer_id', right_on='id')

    st.subheader("Top 5 Influencers by ROAS")
    for _, row in top_inf.iterrows():
        st.markdown(f"- {row['name']}: {row['roas']:.2f}x")

    # Top 5 campaigns by revenue
    camp_rev = (
        tracking_df.groupby('campaign')['revenue']
        .sum()
        .reset_index()
        .sort_values('revenue', ascending=False)
        .head(5)
    )
    st.subheader("Top 5 Campaigns by Revenue")
    for _, row in camp_rev.iterrows():
        st.markdown(f"- {row['campaign']}: ₹{row['revenue']:,.2f}")

    # Revenue growth month-over-month
    monthly = (
        tracking_df.set_index('date')
        .resample('M')['revenue']
        .sum()
        .reset_index()
    )
    monthly['pct_change'] = monthly['revenue'].pct_change() * 100
    if len(monthly) >= 2:
        latest = monthly.iloc[-1]
        change = latest['pct_change']
        st.subheader("Revenue Growth")
        st.markdown(f"Month-over-month ({latest['date'].strftime('%b %Y')}): {change:.2f}%")

    # Recommendations
    st.markdown("---")
    st.subheader("Recommendations")
    recommendations = [
        "Consider increasing budget for top-performing campaigns to amplify ROI.",
        "Re-evaluate payout structures for influencers with low ROAS.",
        "Explore underutilized platforms showing growth potential.",
    ]
    for rec in recommendations:
        st.markdown(f"- {rec}")
