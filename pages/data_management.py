import streamlit as st
from data_processing.data_manager import DataManager
from data_processing.sample_data_generator import generate_sample_data


def show_data_management():
    st.title("📁 Data Management")
    st.markdown("Upload or load demo CSV files for influencers, posts, tracking data, and payouts.")

    dm = st.session_state.data_manager

    col1, col2 = st.columns(2)
    with col1:
        demo = st.button("Load Demo Data")
    with col2:
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
