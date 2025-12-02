import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
from PIL import Image
import sys
import os

sys.path.append('utils')
from monitoring import MediaMonitor
from discovery import ContentDiscoverer
from generation import ContentGenerator
from visualization import create_timeline, create_sentiment_gauge, create_topic_network

# Page configuration
st.set_page_config(
    page_title="Chronos AI - Autonomous Content Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0;
    }
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-top: 0;
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
    }
    .content-box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'monitor' not in st.session_state:
    st.session_state.monitor = MediaMonitor()
if 'discoverer' not in st.session_state:
    st.session_state.discoverer = ContentDiscoverer()
if 'generator' not in st.session_state:
    st.session_state.generator = ContentGenerator()
if 'demo_step' not in st.session_state:
    st.session_state.demo_step = 0
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}

def run_demo_pipeline():
    """Run the complete Chronos pipeline"""
    with st.spinner("🕵️ **Monitoring digital landscape...**"):
        time.sleep(1)
        trends = st.session_state.monitor.get_current_trends()
    
    with st.spinner("🧠 **Analyzing opportunities...**"):
        time.sleep(1)
        opportunities = st.session_state.discoverer.analyze_trends(trends)
    
    with st.spinner("🎨 **Generating content...**"):
        time.sleep(2)
        if opportunities:
            content = st.session_state.generator.create_content_package(
                opportunities[0],  # Use top opportunity
                formats=['tweet', 'linkedin', 'image_prompt', 'video_script']
            )
            st.session_state.generated_content = content
    
    st.session_state.demo_step = 3
    st.success("✅ **Pipeline complete!** Generated multi-format content package.")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">Chronos AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Autonomous Content Intelligence System</p>', unsafe_allow_html=True)
with col2:
    st.image("assets/logos/chronos_logo.png", width=120)

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
    st.metric("Trends Monitored", "1.2M/hour", "+15%")
with metrics_col2:
    st.metric("Prediction Accuracy", "78.3%", "+4.2%")
with metrics_col3:
    st.metric("Content Velocity", "23 min", "-65%")
with metrics_col4:
    st.metric("Engagement Lift", "+312%", "+47%")

# Main Demo Section
st.markdown("---")
st.subheader("🚀 Interactive Demo")

demo_col1, demo_col2 = st.columns([2, 1])
with demo_col2:
    st.markdown("""
    ### **Demo Pipeline**
    1. **Monitor** - Track trends across platforms
    2. **Discover** - Identify high-value opportunities  
    3. **Create** - Generate multi-format content
    4. **Optimize** - Platform-specific optimization
    """)
    
    if st.button("▶️ Run Complete Pipeline", use_container_width=True):
        run_demo_pipeline()

# Pipeline Steps
tab1, tab2, tab3, tab4 = st.tabs(["📡 Monitor", "🔍 Discover", "🎨 Create", "🚀 Optimize"])

with tab1:
    st.subheader("Real-time Media Monitoring")
    
    # Simulated data stream
    monitor_data = st.session_state.monitor.get_dashboard_data()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = create_timeline(monitor_data['trends'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = create_sentiment_gauge(monitor_data['overall_sentiment'])
        st.plotly_chart(fig2, use_container_width=True)
    
    # Trending topics
    st.subheader("🔥 Trending Now")
    topics_df = pd.DataFrame(monitor_data['topics'])
    st.dataframe(topics_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Content Opportunity Discovery")
    
    if st.button("Analyze Current Trends", key="analyze_btn"):
        with st.spinner("Discovering opportunities..."):
            trends = st.session_state.monitor.get_current_trends()
            opportunities = st.session_state.discoverer.analyze_trends(trends)
            st.session_state.demo_step = 2
            
            for i, opp in enumerate(opportunities[:3]):
                with st.expander(f"🎯 Opportunity #{i+1}: {opp['title']} (Score: {opp['score']}/10)", expanded=i==0):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Virality Potential", f"{opp['metrics']['virality']}/10")
                    col2.metric("Competition Gap", f"{opp['metrics']['competition_gap']}/10")
                    col3.metric("Audience Fit", f"{opp['metrics']['audience_fit']}/10")
                    
                    st.markdown(f"**Strategic Brief:** {opp['brief']}")
                    
                    if st.button(f"Select This Opportunity", key=f"select_{i}"):
                        st.session_state.selected_opportunity = opp
                        st.success(f"Selected: {opp['title']}")

with tab3:
    st.subheader("AI-Powered Content Generation")
    
    if st.session_state.get('generated_content'):
        content = st.session_state.generated_content
        
        st.markdown(f"### ✨ Generated Content Package")
        st.markdown(f"**Based on:** {content['opportunity_title']}")
        
        # Format tabs
        gen_tabs = st.tabs(["Twitter", "LinkedIn", "Visual", "Video"])
        
        with gen_tabs[0]:
            st.markdown("#### Tweet Thread")
            for i, tweet in enumerate(content['formats']['tweet']):
                st.markdown(f"""
                <div class="content-box">
                <strong>Tweet {i+1}:</strong><br>
                {tweet}<br>
                <em>⏱️ Optimal timing: {content['timing']['twitter']}</em>
                </div>
                """, unsafe_allow_html=True)
        
        with gen_tabs[1]:
            st.markdown("#### LinkedIn Post")
            st.markdown(f"""
            <div class="content-box">
            {content['formats']['linkedin']}<br><br>
            <strong>Hashtags:</strong> {', '.join(content['hashtags'][:5])}<br>
            <em>⏱️ Optimal timing: {content['timing']['linkedin']}</em>
            </div>
            """, unsafe_allow_html=True)
        
        with gen_tabs[2]:
            st.markdown("#### Visual Content Prompt")
            st.code(content['formats']['image_prompt'], language="text")
            st.markdown("""
            *Would generate using Stable Diffusion/DALL-E 3*
            """)
            
            # Simulated image generation
            if st.button("Generate Preview Image", key="gen_image"):
                st.image("assets/sample_generated_image.png", caption="AI-Generated Visual Concept")
        
        with gen_tabs[3]:
            st.markdown("#### Video Script Outline")
            st.markdown(f"""
            <div class="content-box">
            {content['formats']['video_script']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Duration:** 60-90 seconds")
            st.markdown("**Format:** Vertical/short-form optimized")

with tab4:
    st.subheader("Distribution Optimization")
    
    if st.session_state.get('generated_content'):
        content = st.session_state.generated_content
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Performance Prediction")
            platforms = ['Twitter', 'LinkedIn', 'Instagram', 'TikTok']
            scores = [85, 78, 92, 95]
            
            fig = go.Figure(data=[go.Bar(
                x=platforms,
                y=scores,
                marker_color=['#1DA1F2', '#0077B5', '#E4405F', '#000000']
            )])
            fig.update_layout(
                title="Predicted Engagement Score by Platform",
                yaxis_title="Score (0-100)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⏰ Optimal Timing")
            timing_data = pd.DataFrame({
                'Platform': ['Twitter', 'LinkedIn', 'Instagram', 'TikTok'],
                'Best Time': ['9:30 AM', '11:00 AM', '2:00 PM', '7:00 PM'],
                'Day': ['Wed', 'Tue', 'Thu', 'Fri']
            })
            st.dataframe(timing_data, use_container_width=True, hide_index=True)
        
        st.markdown("### 🎯 Personalization Variants")
        variants = [
            {"Audience": "Tech Professionals", "Hook": "The data engineering implications..."},
            {"Audience": "Business Leaders", "Hook": "How this affects Q4 ROI..."},
            {"Audience": "General Consumers", "Hook": "Here's why you should care..."},
        ]
        st.dataframe(pd.DataFrame(variants), use_container_width=True)

# Technology Stack
st.markdown("---")
st.subheader("🛠️ Technology Stack")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
    **AI/ML Core**
    - GPT-4 & Claude for strategy
    - Stable Diffusion XL for visuals
    - Custom BERT models for monitoring
    - Prophet for trend forecasting
    """)

with tech_col2:
    st.markdown("""
    **Infrastructure**
    - Real-time Kafka streams
    - Vector databases (Pinecone)
    - Kubernetes orchestration
    - Multi-region AWS deployment
    """)

with tech_col3:
    st.markdown("""
    **Integrations**
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
<h3>We're raising $2.5M Seed Round</h3>
<p><strong>Traction:</strong> 6 pilot clients, 312% engagement lift proven</p>
<p><strong>Market:</strong> $42B content marketing industry, growing at 16% CAGR</p>
<p><strong>Team:</strong> Ex-Google, Meta AI researchers + serial entrepreneurs</p>
<p><strong>Use of Funds:</strong> 
<ul>
<li>Scale engineering team (8 hires)</li>
<li>Enhanced AI model development</li>
<li>Go-to-market expansion</li>
<li>Platform partnerships</li>
</ul>
</p>
</div>
""", unsafe_allow_html=True)

# Contact
st.markdown("---")
contact_col1, contact_col2 = st.columns(2)
with contact_col1:
    st.markdown("**📧 Contact:** ceo@chronos-ai.com")
with contact_col2:
    st.markdown("**🌐 Website:** [chronos-ai.com](https://chronos-ai.com)")