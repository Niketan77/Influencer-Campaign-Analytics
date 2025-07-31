import random
import pandas as pd
from datetime import datetime, timedelta


def generate_sample_data():
    """Generate realistic sample data for demo"""
    BRANDS = ['MuscleBlaze', 'HKVitals', 'Gritzo']
    PLATFORMS = ['Instagram', 'YouTube', 'Twitter']
    CATEGORIES = ['Fitness', 'Lifestyle', 'Health', 'Beauty', 'Sports']
    PRODUCTS = [
        'Protein Powder', 'Mass Gainer', 'Pre-Workout', 'Vitamins',
        'Multivitamins', 'Omega-3', 'Probiotics', 'Energy Bars'
    ]
    # Influencers
    influencers_data = []
    for i in range(1, 151):
        influencers_data.append({
            'id': i,
            'name': f'Influencer_{i}',
            'category': random.choice(CATEGORIES),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'follower_count': random.randint(1000, 1000000),
            'platform': random.choice(PLATFORMS),
            'created_date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        })
    influencers_df = pd.DataFrame(influencers_data)
    # Posts
    posts_data = []
    post_id = 1
    for influencer_id in range(1, 151):
        for _ in range(random.randint(5, 15)):
            reach = random.randint(1000, 100000)
            likes = random.randint(int(reach * 0.01), int(reach * 0.1))
            comments = random.randint(int(likes * 0.05), int(likes * 0.2))
            posts_data.append({
                'id': post_id,
                'influencer_id': influencer_id,
                'platform': random.choice(PLATFORMS),
                'date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
                'url': f'https://example.com/post/{post_id}',
                'caption': f'Sample post caption {post_id}',
                'reach': reach,
                'likes': likes,
                'comments': comments,
                'created_date': datetime.now().strftime('%Y-%m-%d')
            })
            post_id += 1
    posts_df = pd.DataFrame(posts_data)
    # Tracking data
    tracking_data = []
    tracking_id = 1
    campaigns = [f'Campaign_{i}' for i in range(1, 21)]
    for _ in range(5000):
        orders = random.randint(0, 10)
        revenue = round(orders * random.uniform(200, 2000), 2)
        tracking_data.append({
            'id': tracking_id,
            'source': 'influencer_post',
            'campaign': random.choice(campaigns),
            'influencer_id': random.randint(1, 150),
            'user_id': f'user_{random.randint(1000, 9999)}',
            'product': random.choice(PRODUCTS),
            'brand': random.choice(BRANDS),
            'date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
            'orders': orders,
            'revenue': revenue,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        })
        tracking_id += 1
    tracking_df = pd.DataFrame(tracking_data)
    # Payouts
    payouts_data = []
    payout_id = 1
    for influencer_id in range(1, 151):
        for _ in range(random.randint(1, 5)):
            basis = random.choice(['post', 'order'])
            if basis == 'post':
                rate = round(random.uniform(300, 2000), 2)
                posts = random.randint(1, 5)
                orders = 0
                total_payout = round(rate * posts, 2)
            else:
                rate = round(random.uniform(50, 200), 2)
                orders = random.randint(1, 20)
                posts = 0
                total_payout = round(rate * orders, 2)
            payouts_data.append({
                'id': payout_id,
                'influencer_id': influencer_id,
                'campaign': random.choice(campaigns),
                'basis': basis,
                'rate': rate,
                'orders': orders,
                'posts': posts,
                'total_payout': total_payout,
                'payment_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'status': random.choice(['pending', 'processing', 'paid']),
                'created_date': datetime.now().strftime('%Y-%m-%d')
            })
            payout_id += 1
    payouts_df = pd.DataFrame(payouts_data)
    return influencers_df, posts_df, tracking_df, payouts_df
