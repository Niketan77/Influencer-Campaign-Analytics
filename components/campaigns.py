import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing.data_manager import DataManager
from utils.visualizations import create_dynamic_filters

def show_campaign_performance():
    st.title("📈 Campaign Performance")
    st.markdown("### Deep-dive into campaign metrics and ROI analysis")
    dm: DataManager = st.session_state.data_manager
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ **No Data Loaded**")
        st.info("👆 Navigate to **Data Management** page first to load your data or demo data")
        st.markdown("---")
        st.markdown("""
        **This page provides:**
        - 🎯 Campaign filtering by date, brand, platform
        - 📊 Performance metrics (orders, revenue, ROAS)
        - 🔍 Influencer performance scatter plots
        - 📅 Timeline analysis of orders and revenue
        - 🏆 Platform comparison insights
        """)
        return

    st.info("💡 **Tip:** Use the filters below to analyze specific campaigns, date ranges, or platforms")

    # Get merged tracking data
    _, tracking_with_influencers = dm.get_merged_data()

    # Apply dynamic filters
    filtered_df, filters = create_dynamic_filters(tracking_with_influencers)

    # Performance metrics
    total_orders = int(filtered_df['orders'].sum())
    total_revenue = filtered_df['revenue'].sum()
    # Filter payouts based on campaign filter
    payouts_df = dm.payouts_df
    if filters['campaign'] != 'All':
        payouts_df = payouts_df[payouts_df['campaign'] == filters['campaign']]
    total_cost = payouts_df['total_payout'].sum()
    avg_roas = (total_revenue / total_cost) if total_cost > 0 else 0

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", total_orders)
    col2.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col3.metric("Total Cost", f"₹{total_cost:,.2f}")
    col4.metric("Avg ROAS", f"{avg_roas:.2f}x")

    st.markdown("---")

    # Performance by Influencer
    perf_df = (filtered_df.groupby(['influencer_id', 'name'])
               .agg(orders=('orders', 'sum'), revenue=('revenue', 'sum'))
               .reset_index())
    # Merge cost per influencer
    cost_df = payouts_df.groupby('influencer_id')['total_payout'].sum().reset_index()
    perf_df = perf_df.merge(cost_df, on='influencer_id', how='left').fillna(0)
    perf_df['roas'] = perf_df.apply(lambda x: x['revenue'] / x['total_payout'] if x['total_payout'] > 0 else 0, axis=1)
    perf_df['roas'] = perf_df['roas'].round(2)

    st.subheader("Influencer Performance Scatter")
    fig_scatter = px.scatter(perf_df, x='revenue', y='roas', size='orders',
                             hover_data=['name'], title="ROAS vs Revenue by Influencer")
    st.plotly_chart(fig_scatter, use_container_width=True, key="campaign_scatter_chart")

    st.markdown("---")

    # Timeline: revenue and orders over time
    time_df = (filtered_df.groupby('date')
               .agg(orders=('orders', 'sum'), revenue=('revenue', 'sum'))
               .reset_index())
    time_df['date'] = pd.to_datetime(time_df['date'])
    st.subheader("Timeline: Orders and Revenue Over Time")
    fig_time = px.line(time_df, x='date', y=['orders', 'revenue'], title="Orders and Revenue Trend")
    st.plotly_chart(fig_time, use_container_width=True, key="campaign_time_chart")

    st.markdown("---")

    # Platform comparison
    plat_df = (filtered_df.groupby('platform')['revenue']
               .sum().reset_index())
    st.subheader("Revenue by Platform")
    fig_platform = px.bar(plat_df, x='platform', y='revenue',
                          title="Revenue by Platform", labels={'revenue':'Revenue (₹)'})
    st.plotly_chart(fig_platform, use_container_width=True, key="campaign_platform_chart")
