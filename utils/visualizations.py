import streamlit as st
import pandas as pd

def create_dynamic_filters(df: pd.DataFrame):
    """Create filter widgets and apply to df"""
    # Row 1 filters: Brand, Platform, Campaign, Product
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        brands = ['All'] + sorted(df['brand'].dropna().unique())
        selected_brand = st.selectbox('Brand', brands)
    with col2:
        platforms = ['All'] + sorted(df['platform'].dropna().unique())
        selected_platform = st.selectbox('Platform', platforms)
    with col3:
        campaigns = ['All'] + sorted(df['campaign'].dropna().unique())
        selected_campaign = st.selectbox('Campaign', campaigns)
    with col4:
        products = ['All'] + sorted(df['product'].dropna().unique())
        selected_product = st.selectbox('Product', products)
    # Row 2 filters: Category, Date Range
    col5, col6 = st.columns(2)
    with col5:
        categories = ['All'] + sorted(df['category'].dropna().unique())
        selected_category = st.selectbox('Category', categories)
    with col6:
        date_min = pd.to_datetime(df['date']).min()
        date_max = pd.to_datetime(df['date']).max()
        selected_dates = st.date_input('Date Range', value=(date_min, date_max), min_value=date_min, max_value=date_max)
    filtered = df.copy()
    if selected_brand != 'All':
        filtered = filtered[filtered['brand'] == selected_brand]
    if selected_platform != 'All':
        filtered = filtered[filtered['platform'] == selected_platform]
    if selected_campaign != 'All':
        filtered = filtered[filtered['campaign'] == selected_campaign]
    if selected_product != 'All':
        filtered = filtered[filtered['product'] == selected_product]
    if selected_category != 'All':
        filtered = filtered[filtered['category'] == selected_category]
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        filtered['date'] = pd.to_datetime(filtered['date'])
        filtered = filtered[(filtered['date'] >= pd.to_datetime(selected_dates[0])) & (filtered['date'] <= pd.to_datetime(selected_dates[1]))]
    filters = {
        'brand': selected_brand,
        'platform': selected_platform,
        'campaign': selected_campaign,
        'product': selected_product,
        'category': selected_category,
        'date_range': selected_dates
    }
    return filtered, filters
