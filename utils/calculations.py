import pandas as pd

# ROAS calculations
def calculate_roas(revenue: float, cost: float) -> float:
    if cost == 0:
        return 0.0
    return revenue / cost

def calculate_incremental_roas(campaign_revenue: float, baseline_revenue: float, campaign_cost: float) -> float:
    incremental = campaign_revenue - baseline_revenue
    if campaign_cost == 0:
        return 0.0
    return incremental / campaign_cost

def calculate_platform_roas(df: pd.DataFrame) -> pd.DataFrame:
    metrics = df.groupby('platform').agg({'revenue': 'sum', 'total_payout': 'sum'}).reset_index()
    metrics['roas'] = metrics.apply(lambda x: calculate_roas(x['revenue'], x['total_payout']), axis=1)
    return metrics

# Engagement and conversion

def calculate_engagement_rate(likes: int, comments: int, reach: int) -> float:
    if reach == 0:
        return 0.0
    return ((likes + comments) / reach) * 100.0

def calculate_conversion_rate(orders: int, reach: int) -> float:
    if reach == 0:
        return 0.0
    return (orders / reach) * 100.0

def analyze_influencer_performance(posts_df: pd.DataFrame, tracking_df: pd.DataFrame, payouts_df: pd.DataFrame) -> pd.DataFrame:
    """Comprehensive influencer performance analysis"""
    # Calculate engagement rate per post
    posts = posts_df.copy()
    posts['engagement_rate'] = posts.apply(
        lambda x: calculate_engagement_rate(x['likes'], x['comments'], x['reach']),
        axis=1
    )
    # Aggregate post metrics by influencer
    influencer_posts = posts.groupby('influencer_id').agg(
        reach=('reach', 'sum'),
        likes=('likes', 'sum'),
        comments=('comments', 'sum'),
        engagement_rate=('engagement_rate', 'mean')
    ).reset_index()
    # Aggregate revenue by influencer
    influencer_revenue = tracking_df.groupby('influencer_id')['revenue'].sum().reset_index()
    # Aggregate cost by influencer
    influencer_costs = payouts_df.groupby('influencer_id')['total_payout'].sum().reset_index()
    # Merge all metrics
    perf = influencer_posts.merge(influencer_revenue, on='influencer_id', how='left')
    perf = perf.merge(influencer_costs, on='influencer_id', how='left')
    # Fill missing values
    perf['revenue'] = perf['revenue'].fillna(0)
    perf['total_payout'] = perf['total_payout'].fillna(0)
    # Calculate ROAS
    perf['roas'] = perf.apply(
        lambda x: calculate_roas(x['revenue'], x['total_payout']),
        axis=1
    )
    return perf
