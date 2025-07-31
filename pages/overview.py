import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing.data_manager import DataManager

def show_overview():
    st.title("📊 Overview Dashboard")
    dm: DataManager = st.session_state.data_manager

    # Ensure data loaded
    if not st.session_state.get('data_loaded', False):
        st.info("Load data on Data Management page first.")
        return

    # Key metrics
    total_revenue = dm.tracking_df['revenue'].sum()
    total_cost = dm.payouts_df['total_payout'].sum()
    active_campaigns = dm.tracking_df['campaign'].nunique()
    total_influencers = dm.influencers_df.shape[0]
    avg_roas = (total_revenue / total_cost) if total_cost > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("Active Campaigns", active_campaigns)
    col3.metric("Total Influencers", total_influencers)
    col4.metric("Avg ROAS", f"{avg_roas:.2f}x")

    st.markdown("---")

    # Revenue Trend Over Time
    daily_revenue = (
        dm.tracking_df.groupby('date')['revenue']
        .sum()
        .reset_index()
    )
    daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
    fig_trend = px.line(
        daily_revenue,
        x='date', y='revenue',
        title='Revenue Trend Over Time',
        labels={'revenue':'Revenue (₹)', 'date':'Date'}
    )
    st.plotly_chart(fig_trend, use_container_width=True, key="overview_trend_chart")

    st.markdown("---")

    # Brand Revenue Comparison
    brand_rev = (
        dm.tracking_df.groupby('brand')['revenue']
        .sum()
        .reset_index()
    )
    fig_brand = px.bar(
        brand_rev,
        x='brand', y='revenue',
        title='Revenue by Brand',
        labels={'revenue':'Revenue (₹)', 'brand':'Brand'}
    )
    st.plotly_chart(fig_brand, use_container_width=True, key="overview_brand_chart")

    st.markdown("---")
    # Top 5 Influencers by Revenue
    inf_rev = (
        dm.tracking_df.groupby('influencer_id')['revenue']
        .sum().reset_index()
    )
    inf_rev = inf_rev.merge(
        dm.influencers_df[['id', 'name']],
        left_on='influencer_id', right_on='id'
    )
    top_inf = inf_rev.nlargest(5, 'revenue')
    fig_inf = px.bar(
        top_inf, x='name', y='revenue',
        title='Top 5 Influencers by Revenue',
        labels={'revenue':'Revenue (₹)', 'name':'Influencer'}
    )
    st.plotly_chart(fig_inf, use_container_width=True, key="overview_top_influencers_chart")

    st.markdown("---")
    # Payout Status Distribution
    status_counts = dm.payouts_df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    # Pie chart for payment status
    fig_status = px.pie(
        status_counts,
        names='status',
        values='count',
        title='Payout Status Distribution'
    )
    st.plotly_chart(fig_status, use_container_width=True, key="overview_status_pie_chart")
    # Removed duplicate pie chart to avoid duplicate element IDs
