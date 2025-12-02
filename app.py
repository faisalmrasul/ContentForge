import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
from io import BytesIO

# Create a base64 encoded logo to avoid file dependencies
def get_base64_logo():
    # Simple SVG logo as base64
    logo_svg = """
    <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="60" cy="60" r="50" fill="url(#grad1)" stroke="#fff" stroke-width="3"/>
        <text x="60" y="65" font-family="Arial, sans-serif" font-size="28" font-weight="bold" 
              text-anchor="middle" fill="white">C</text>
        <text x="78" y="65" font-family="Arial, sans-serif" font-size="20" font-weight="bold" 
              text-anchor="middle" fill="white">AI</text>
        <circle cx="60" cy="60" r="15" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    """
    return base64.b64encode(logo_svg.encode()).decode()

# Page configuration
st.set_page_config(
    page_title="Chronos AI - Autonomous Content Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with embedded styles
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
    }
    .content-box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .content-box:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .success-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        color: #856404;
    }
    .pipeline-step {
        display: flex;
        align-items: center;
        margin: 10px 0;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 8px;
    }
    .step-number {
        background: #667eea;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-weight: bold;
    }
    .platform-tag {
        display: inline-block;
        background: #e9ecef;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'demo_step' not in st.session_state:
    st.session_state.demo_step = 0
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'selected_opportunity' not in st.session_state:
    st.session_state.selected_opportunity = None

# Sample data generators
def generate_trends():
    topics = ['AI Regulation', 'Quantum Computing', 'Sustainable Tech', 'Web3', 
              'Space Exploration', 'Biotech', 'Climate Tech', 'Cybersecurity']
    trends = []
    for topic in topics[:6]:
        trends.append({
            'topic': topic,
            'mentions': np.random.randint(1000, 50000),
            'growth': f"{np.random.uniform(5, 200):.1f}%",
            'sentiment': np.random.uniform(0.3, 0.9),
            'platforms': np.random.choice(['Twitter', 'Reddit', 'News', 'YouTube', 'TikTok'], 
                                         np.random.randint(2, 4), replace=False),
            'emerging': np.random.random() > 0.7
        })
    return trends

def generate_opportunities(trends):
    opportunities = []
    for i, trend in enumerate(trends[:3]):
        score = np.random.uniform(6.5, 9.5)
        opportunities.append({
            'id': i + 1,
            'title': f"Explain {trend['topic']} to Business Leaders",
            'trend': trend['topic'],
            'score': round(score, 1),
            'metrics': {
                'virality': round(np.random.uniform(6, 9), 1),
                'competition_gap': round(np.random.uniform(7, 10), 1),
                'audience_fit': round(np.random.uniform(6, 9), 1),
                'resource_efficiency': round(np.random.uniform(8, 10), 1)
            },
            'brief': f"Create accessible content explaining {trend['topic']} to non-experts, focusing on practical business implications.",
            'timing': f"Within {np.random.randint(1, 6)} hours"
        })
    return sorted(opportunities, key=lambda x: x['score'], reverse=True)

def generate_content(opportunity):
    return {
        'opportunity_title': opportunity['title'],
        'formats': {
            'tweet': [
                f"🚀 {opportunity['trend']} isn't just another tech trend—it's a fundamental shift in how we approach problem-solving.",
                f"1/ The core concept: {opportunity['trend'].lower()} enables exponential solutions to previously impossible problems.",
                f"2/ Business impact: Companies adopting early see 3-5x faster innovation cycles and competitive advantage.",
                f"3/ What's next: The next 12 months will determine which enterprises lead vs follow. Start exploring use cases now."
            ],
            'linkedin': f"""The Strategic Imperative: Understanding {opportunity['trend']}

As {opportunity['trend']} transitions from theoretical concept to practical tool, business leaders face a critical window of opportunity.

📊 Why This Matters Now:
• Market disruption expected within 18-24 months
• Early adopters are already seeing ROI
• Talent with {opportunity['trend'].lower()} expertise is scarce but crucial

🔍 Key Questions Every Leader Should Ask:
1. How will {opportunity['trend'].lower()} impact our industry specifically?
2. What are the first, lowest-risk applications we can pilot?
3. How do we build internal capability while the field evolves?

🚀 The Path Forward:
Start with education, move to experimentation, then scale successful pilots. The cost of waiting exceeds the risk of starting.

#BusinessStrategy #Innovation #DigitalTransformation #{opportunity['trend'].replace(' ', '')}""",
            'image_prompt': f"""Professional infographic about {opportunity['trend']}:

Style: Clean, corporate design with data visualization
Colors: Blue gradient theme (#667eea to #764ba2)
Elements:
1. Central icon representing {opportunity['trend'].lower()}
2. 3 key statistics in bold typography
3. Timeline showing adoption curve
4. Comparison: Traditional vs {opportunity['trend']} approach
5. Call-to-action: "Start your strategy today"

Layout: Optimized for social media (1080x1080)""",
            'video_script': f"""HOOK (0-5s): [Dynamic animation] "What if your biggest business challenge could be solved exponentially faster?"

EXPLANATION (5-30s): [Whiteboard animation] "Here's how {opportunity['trend']} works in simple terms..."

IMPACT (30-45s): [Real-world examples] "Companies using this are seeing..."

CALL TO ACTION (45-60s): [Clear text overlay] "3 steps to get started today..." """
        },
        'timing': {
            'twitter': "9:30 AM EST, Wednesday",
            'linkedin': "11:00 AM EST, Tuesday",
            'instagram': "2:00 PM EST, Thursday",
            'tiktok': "7:00 PM EST, Friday"
        },
        'hashtags': ['#AI', '#Tech', '#Innovation', '#Business', '#Future', f"#{opportunity['trend'].replace(' ', '')}"]
    }

# Header with embedded logo
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">Chronos AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Autonomous Content Intelligence System</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="warning-box">
    <strong>🚀 Live Demo Mode</strong> - This prototype showcases our end-to-end AI content pipeline. 
    Data is simulated for demonstration purposes.
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Embedded SVG logo
    logo_base64 = get_base64_logo()
    st.markdown(f'''
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{logo_base64}" width="120" height="120">
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# Introduction
st.markdown("""
### **The Future of Content Strategy: AI-Powered Intelligence Loop**
Chronos continuously monitors the digital landscape, identifies high-potential opportunities, 
creates optimized multi-format content, and learns from performance — all in real-time.
""")

# Key Metrics
st.subheader("📈 System Performance Metrics")
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    st.metric("Trends Monitored", "1.2M/hour", "+15%", delta_color="normal")
with metrics_col2:
    st.metric("Prediction Accuracy", "78.3%", "+4.2%", delta_color="normal")
with metrics_col3:
    st.metric("Content Velocity", "23 min", "-65%", delta_color="inverse")
with metrics_col4:
    st.metric("Engagement Lift", "+312%", "+47%", delta_color="normal")

# Main Demo Section
st.markdown("---")
st.subheader("🚀 Interactive Demo")

demo_col1, demo_col2 = st.columns([2, 1])
with demo_col1:
    # Show pipeline visualization
    st.markdown("""
    <div class="pipeline-step">
        <div class="step-number">1</div>
        <div><strong>Monitor</strong> - Real-time tracking across 20+ platforms</div>
    </div>
    <div class="pipeline-step">
        <div class="step-number">2</div>
        <div><strong>Discover</strong> - AI-powered opportunity scoring</div>
    </div>
    <div class="pipeline-step">
        <div class="step-number">3</div>
        <div><strong>Create</strong> - Multi-format content generation</div>
    </div>
    <div class="pipeline-step">
        <div class="step-number">4</div>
        <div><strong>Optimize</strong> - Platform-specific distribution</div>
    </div>
    """, unsafe_allow_html=True)

with demo_col2:
    if st.button("▶️ **Run Complete Pipeline**", use_container_width=True, type="primary"):
        with st.spinner("🕵️ **Monitoring digital landscape...**"):
            time.sleep(1)
            st.session_state.trends = generate_trends()
        
        with st.spinner("🧠 **Analyzing opportunities...**"):
            time.sleep(1)
            st.session_state.opportunities = generate_opportunities(st.session_state.trends)
            st.session_state.selected_opportunity = st.session_state.opportunities[0]
        
        with st.spinner("🎨 **Generating content...**"):
            time.sleep(2)
            st.session_state.generated_content = generate_content(st.session_state.selected_opportunity)
        
        st.session_state.demo_step = 3
        st.success("✅ **Pipeline complete!** Generated multi-format content package.")

# Pipeline Steps
tab1, tab2, tab3, tab4 = st.tabs(["📡 **Monitor**", "🔍 **Discover**", "🎨 **Create**", "🚀 **Optimize**"])

with tab1:
    st.subheader("Real-time Media Monitoring")
    
    if st.session_state.get('trends'):
        trends = st.session_state.trends
    else:
        trends = generate_trends()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Timeline chart
        hours = 24
        timestamps = [datetime.now() - timedelta(hours=h) for h in range(hours, 0, -1)]
        mentions = [np.random.randint(500, 3000) for _ in range(hours)]
        sentiment = [np.random.uniform(0.3, 0.9) for _ in range(hours)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=mentions,
            name='Mentions',
            line=dict(color='#667eea', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=[s * 3000 for s in sentiment],
            name='Sentiment',
            fill='tozeroy',
            line=dict(color='rgba(102, 126, 234, 0.3)', width=1),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='📊 Real-time Trend Volume & Sentiment',
            xaxis_title='Time',
            yaxis=dict(title='Mentions', side='left'),
            yaxis2=dict(title='Sentiment', side='right', overlaying='y', range=[0, 3000]),
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sentiment gauge
        overall_sentiment = np.mean([t['sentiment'] for t in trends])
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_sentiment * 100,
            title={'text': "📈 Overall Sentiment"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 33], 'color': "#ff6b6b"},
                    {'range': [33, 66], 'color': "#ffd93d"},
                    {'range': [66, 100], 'color': "#6bcf7f"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Trending topics table
    st.subheader("🔥 Trending Now")
    trends_df = pd.DataFrame(trends)
    trends_df['platforms'] = trends_df['platforms'].apply(lambda x: ', '.join(x))
    trends_df['sentiment_color'] = trends_df['sentiment'].apply(
        lambda x: '🟢' if x > 0.7 else '🟡' if x > 0.4 else '🔴'
    )
    
    # Format the display
    display_df = trends_df[['topic', 'mentions', 'growth', 'sentiment_color', 'platforms']].copy()
    display_df.columns = ['Topic', 'Mentions', 'Growth (24h)', 'Sentiment', 'Platforms']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Content Opportunity Discovery")
    
    if st.button("🔍 Analyze Current Trends", key="analyze_btn", use_container_width=True):
        trends = generate_trends()
        opportunities = generate_opportunities(trends)
        st.session_state.opportunities = opportunities
        
    if st.session_state.get('opportunities'):
        for i, opp in enumerate(st.session_state.opportunities):
            with st.expander(f"🎯 Opportunity #{i+1}: {opp['title']} (Score: {opp['score']}/10)", expanded=i==0):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Virality", f"{opp['metrics']['virality']}/10")
                col2.metric("Gap", f"{opp['metrics']['competition_gap']}/10")
                col3.metric("Audience", f"{opp['metrics']['audience_fit']}/10")
                col4.metric("Efficiency", f"{opp['metrics']['resource_efficiency']}/10")
                
                st.markdown(f"**Strategic Brief:** {opp['brief']}")
                st.markdown(f"**Optimal Timing:** {opp['timing']}")
                
                if st.button(f"Select & Generate Content", key=f"select_{i}", type="secondary"):
                    st.session_state.selected_opportunity = opp
                    st.session_state.generated_content = generate_content(opp)
                    st.success(f"✅ Selected: {opp['title']}")
                    st.rerun()

with tab3:
    st.subheader("AI-Powered Content Generation")
    
    if st.session_state.get('generated_content'):
        content = st.session_state.generated_content
        
        st.markdown(f"""
        <div class="success-box">
        <strong>✨ Generated Content Package</strong><br>
        Based on: {content['opportunity_title']}<br>
        Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)
        
        # Format tabs
        gen_tabs = st.tabs(["🐦 **Twitter**", "💼 **LinkedIn**", "🎨 **Visual**", "🎥 **Video**"])
        
        with gen_tabs[0]:
            st.markdown("#### Tweet Thread (4-part)")
            for i, tweet in enumerate(content['formats']['tweet']):
                st.markdown(f"""
                <div class="content-box">
                <strong>Tweet {i+1}:</strong><br>
                {tweet}
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"**⏱️ Optimal Timing:** {content['timing']['twitter']}")
            st.markdown(f"**🏷️ Hashtags:** {', '.join(content['hashtags'][:5])}")
        
        with gen_tabs[1]:
            st.markdown("#### LinkedIn Article Format")
            st.markdown(f"""
            <div class="content-box">
            {content['formats']['linkedin']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**⏱️ Optimal Timing:** {content['timing']['linkedin']}")
        
        with gen_tabs[2]:
            st.markdown("#### Visual Content Prompt")
            st.code(content['formats']['image_prompt'], language="text")
            st.markdown("""
            **🎯 AI Model:** Stable Diffusion XL<br>
            **📐 Aspect Ratio:** 1:1 (Square)<br>
            **🎨 Style:** Professional infographic
            """)
            
            # Generate a simple visual representation
            if st.button("🖼️ Generate Sample Layout", key="gen_layout"):
                st.markdown("""
                ```
                ┌─────────────────────────────────────┐
                │                                     │
                │          [MAIN ICON]               │
                │                                     │
                │  📊 Stat 1: 245% Growth            │
                │  🎯 Stat 2: 78% Adoption           │
                │  ⚡ Stat 3: 3.2x ROI               │
                │                                     │
                │  ┌─────────┐    ┌─────────┐        │
                │  │ Before  │ →  │ After   │        │
                │  │  Slow   │    │  Fast   │        │
                │  └─────────┘    └─────────┘        │
                │                                     │
                └─────────────────────────────────────┘
                ```
                """)
        
        with gen_tabs[3]:
            st.markdown("#### Video Script (60s Short-form)")
            st.markdown(f"""
            <div class="content-box">
            {content['formats']['video_script']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**🎬 Format:** Vertical (9:16)")
            st.markdown("**🎵 Music:** Upbeat corporate")
            st.markdown("**🎙️ Voiceover:** Professional, energetic")

with tab4:
    st.subheader("Distribution Optimization")
    
    if st.session_state.get('generated_content'):
        content = st.session_state.generated_content
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance prediction
            platforms = ['Twitter', 'LinkedIn', 'Instagram', 'TikTok']
            scores = [85, 78, 92, 95]
            colors = ['#1DA1F2', '#0077B5', '#E4405F', '#000000']
            
            fig = go.Figure(data=[go.Bar(
                x=platforms,
                y=scores,
                marker_color=colors,
                text=[f'{s}%' for s in scores],
                textposition='auto'
            )])
            fig.update_layout(
                title='📊 Predicted Engagement Score',
                yaxis=dict(title='Score (0-100)', range=[0, 100]),
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Timing optimization
            timing_data = pd.DataFrame({
                'Platform': platforms,
                'Best Time': ['9:30 AM', '11:00 AM', '2:00 PM', '7:00 PM'],
                'Best Day': ['Wednesday', 'Tuesday', 'Thursday', 'Friday'],
                'Audience': ['Professionals', 'B2B', 'Youth', 'Gen Z']
            })
            st.dataframe(timing_data, use_container_width=True, hide_index=True)
        
        # Personalization variants
        st.subheader("🎯 Personalization Variants")
        variants_col1, variants_col2, variants_col3 = st.columns(3)
        
        with variants_col1:
            st.markdown("""
            <div class="content-box">
            <strong>👔 Business Leaders</strong><br>
            Focus: ROI & Competitive Advantage<br>
            Tone: Strategic, data-driven<br>
            Hook: "The $4.2T opportunity in..."
            </div>
            """, unsafe_allow_html=True)
        
        with variants_col2:
            st.markdown("""
            <div class="content-box">
            <strong>👩‍💻 Tech Professionals</strong><br>
            Focus: Implementation & Stack<br>
            Tone: Technical, detailed<br>
            Hook: "The engineering behind..."
            </div>
            """, unsafe_allow_html=True)
        
        with variants_col3:
            st.markdown("""
            <div class="content-box">
            <strong>👥 General Public</strong><br>
            Focus: Daily Impact & Benefits<br>
            Tone: Accessible, story-driven<br>
            Hook: "How this changes your daily life..."
            </div>
            """, unsafe_allow_html=True)

# Technology Stack
st.markdown("---")
st.subheader("🛠️ Technology Stack")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
    **🤖 AI/ML Core**
    - GPT-4 & Claude for strategy
    - Stable Diffusion XL for visuals
    - Custom BERT models for monitoring
    - Prophet for trend forecasting
    """)

with tech_col2:
    st.markdown("""
    **⚙️ Infrastructure**
    - Real-time Kafka streams
    - Vector databases (Pinecone)
    - Kubernetes orchestration
    - Multi-region AWS deployment
    """)

with tech_col3:
    st.markdown("""
    **🔌 Integrations**
    - 20+ social/platform APIs
    - News aggregators
    - Analytics suites
    - CRM/Marketing automation
    """)

# Investment Ask
st.markdown("---")
st.subheader("💼 Investment Opportunity")

st.markdown("""
<div class="metric-card">
<h3>🚀 Seeking $2.5M Seed Round</h3>
<p><strong>📈 Traction:</strong> 6 pilot clients, 312% engagement lift proven</p>
<p><strong>🌍 Market:</strong> $42B content marketing industry, 16% CAGR</p>
<p><strong>👥 Team:</strong> Ex-Google, Meta AI researchers + serial entrepreneurs</p>
<p><strong>💰 Use of Funds:</strong></p>
<ul>
<li>Scale engineering team (8 hires)</li>
<li>Enhanced AI model development</li>
<li>Go-to-market expansion</li>
<li>Platform partnerships</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Contact & Next Steps
st.markdown("---")
contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col1:
    st.markdown("**📧 Contact:** ceo@chronos-ai.com")
    st.markdown("**📞 Schedule Demo:** calendly.com/chronos-ai")

with contact_col2:
    st.markdown("**🌐 Website:** chronos-ai.com")
    st.markdown("**📚 Documentation:** docs.chronos-ai.com")

with contact_col3:
    st.markdown("**👨‍💻 GitHub:** github.com/chronos-ai")
    st.markdown("**🐦 Twitter:** @ChronosAI")

# Add footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
<p><strong>Chronos AI Demo v1.0</strong> | Confidential Investor Preview</p>
<p><em>This demo showcases our proprietary AI content intelligence pipeline. 
All data is simulated for demonstration purposes.</em></p>
</div>
""", unsafe_allow_html=True)

# Add some sample data if needed
if st.sidebar.checkbox("📊 Show Raw Data"):
    st.sidebar.subheader("Sample Data")
    if st.session_state.get('trends'):
        st.sidebar.json(st.session_state.trends[:2])
    if st.session_state.get('opportunities'):
        st.sidebar.json(st.session_state.opportunities[:1])
