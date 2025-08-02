import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing.data_manager import DataManager
from utils.calculations import analyze_influencer_performance


def show_influencers():
    st.title("👥 Influencer Analytics")
    dm: DataManager = st.session_state.data_manager
    if not st.session_state.get('data_loaded', False):
        st.info("Load data on Data Management page first.")
        return

    perf = analyze_influencer_performance(
        dm.posts_df, dm.tracking_df, dm.payouts_df
    )
    perf['roas'] = perf['roas'].round(2)
    # Filters: Category and Follower Count
    categories = ['All'] + sorted(dm.influencers_df['category'].dropna().unique())
    selected_cat = st.selectbox('Category Filter', categories)
    min_fol = int(dm.influencers_df['follower_count'].min())
    max_fol = int(dm.influencers_df['follower_count'].max())
    fol_range = st.slider('Follower Count Range', min_fol, max_fol, (min_fol, max_fol))
    # Merge category and follower_count
    perf = perf.merge(dm.influencers_df[['id','name','category','follower_count']], left_on='influencer_id', right_on='id')
    if selected_cat != 'All':
        perf = perf[perf['category'] == selected_cat]
    perf = perf[(perf['follower_count'] >= fol_range[0]) & (perf['follower_count'] <= fol_range[1])]
    st.subheader("Influencer Performance Metrics")
    st.dataframe(perf)
    # Top Influencers by ROAS
    st.markdown("---")
    top_inf = perf.sort_values('roas', ascending=False).head(10)
    fig_inf = px.bar(top_inf, x='name', y='roas', title='Top 10 Influencers by ROAS', labels={'roas':'ROAS','name':'Influencer'})
    st.plotly_chart(fig_inf, use_container_width=True)
