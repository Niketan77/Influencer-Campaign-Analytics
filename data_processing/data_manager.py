import pandas as pd

class DataManager:
    def __init__(self):
        self.influencers_df = None
        self.posts_df = None
        self.tracking_df = None
        self.payouts_df = None

    def load_csv_files(self, uploaded_files):
        """Load and validate all CSV files into dataframes"""
        files_loaded = {}
        for file in uploaded_files:
            name = file.name.lower()
            if name.startswith('influencers'):
                self.influencers_df = pd.read_csv(file)
                files_loaded['influencers'] = True
            elif name.startswith('posts'):
                self.posts_df = pd.read_csv(file)
                files_loaded['posts'] = True
            elif name.startswith('tracking'):
                self.tracking_df = pd.read_csv(file)
                files_loaded['tracking'] = True
            elif name.startswith('payouts'):
                self.payouts_df = pd.read_csv(file)
                files_loaded['payouts'] = True
        return files_loaded

    def validate_data(self):
        """Validate data integrity and relationships"""
        errors = []
        # Check loaded dataframes
        if self.influencers_df is None:
            errors.append("Influencers data not loaded")
        if self.posts_df is None:
            errors.append("Posts data not loaded")
        if self.tracking_df is None:
            errors.append("Tracking data not loaded")
        if self.payouts_df is None:
            errors.append("Payouts data not loaded")
        if errors:
            return False, errors
        # Validate relationships
        invalid_posts = ~self.posts_df['influencer_id'].isin(self.influencers_df['id'])
        if invalid_posts.any():
            errors.append("Some posts reference non-existent influencers")
        return len(errors) == 0, errors

    def get_merged_data(self):
        """Merge posts and tracking data with influencer info"""
        posts_with_influencers = self.posts_df.merge(
            self.influencers_df,
            left_on='influencer_id',
            right_on='id',
            suffixes=('_post', '_influencer')
        )
        tracking_with_influencers = self.tracking_df.merge(
            self.influencers_df,
            left_on='influencer_id',
            right_on='id',
            suffixes=('_tracking', '_influencer')
        )
        return posts_with_influencers, tracking_with_influencers
