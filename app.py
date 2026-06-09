import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pickle
from groq import Groq
from dotenv import load_dotenv
import os

#page config
st.set_page_config(
    page_title="AspectIQ",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

#load data
@st.cache_data
def load_data():
    with open('dashboard_data.pkl','rb') as f:
        return pickle.load(f)
data=load_data()
sample_df=data['sample_df']
sentiment_counts=data['sentiment_counts']
aspect_descriptions=data['aspect_descriptions']

#Load Groq
load_dotenv()
groq_client=Groq(api_key=os.getenv('GROQ_API_KEY'))

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0F1117; }
    .stApp { background-color: #0F1117; }
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e, #252b3b);
        border: 1px solid #2d3555;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4F8EF7;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8892a4;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .insight-card {
        background: linear-gradient(135deg, #1a1f2e, #252b3b);
        border-left: 4px solid #4F8EF7;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/fluency/96/search.png", width=60)
st.sidebar.title("AspectIQ")
st.sidebar.markdown("*Product Review Intelligence*")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Aspect Intelligence", "Business Impact"]
)

if page == "Overview":
    
    # Header
    st.markdown("<h1 style='color:#4F8EF7; font-size:2.8rem;'>AspectIQ 🔍</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892a4; font-size:1.1rem;'>Product Review Intelligence System</p>", unsafe_allow_html=True)
    st.divider()
    
    # Metric cards
    total_reviews = len(sample_df)
    total_aspects = sum(len(a) for a in sample_df['embed_aspects'])
    total_negative = sum(
        1 for sentiments in sample_df['aspect_sentiment']
        for s in sentiments.values() if s == 'negative'
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_reviews:,}</div>
            <div class="metric-label">Reviews Analyzed</div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_aspects:,}</div>
            <div class="metric-label">Aspects Detected</div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_negative:,}</div>
            <div class="metric-label">Issues Flagged</div>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        aspects_list = ['packaging', 'delivery', 'taste', 'price']
        most_complained = max(aspects_list, 
                    key=lambda a: sentiment_counts.get(a, {}).get('negative', 0) / 
                    max(sum(sentiment_counts.get(a, {}).values()), 1))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">📦</div>
            <div class="metric-label">Top Issue: {most_complained.upper()}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color:#ffffff;'>Aspect Distribution</h3>", unsafe_allow_html=True)
        aspect_counts = {a: sentiment_counts.get(a, {}).get('positive', 0) + 
                        sentiment_counts.get(a, {}).get('negative', 0) + 
                        sentiment_counts.get(a, {}).get('neutral', 0) 
                        for a in ['taste', 'packaging', 'price', 'delivery']}
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=list(aspect_counts.keys()),
            values=list(aspect_counts.values()),
            hole=0.6,
            marker_colors=['#4F8EF7', '#00C896', '#FFB547', '#FF5757']
        )])
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True,
            legend=dict(font=dict(color='white'))
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color:#ffffff;'>Sentiment Breakdown by Aspect</h3>", unsafe_allow_html=True)
        aspects = ['taste', 'packaging', 'price', 'delivery']
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Positive', x=aspects, 
                                  y=[sentiment_counts[a]['positive'] for a in aspects],
                                  marker_color='#00C896'))
        fig_bar.add_trace(go.Bar(name='Negative', x=aspects,
                                  y=[sentiment_counts[a]['negative'] for a in aspects],
                                  marker_color='#FF5757'))
        fig_bar.add_trace(go.Bar(name='Neutral', x=aspects,
                                  y=[sentiment_counts[a]['neutral'] for a in aspects],
                                  marker_color='#4F8EF7'))
        fig_bar.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(gridcolor='#2d3555'),
            yaxis=dict(gridcolor='#2d3555')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
elif page == "Aspect Intelligence":
    
    st.markdown("<h1 style='color:#4F8EF7;'>Aspect Intelligence 🔍</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892a4;'>Deep dive into what customers say about each aspect</p>", unsafe_allow_html=True)
    st.divider()
    
    # Aspect selector
    selected_aspect = st.selectbox(
        "Select an aspect to analyze:",
        ['taste', 'packaging', 'price', 'delivery'],
        format_func=lambda x: {
            'taste': 'Taste',
            'packaging': 'Packaging', 
            'price': 'Price',
            'delivery': 'Delivery'
        }[x]
    )
    # Sentiment counts for selected aspect
    counts = sentiment_counts.get(selected_aspect, {})
    positive = counts.get('positive', 0)
    negative = counts.get('negative', 0)
    neutral = counts.get('neutral', 0)
    total = positive + negative + neutral
    
    health_score = int((positive / total) * 100) if total > 0 else 0
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # Sentiment health gauge
        st.markdown("<h3 style='color:#ffffff;'>Sentiment Health Score</h3>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': selected_aspect.upper(), 'font': {'color': 'white'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': 'white'},
                'bar': {'color': '#4F8EF7'},
                'steps': [
                    {'range': [0, 40], 'color': '#FF5757'},
                    {'range': [40, 70], 'color': '#FFB547'},
                    {'range': [70, 100], 'color': '#00C896'}
                ],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.75,
                    'value': health_score
                }
            },
            number={'font': {'color': 'white'}}
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Sentiment breakdown
        st.markdown("<h3 style='color:#ffffff;'>Sentiment Breakdown</h3>", unsafe_allow_html=True)
        fig_sentiment = go.Figure(go.Bar(
            x=['Positive', 'Negative', 'Neutral'],
            y=[positive, negative, neutral],
            marker_color=['#00C896', '#FF5757', '#4F8EF7'],
            text=[positive, negative, neutral],
            textposition='auto',
            textfont=dict(color='white')
        ))
        fig_sentiment.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(gridcolor='#2d3555'),
            yaxis=dict(gridcolor='#2d3555'),
            height=300
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
        st.divider()
    st.markdown("<h3 style='color:#ffffff;'>🤖 AI-Powered Complaint Analysis</h3>", unsafe_allow_html=True)
    
    if st.button(f"Analyze {selected_aspect.upper()} complaints with AI"):
        with st.spinner(f"Analyzing {selected_aspect} complaints..."):
            # Get negative reviews for selected aspect
            negative_reviews = []
            for _, row in sample_df.iterrows():
                if selected_aspect in row['embed_aspects']:
                    if row['aspect_sentiment'].get(selected_aspect) == 'negative':
                        negative_reviews.append(row['Text'])
            
            if negative_reviews:
                reviews_sample = negative_reviews[:20]
                combined = "\n\n".join(reviews_sample)
                
                prompt = f"""You are a product analyst. Below are negative customer reviews about {selected_aspect}.
Summarize the TOP 3 specific complaints in 3 bullet points. Be specific and actionable.
Reviews:
{combined}"""
                
                response = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant",
                )
                
                summary = response.choices[0].message.content
                st.markdown(f"""
                <div class="insight-card">
                    <h4 style='color:#4F8EF7;'>Top Complaints: {selected_aspect.upper()}</h4>
                    <p style='color:#e0e0e0;'>{summary}</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.success(f"No significant negative reviews found for {selected_aspect}! 🎉")
elif page == "Business Impact":
    
    st.markdown("<h1 style='color:#4F8EF7;'>Business Impact Calculator 💰</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8892a4;'>Estimate the revenue impact of fixing customer complaints</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<h3 style='color:#ffffff;'>What if you fixed your top complaints?</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        aspect_choice = st.selectbox(
            "Choose aspect to improve:",
            ['packaging', 'delivery', 'taste', 'price'],
            format_func=lambda x: {
                'taste': 'Taste',
                'packaging': 'Packaging',
                'price': 'Price',
                'delivery': 'Delivery'
            }[x]
        )
        
        fix_percentage = st.slider(
            "% of negative reviews you could fix:",
            min_value=10, max_value=100, value=50, step=10
        )
        
        monthly_revenue = st.number_input(
            "Your monthly revenue (USD):",
            min_value=1000, max_value=10000000,
            value=100000, step=10000
        )
    
    with col2:
        counts = sentiment_counts.get(aspect_choice, {})
        negative = counts.get('negative', 0)
        total = sum(counts.values())
        
        current_negative_rate = (negative / total * 100) if total > 0 else 0
        fixed_reviews = int(negative * fix_percentage / 100)
        new_negative = negative - fixed_reviews
        new_negative_rate = ((new_negative / total) * 100) if total > 0 else 0
        
        # Rating improvement estimate
        # Research shows fixing complaints improves rating by ~0.1 per 5% reduction in complaints
        complaint_reduction = current_negative_rate - new_negative_rate
        rating_improvement = round(complaint_reduction * 0.02, 2)
        
        # Revenue impact: each 0.1 star improvement = ~2.5% revenue increase
        revenue_impact = monthly_revenue * (rating_improvement / 0.1) * 0.025
        
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:15px;">
            <div class="metric-number" style="color:#FF5757;">{current_negative_rate:.1f}%</div>
            <div class="metric-label">Current Complaint Rate</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:15px;">
            <div class="metric-number" style="color:#00C896;">{new_negative_rate:.1f}%</div>
            <div class="metric-label">Projected Complaint Rate</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number" style="color:#FFB547;">+${revenue_impact:,.0f}</div>
            <div class="metric-label">Estimated Monthly Revenue Impact</div>
        </div>""", unsafe_allow_html=True)    
