import streamlit as st
from data_processing.data_manager import DataManager
from data_processing.sample_data_generator import generate_sample_data


def show_data_management():
    st.title("📁 Data Management")
    st.markdown("### Upload your data or explore with sample datasets")
    
    # Instructions section
    st.info("""
    **📋 Getting Started Instructions:**
    1. **New Users**: Click 'Load Demo Data' to explore the dashboard with sample data
    2. **Upload Data**: Use the file uploader to import your CSV files
    3. **Required Files**: influencers.csv, posts.csv, tracking.csv, payouts.csv
    """)
    
    # Expected data format guide
    with st.expander("📊 **Expected CSV Format Guide**", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **influencers.csv should contain:**
            - id, name, category, platform, follower_count
            
            **posts.csv should contain:**  
            - id, influencer_id, campaign, likes, comments, reach
            """)
        with col2:
            st.markdown("""
            **tracking.csv should contain:**
            - influencer_id, campaign, date, orders, revenue, brand, platform
            
            **payouts.csv should contain:**
            - influencer_id, campaign, total_payout, payment_date, status
            """)

    dm = st.session_state.data_manager

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🎭 **Try Demo Data**")
        st.markdown("Perfect for exploring features without uploading files")
        demo = st.button("🚀 Load Demo Data", type="primary", key="demo_data_btn")
    with col2:
        st.markdown("#### 📤 **Upload Your Data**") 
        st.markdown("Import your own CSV files for analysis")
        uploaded_files = st.file_uploader(
            "Upload CSV files", type=["csv"], accept_multiple_files=True
        )

    if demo:
        with st.spinner("Generating demo data..."):
            influencers_df, posts_df, tracking_df, payouts_df = generate_sample_data()
            dm.influencers_df = influencers_df
            dm.posts_df = posts_df
            dm.tracking_df = tracking_df
            dm.payouts_df = payouts_df
            st.success("Demo data loaded.")
        st.session_state.data_loaded = True

    elif uploaded_files:
        files_loaded = dm.load_csv_files(uploaded_files)
        valid, errors = dm.validate_data()
        if not valid:
            st.error("Data validation failed:")
            for err in errors:
                st.write(f"- {err}")
        else:
            st.success("All files loaded and validated.")
            st.session_state.data_loaded = True

    # Preview
    if st.session_state.get('data_loaded', False):
        st.subheader("Influencers")
        st.dataframe(dm.influencers_df)
        st.subheader("Posts")
        st.dataframe(dm.posts_df)
        st.subheader("Tracking Data")
        st.dataframe(dm.tracking_df)
        st.subheader("Payouts")
        st.dataframe(dm.payouts_df)

    else:
        st.info("No data loaded yet.")
