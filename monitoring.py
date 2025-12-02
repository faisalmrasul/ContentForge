import random
from datetime import datetime, timedelta
import pandas as pd

class MediaMonitor:
    def __init__(self):
        self.platforms = ['Twitter', 'Reddit', 'News', 'YouTube', 'TikTok']
        self.topics = [
            'AI Regulation', 'Quantum Computing', 'Sustainable Tech', 
            'Web3 Developments', 'Space Exploration', 'Biotech Breakthroughs',
            'Climate Tech', 'Cybersecurity', 'Metaverse', 'Edge Computing'
        ]
    
    def get_current_trends(self):
        """Simulate real-time trend monitoring"""
        trends = []
        for i in range(8):
            topic = random.choice(self.topics)
            volume = random.randint(1000, 50000)
            growth = random.uniform(5, 150)
            sentiment = random.uniform(-0.8, 0.8)
            
            trends.append({
                'topic': topic,
                'volume': volume,
                'growth_24h': f"{growth:.1f}%",
                'sentiment': sentiment,
                'platforms': random.sample(self.platforms, random.randint(1, 3)),
                'emerging': random.choice([True, False]),
                'timestamp': datetime.now() - timedelta(hours=random.randint(0, 12))
            })
        
        return trends
    
    def get_dashboard_data(self):
        """Generate dashboard visualization data"""
        # Generate time series data
        hours = 24
        timestamps = [datetime.now() - timedelta(hours=h) for h in range(hours, 0, -1)]
        
        data = {
            'trends': [],
            'topics': [],
            'overall_sentiment': 0.65  # Generally positive
        }
        
        # Create trending topics
        for i in range(10):
            topic = random.choice(self.topics)
            data['topics'].append({
                'Topic': topic,
                'Mentions': random.randint(1000, 50000),
                'Growth': f"{random.uniform(5, 200):.1f}%",
                'Sentiment': random.choice(['🔥 Very Positive', '😊 Positive', '😐 Neutral', '😟 Negative']),
                'Platforms': ', '.join(random.sample(self.platforms, 2))
            })
        
        # Create timeline data
        for ts in timestamps:
            data['trends'].append({
                'timestamp': ts,
                'mentions': random.randint(500, 3000),
                'sentiment': random.uniform(0.3, 0.9),
                'events': random.randint(0, 3)
            })
        
        return data