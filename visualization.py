import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_timeline(data):
    """Create timeline visualization of mentions and sentiment"""
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    # Add mentions line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['mentions'],
        name='Mentions',
        line=dict(color='#667eea', width=3),
        yaxis='y1'
    ))
    
    # Add sentiment area
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['sentiment'],
        name='Sentiment',
        fill='tozeroy',
        line=dict(color='rgba(102, 126, 234, 0.3)', width=1),
        yaxis='y2'
    ))
    
    # Add event markers
    event_times = [df['timestamp'][i] for i in range(len(df)) if df['events'][i] > 0]
    if event_times:
        fig.add_trace(go.Scatter(
            x=event_times,
            y=[max(df['mentions']) * 0.9] * len(event_times),
            mode='markers',
            name='Key Events',
            marker=dict(color='red', size=10, symbol='diamond'),
            yaxis='y1'
        ))
    
    fig.update_layout(
        title='Real-time Trend Monitoring',
        xaxis_title='Time',
        yaxis=dict(title='Mentions', side='left'),
        yaxis2=dict(title='Sentiment', side='right', overlaying='y', range=[0, 1]),
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_sentiment_gauge(value):
    """Create a sentiment gauge visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value * 100,
        title={'text': "Overall Sentiment"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 33], 'color': "lightgray"},
                {'range': [33, 66], 'color': "gray"},
                {'range': [66, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_topic_network(topics):
    """Create network visualization of related topics"""
    nodes = []
    edges = []
    
    for i, topic in enumerate(topics[:8]):
        nodes.append({
            'id': i,
            'label': topic,
            'size': random.randint(10, 30),
            'color': f'hsl({i*40}, 70%, 50%)'
        })
        
        # Create connections
        for j in range(i+1, min(i+3, len(topics[:8]))):
            if random.random() > 0.5:
                edges.append((i, j, random.uniform(0.3, 1)))
    
    # This would normally use networkx + plotly
    # Simplified for demo
    return None