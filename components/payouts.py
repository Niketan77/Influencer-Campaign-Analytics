import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

def filter_payouts_by_date(df: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    """Filter payouts DataFrame by date range using pandas Timestamps."""
    df = df.copy()
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    # Compare on pure date to avoid dtype mismatches
    df['payment_date_date'] = df['payment_date'].dt.date
    # Filter between Python date objects directly
    mask = (df['payment_date_date'] >= start_date) & (df['payment_date_date'] <= end_date)
    result = df.loc[mask].drop(columns=['payment_date_date'])
    return result

def show_payouts():
    st.title("💳 Payout Tracker")
    dm = st.session_state.data_manager
    if not st.session_state.get('data_loaded', False):
        st.info("Load data on Data Management page first.")
        return

    st.subheader("Payout Records")
    # Date filter on payment_date
    payouts_df = dm.payouts_df.copy()
    # Use Python date for date_input defaults
    payouts_df['payment_date'] = pd.to_datetime(payouts_df['payment_date'])
    min_date = payouts_df['payment_date'].min().date()
    max_date = payouts_df['payment_date'].max().date()
    # Allow unrestricted date selection for payment date filter
    selected_range = st.date_input(
        'Filter by Payment Date',
        # default and limits based on actual payment dates
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        start_date, end_date = selected_range
        payouts_df = filter_payouts_by_date(payouts_df, start_date, end_date)
    st.dataframe(payouts_df)

    st.markdown("---")
    # Monthly Payout Trend
    payouts_df['month'] = payouts_df['payment_date'].dt.to_period('M').dt.to_timestamp()
    monthly = payouts_df.groupby('month')['total_payout'].sum().reset_index()
    fig_month = px.bar(
        monthly, x='month', y='total_payout',
        title='Monthly Total Payouts', labels={'total_payout':'Total Payout (₹)','month':'Month'}
    )
    st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("---")
    # Top Influencers by Payout
    top_inf = (
        payouts_df.groupby('influencer_id')['total_payout']
        .sum().reset_index()
    )
    top_inf = top_inf.merge(dm.influencers_df[['id','name']], left_on='influencer_id', right_on='id')
    top_inf = top_inf.nlargest(10, 'total_payout')
    fig_top = px.bar(
        top_inf, x='name', y='total_payout',
        title='Top 10 Influencers by Payout', labels={'total_payout':'Total Payout (₹)','name':'Influencer'}
    )
    st.plotly_chart(fig_top, use_container_width=True)
