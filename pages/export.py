import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


def show_export_data():
    st.title("📤 Export Data")
    dm = st.session_state.data_manager
    if not st.session_state.get('data_loaded', False):
        st.info("Load data on Data Management page first.")
        return

    datasets = {
        "Influencers": dm.influencers_df,
        "Posts": dm.posts_df,
        "Tracking Data": dm.tracking_df,
        "Payouts": dm.payouts_df
    }
    dataset_name = st.selectbox("Select dataset to export", list(datasets.keys()))
    df = datasets[dataset_name]
    st.write(df.head())

    # CSV export
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {dataset_name} as CSV",
        data=csv_bytes,
        file_name=f"{dataset_name}.csv",
        mime="text/csv"
    )

    # Excel export
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=dataset_name)
    st.download_button(
        label=f"Download {dataset_name} as Excel",
        data=excel_buffer.getvalue(),
        file_name=f"{dataset_name}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # PDF export (first 20 rows)
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    data = [df.columns.tolist()] + df.head(20).values.tolist()
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    doc.build([table])
    st.download_button(
        label=f"Download {dataset_name} as PDF (first 20 rows)",
        data=pdf_buffer.getvalue(),
        file_name=f"{dataset_name}.pdf",
        mime="application/pdf"
    )
