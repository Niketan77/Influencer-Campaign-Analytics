import pytest
import pandas as pd
from utils.calculations import calculate_roas, calculate_incremental_roas, calculate_engagement_rate, calculate_conversion_rate, analyze_influencer_performance

def test_calculate_roas_zero_cost():
    assert calculate_roas(1000, 0) == 0.0

@pytest.mark.parametrize("revenue,cost,expected", [
    (1000, 500, 2.0),
    (0, 100, 0.0),
    (750, 250, 3.0)
])
def test_calculate_roas_basic(revenue, cost, expected):
    assert calculate_roas(revenue, cost) == expected

@pytest.mark.parametrize("campaign_rev,baseline,cost,expected", [
    (200, 100, 50, 2.0),
    (100, 150, 50, -1.0),
    (0, 100, 50, -2.0)
])
def test_calculate_incremental_roas(campaign_rev, baseline, cost, expected):
    assert calculate_incremental_roas(campaign_rev, baseline, cost) == expected

@pytest.mark.parametrize("likes,comments,reach,expected", [
    (100, 50, 1000, 15.0),
    (0, 0, 100, 0.0)
])
def test_engagement_conversion(likes, comments, reach, expected):
    assert calculate_engagement_rate(likes, comments, reach) == expected
    assert calculate_conversion_rate(comments, reach) == pytest.approx(comments/reach*100)


def test_analyze_influencer_performance():
    posts = pd.DataFrame({
        'influencer_id': [1,1], 'likes': [10,20], 'comments': [2,3], 'reach':[100,200]
    })
    tracking = pd.DataFrame({'influencer_id':[1,1], 'revenue':[100,200]})
    payouts = pd.DataFrame({'influencer_id':[1], 'total_payout':[50]})
    perf = analyze_influencer_performance(posts, tracking, payouts)
    assert 'roas' in perf.columns
    assert perf.loc[0,'revenue'] == 300
    assert perf.loc[0,'total_payout'] == 50
    assert perf.loc[0,'roas'] == pytest.approx(300/50)
