import pandas as pd
import pytest
from components.payouts import filter_payouts_by_date
from datetime import date

@pytest.fixture
def sample_payouts_df():
    # Sample data with various payment dates
    data = {
        'influencer_id': [1, 2, 3, 4],
        'total_payout': [100, 200, 300, 400],
        'payment_date': ['2024-01-10', '2024-01-15', '2024-01-20', '2024-02-01']
    }
    return pd.DataFrame(data)

@pytest.mark.parametrize(
    "start, end, expected_ids",
    [
        (date(2024, 1, 10), date(2024, 1, 20), [1, 2, 3]),  # inclusive
        (date(2024, 1, 15), date(2024, 1, 15), [2]),         # single day
        (date(2023, 12, 31), date(2024, 1, 9), []),          # before any
        (date(2024, 1, 21), date(2024, 1, 31), []),          # between
        (date(2024, 2, 1), date(2024, 2, 1), [4])            # boundary
    ]
)
def test_filter_payouts_by_date(sample_payouts_df, start, end, expected_ids):
    df = filter_payouts_by_date(sample_payouts_df, start, end)
    assert sorted(df['influencer_id'].tolist()) == expected_ids


def test_filter_payouts_type_mismatch(sample_payouts_df):
    # Ensure passing date objects works and no dtype errors raised
    try:
        df = filter_payouts_by_date(sample_payouts_df, date(2024,1,1), date(2024,12,31))
    except TypeError:
        pytest.fail("filter_payouts_by_date raised TypeError unexpectedly!")
