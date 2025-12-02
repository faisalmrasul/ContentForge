import random

class ContentDiscoverer:
    def __init__(self):
        self.opportunity_templates = [
            {
                'title': "Explain {topic} to {audience}",
                'audiences': ['beginners', 'business leaders', 'developers', 'students'],
                'formats': ['explainer video', 'thread', 'blog post', 'infographic']
            },
            {
                'title': "Counter-misinformation about {topic}",
                'audiences': ['general public', 'industry professionals'],
                'formats': ['fact-check article', 'video debunk', 'twitter thread']
            },
            {
                'title': "Future implications of {topic}",
                'audiences': ['strategists', 'investors', 'policy makers'],
                'formats': ['thought leadership', 'research brief', 'podcast']
            }
        ]
    
    def analyze_trends(self, trends):
        """Analyze trends and identify content opportunities"""
        opportunities = []
        
        for i, trend in enumerate(trends[:4]):  # Top 4 trends
            template = random.choice(self.opportunity_templates)
            title = template['title'].format(
                topic=trend['topic'],
                audience=random.choice(template['audiences'])
            )
            
            score = random.uniform(6.5, 9.5)
            
            opportunity = {
                'id': i + 1,
                'title': title,
                'trend': trend['topic'],
                'score': round(score, 1),
                'metrics': {
                    'virality': round(random.uniform(6, 9), 1),
                    'competition_gap': round(random.uniform(7, 10), 1),
                    'audience_fit': round(random.uniform(6, 9), 1),
                    'resource_efficiency': round(random.uniform(8, 10), 1)
                },
                'brief': self._generate_brief(trend['topic']),
                'recommended_formats': random.sample(template['formats'], random.randint(2, 3)),
                'timing': f"Within {random.randint(1, 6)} hours"
            }
            
            opportunities.append(opportunity)
        
        # Sort by score
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        return opportunities
    
    def _generate_brief(self, topic):
        briefs = [
            f"Create accessible content explaining {topic} to non-experts, focusing on practical implications rather than technical details.",
            f"Address common misconceptions about {topic} with data-driven evidence and expert opinions.",
            f"Explore how {topic} will impact different industries over the next 2-5 years, with specific examples.",
            f"Compare and contrast {topic} with similar technologies/trends, highlighting unique advantages.",
            f"Create a guide for businesses looking to implement or respond to {topic}, with actionable steps."
        ]
        return random.choice(briefs)