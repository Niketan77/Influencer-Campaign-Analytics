# Influencer Campaign Analytics Dashboard

This Streamlit application allows you to track and visualize influencer campaign performance and ROI using CSV data files and Pandas.

## Features

- **Data Management**: Upload or load demo data for influencers, posts, tracking, and payouts.
- **Overview Dashboard**: Key metrics (total revenue, active campaigns, influencers, avg. ROAS), time series and distribution charts.
- **Campaign Performance**: Multi-level filtering, metrics, scatter and timeline visualizations, platform comparison.
- **Influencer Analytics**: Engagement, revenue, cost, ROAS, top influencers bar chart, category and follower filters.
- **ROAS Calculator**: Overall and campaign-level ROAS and incremental ROAS calculations.
- **Payout Tracker**: Date-range filtering, monthly trend, top influencers by payout.
- **Automated Insights**: Top influencers, campaigns, revenue growth, and recommendations.
- **Export Data**: CSV, Excel, and PDF export of all datasets.

## Getting Started

### Prerequisites

- Python 3.9+
- Git (optional)

### Installation

1. Clone the repository:
   ```powershell
   git clone <repo-url>
   cd "e:\JOB Prepration\Potfolio\personal projects\Influencer Campaign Analytics"
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### Running the App

```powershell
streamlit run app.py
```

Go to the Streamlit UI at `http://localhost:8501`.

### Running Tests

```powershell
pip install pytest
pytest
```

## Project Structure

```
├── app.py
├── README.md
├── requirements.txt
├── data_processing/
├── pages/
├── utils/
└── tests/
    ├── test_calculations.py
    └── test_data_processing.py
```

## Documentation

See [docs/user_guide.md](docs/user_guide.md) for detailed usage and examples.
