import random
from datetime import datetime, timedelta

class ContentGenerator:
    def __init__(self):
        self.tone_options = ['professional', 'conversational', 'provocative', 'educational', 'inspirational']
        self.hashtag_banks = {
            'tech': ['#AI', '#Tech', '#Innovation', '#Future', '#DigitalTransformation'],
            'business': ['#Business', '#Strategy', '#Leadership', '#Entrepreneurship'],
            'general': ['#Trending', '#News', '#Insights', '#Learn']
        }
    
    def create_content_package(self, opportunity, formats=None):
        """Generate multi-format content based on opportunity"""
        if formats is None:
            formats = ['tweet', 'linkedin', 'image_prompt']
        
        content = {
            'opportunity_title': opportunity['title'],
            'generated_at': datetime.now().isoformat(),
            'formats': {},
            'hashtags': self._generate_hashtags(opportunity['trend']),
            'timing': self._calculate_optimal_timing(),
            'performance_predictions': self._predict_performance()
        }
        
        # Generate each format
        if 'tweet' in formats:
            content['formats']['tweet'] = self._generate_tweet_thread(opportunity)
        
        if 'linkedin' in formats:
            content['formats']['linkedin'] = self._generate_linkedin_post(opportunity)
        
        if 'image_prompt' in formats:
            content['formats']['image_prompt'] = self._generate_image_prompt(opportunity)
        
        if 'video_script' in formats:
            content['formats']['video_script'] = self._generate_video_script(opportunity)
        
        return content
    
    def _generate_tweet_thread(self, opportunity):
        tweets = [
            f"🚀 Breaking down: {opportunity['trend']}\n\nWhy this matters now:",
            f"1. First key insight about {opportunity['trend'].lower()}",
            f"2. Second critical point that most people miss",
            f"3. Practical implications for different industries",
            f"4. What to watch for in the coming weeks/months"
        ]
        return tweets
    
    def _generate_linkedin_post(self, opportunity):
        post = f"""The conversation around {opportunity['trend']} is heating up, but most discussions miss the strategic implications.

Here's what leaders need to understand:

• The core shift happening
• How this affects competitive dynamics  
• Actionable steps to prepare
• Long-term opportunities emerging

This isn't just another trend—it's a fundamental shift in how we think about technology and business.

What's your take on {opportunity['trend']}? How is your organization preparing?"""
        return post
    
    def _generate_image_prompt(self, opportunity):
        styles = [
            "minimalist infographic style",
            "futuristic cyberpunk aesthetic",
            "clean corporate illustration",
            "abstract data visualization"
        ]
        
        prompt = f"""Create an engaging social media image about {opportunity['trend']}:

Style: {random.choice(styles)}
Key elements:
1. Central visual metaphor representing {opportunity['trend']}
2. 3 key data points/insights displayed clearly
3. Modern, clean typography
4. Brand colors: blue gradient with white accents
5. Platform optimized: 1080x1080 for Instagram, 1200x630 for LinkedIn

Mood: Professional yet innovative, forward-looking"""
        
        return prompt
    
    def _generate_video_script(self, opportunity):
        script = f"""OPENING HOOK (0-3 seconds):
[Eye-catching visual of {opportunity['trend']} in action]
"You've been hearing about {opportunity['trend']}, but here's what no one is telling you..."

KEY POINTS (3-45 seconds):
1. [Visual: Animated explainer] "The core concept in 30 seconds..."
2. [Visual: Data visualization] "Why this matters right now..."
3. [Visual: Real-world examples] "3 industries being transformed..."
4. [Visual: Future timeline] "Where this is headed next..."

CALL TO ACTION (45-60 seconds):
[Visual: Clear text overlay] "What's your take? Comment below!"
[Visual: Subscribe/follow prompt]"""
        
        return script
    
    def _generate_hashtags(self, topic):
        hashtags = []
        for category in self.hashtag_banks.values():
            hashtags.extend(random.sample(category, min(2, len(category))))
        hashtags.append(f"#{topic.replace(' ', '')}")
        return list(set(hashtags))
    
    def _calculate_optimal_timing(self):
        return {
            'twitter': "9:30 AM - 11:30 AM EST, Wednesday",
            'linkedin': "11:00 AM - 1:00 PM EST, Tuesday-Thursday",
            'instagram': "2:00 PM - 4:00 PM EST, Weekdays",
            'tiktok': "7:00 PM - 9:00 PM EST, Thursday-Friday"
        }
    
    def _predict_performance(self):
        return {
            'expected_engagement': random.randint(85, 98),
            'estimated_reach': f"{random.randint(5000, 50000):,}",
            'conversion_potential': f"{random.randint(2, 8)}%"
        }