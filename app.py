import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Life Map Coaching - Personal Journey Explorer", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌱"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    .insight-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌱 Life Map Coaching</h1>
    <h3>Personal Journey Explorer & Reflection Tool</h3>
    <p>Discover patterns, insights, and growth opportunities from your life experiences</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation and settings
with st.sidebar:
    st.header("🎯 Navigation")
    page = st.selectbox("Choose a section:", [
        "📝 Life Events Input",
        "📊 Visual Analytics",
        "🧠 Insights & Coaching",
        "📈 Progress Tracking",
        "💾 Data Management"
    ])
    
    st.markdown("---")
    st.header("⚙️ Settings")
    show_advanced = st.checkbox("Show Advanced Options", value=False)
    auto_save = st.checkbox("Auto-save Progress", value=True)
    
    st.markdown("---")
    st.header("📚 Quick Guide")
    st.info("""
    **How to use:**
    1. Input life events by age
    2. Rate emotional impact
    3. Add reflections
    4. Explore visualizations
    5. Get coaching insights
    """)

# Enhanced age buckets with more detailed life stages
age_buckets = {
    "0-5 (Infancy & Toddler)": list(range(0, 6)),
    "6-12 (Elementary School)": list(range(6, 13)),
    "13-17 (Teenage Years)": list(range(13, 18)),
    "18-22 (College/Early Adult)": list(range(18, 23)),
    "23-29 (Young Professional)": list(range(23, 30)),
    "30-39 (Career Building)": list(range(30, 40)),
    "40-49 (Midlife Growth)": list(range(40, 50)),
    "50-59 (Mature Wisdom)": list(range(50, 60)),
    "60+ (Golden Years)": list(range(60, 101))
}

# Event categories for better classification
event_categories = [
    "🎓 Education & Learning",
    "💼 Career & Work",
    "❤️ Relationships & Family",
    "🏥 Health & Wellness",
    "🎯 Personal Achievement",
    "😢 Loss & Grief",
    "🌍 Travel & Adventure",
    "💰 Financial",
    "🏠 Living Situation",
    "🎨 Creative & Hobbies",
    "⚡ Life-Changing Moment",
    "🤝 Social & Community"
]

# Initialize session state for data persistence
if 'life_events' not in st.session_state:
    st.session_state.life_events = []
if 'current_age' not in st.session_state:
    st.session_state.current_age = 25

# Main content based on selected page
if page == "📝 Life Events Input":
    st.markdown('<div class="section-header"><h2>📝 Life Events Input</h2></div>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", len(st.session_state.life_events))
    with col2:
        good_events = len([e for e in st.session_state.life_events if e.get('sentiment') == 'Positive'])
        st.metric("Positive Events", good_events)
    with col3:
        bad_events = len([e for e in st.session_state.life_events if e.get('sentiment') == 'Negative'])
        st.metric("Challenging Events", bad_events)
    with col4:
        if st.session_state.life_events:
            avg_impact = np.mean([e.get('impact', 5) for e in st.session_state.life_events])
            st.metric("Avg Impact", f"{avg_impact:.1f}/10")
    
    st.markdown("---")
    
    # Enhanced input form
    with st.form("enhanced_life_map_form", clear_on_submit=False):
        st.subheader("🎯 Add a Life Event")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            event_age = st.number_input("Age when this happened", min_value=0, max_value=100, value=st.session_state.current_age)
            event_category = st.selectbox("Event Category", event_categories)
            event_title = st.text_input("Event Title (brief summary)", placeholder="e.g., Started college, Got married, Lost job")
        
        with col2:
            sentiment = st.selectbox("Overall Sentiment", ["Positive", "Negative", "Neutral", "Mixed"])
            impact_score = st.slider("Emotional Impact (1=Low, 10=High)", 1, 10, 5)
            life_area = st.selectbox("Primary Life Area Affected", [
                "Personal Growth", "Relationships", "Career", "Health", 
                "Family", "Education", "Finances", "Spirituality", "Recreation"
            ])
        
        event_description = st.text_area(
            "Detailed Description", 
            placeholder="Describe what happened, how you felt, and why it was significant...",
            height=100
        )
        
        col3, col4 = st.columns([1, 1])
        with col3:
            lessons_learned = st.text_area(
                "Lessons Learned (optional)", 
                placeholder="What did you learn from this experience?",
                height=80
            )
        with col4:
            current_perspective = st.text_area(
                "Current Perspective (optional)", 
                placeholder="How do you view this event now?",
                height=80
            )
        
        if show_advanced:
            st.subheader("🔍 Advanced Details")
            col5, col6 = st.columns([1, 1])
            with col5:
                duration = st.selectbox("Event Duration", ["Moment", "Days", "Weeks", "Months", "Years", "Ongoing"])
                people_involved = st.text_input("Key People Involved", placeholder="Names or relationships")
            with col6:
                location = st.text_input("Location", placeholder="Where did this happen?")
                tags = st.text_input("Tags (comma-separated)", placeholder="graduation, family, milestone")
        
        submitted = st.form_submit_button("💾 Add Event", use_container_width=True)
        
        if submitted and event_title and event_description:
            new_event = {
                "age": event_age,
                "title": event_title,
                "category": event_category,
                "description": event_description,
                "sentiment": sentiment,
                "impact": impact_score,
                "life_area": life_area,
                "lessons_learned": lessons_learned,
                "current_perspective": current_perspective,
                "timestamp": datetime.now().isoformat(),
                "range": next((k for k, v in age_buckets.items() if event_age in v), "Unknown")
            }
            
            if show_advanced:
                new_event.update({
                    "duration": duration,
                    "people_involved": people_involved,
                    "location": location,
                    "tags": tags.split(",") if tags else []
                })
            
            st.session_state.life_events.append(new_event)
            st.session_state.current_age = event_age
            st.success(f"✅ Event '{event_title}' added successfully!")
            st.rerun()
    
    # Display existing events
    if st.session_state.life_events:
        st.markdown("---")
        st.subheader("📋 Your Life Events")
        
        # Create DataFrame for display
        df = pd.DataFrame(st.session_state.life_events)
        
        # Event management
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            sort_by = st.selectbox("Sort by:", ["age", "impact", "timestamp", "sentiment"])
        with col2:
            filter_sentiment = st.selectbox("Filter by sentiment:", ["All", "Positive", "Negative", "Neutral", "Mixed"])
        with col3:
            if st.button("🗑️ Clear All Events"):
                st.session_state.life_events = []
                st.rerun()
        
        # Apply filters
        display_df = df.copy()
        if filter_sentiment != "All":
            display_df = display_df[display_df['sentiment'] == filter_sentiment]
        
        display_df = display_df.sort_values(sort_by, ascending=True if sort_by == "age" else False)
        
        # Display events in an interactive table
        for idx, event in display_df.iterrows():
            with st.expander(f"Age {event['age']}: {event['title']} ({event['sentiment']}) - Impact: {event['impact']}/10"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Category:** {event['category']}")
                    st.write(f"**Description:** {event['description']}")
                    if event.get('lessons_learned'):
                        st.write(f"**Lessons Learned:** {event['lessons_learned']}")
                    if event.get('current_perspective'):
                        st.write(f"**Current Perspective:** {event['current_perspective']}")
                with col2:
                    st.write(f"**Life Area:** {event['life_area']}")
                    st.write(f"**Age Range:** {event['range']}")
                    if st.button(f"🗑️ Delete", key=f"delete_{idx}"):
                        st.session_state.life_events = [e for i, e in enumerate(st.session_state.life_events) if i != idx]
                        st.rerun()

elif page == "📊 Visual Analytics":
    st.markdown('<div class="section-header"><h2>📊 Visual Analytics</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.life_events:
        st.warning("⚠️ No events to visualize. Please add some life events first!")
    else:
        df = pd.DataFrame(st.session_state.life_events)
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Events", len(df))
        with col2:
            avg_impact = df['impact'].mean()
            st.metric("Average Impact", f"{avg_impact:.1f}/10")
        with col3:
            age_span = df['age'].max() - df['age'].min()
            st.metric("Age Span Covered", f"{age_span} years")
        with col4:
            most_common_category = df['category'].mode().iloc[0] if not df.empty else "N/A"
            st.metric("Top Category", most_common_category.split(' ', 1)[1] if ' ' in most_common_category else most_common_category)
        
        st.markdown("---")
        
        # Timeline visualization
        st.subheader("🕒 Life Timeline")
        
        # Create timeline chart
        fig_timeline = px.scatter(df, 
                                x='age', 
                                y='impact',
                                color='sentiment',
                                size='impact',
                                hover_data=['title', 'category', 'life_area'],
                                title="Life Events Timeline",
                                color_discrete_map={
                                    'Positive': '#2E8B57',
                                    'Negative': '#DC143C', 
                                    'Neutral': '#4682B4',
                                    'Mixed': '#DAA520'
                                })
        
        fig_timeline.update_layout(
            xaxis_title="Age",
            yaxis_title="Emotional Impact (1-10)",
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Age range analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Events by Age Range")
            range_counts = df.groupby(['range', 'sentiment']).size().reset_index(name='count')
            
            fig_range = px.bar(range_counts, 
                             x='range', 
                             y='count',
                             color='sentiment',
                             title="Event Distribution by Life Stage",
                             color_discrete_map={
                                 'Positive': '#2E8B57',
                                 'Negative': '#DC143C', 
                                 'Neutral': '#4682B4',
                                 'Mixed': '#DAA520'
                             })
            fig_range.update_xaxes(tickangle=45)
            st.plotly_chart(fig_range, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Life Areas Impact")
            area_impact = df.groupby('life_area')['impact'].mean().sort_values(ascending=True)
            
            fig_areas = px.bar(x=area_impact.values, 
                             y=area_impact.index,
                             orientation='h',
                             title="Average Impact by Life Area",
                             color=area_impact.values,
                             color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_areas, use_container_width=True)
        
        # Category analysis
        st.subheader("📈 Category Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            category_counts = df['category'].value_counts()
            fig_cat = px.pie(values=category_counts.values, 
                           names=category_counts.index,
                           title="Event Categories Distribution")
            st.plotly_chart(fig_cat, use_container_width=True)
        
        with col2:
            # Impact distribution
            fig_impact = px.histogram(df, 
                                    x='impact',
                                    nbins=10,
                                    title="Impact Score Distribution",
                                    color='sentiment')
            st.plotly_chart(fig_impact, use_container_width=True)
        
        # Advanced analytics
        if show_advanced:
            st.markdown("---")
            st.subheader("🔍 Advanced Analytics")
            
            # Correlation analysis
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Age vs Impact Correlation**")
                correlation = df['age'].corr(df['impact'])
                st.metric("Correlation Coefficient", f"{correlation:.3f}")
                
                if correlation > 0.3:
                    st.success("Strong positive correlation: Impact tends to increase with age")
                elif correlation < -0.3:
                    st.warning("Strong negative correlation: Impact tends to decrease with age")
                else:
                    st.info("Weak correlation: No clear age-impact pattern")
            
            with col2:
                st.write("**Sentiment Balance**")
                sentiment_counts = df['sentiment'].value_counts()
                positive_ratio = sentiment_counts.get('Positive', 0) / len(df)
                st.metric("Positive Event Ratio", f"{positive_ratio:.1%}")
                
                if positive_ratio > 0.6:
                    st.success("Predominantly positive life experiences")
                elif positive_ratio < 0.4:
                    st.warning("More challenging experiences recorded")
                else:
                    st.info("Balanced mix of experiences")

elif page == "🧠 Insights & Coaching":
    st.markdown('<div class="section-header"><h2>🧠 Insights & Coaching</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.life_events:
        st.warning("⚠️ No events to analyze. Please add some life events first!")
    else:
        df = pd.DataFrame(st.session_state.life_events)
        
        # Generate insights
        st.subheader("💡 Personal Insights")
        
        # Pattern analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**🔍 Life Patterns Detected:**")
            
            # Most impactful age range
            range_impact = df.groupby('range')['impact'].mean().sort_values(ascending=False)
            top_range = range_impact.index[0]
            st.write(f"• **Most impactful period:** {top_range}")
            
            # Dominant life area
            top_area = df['life_area'].mode().iloc[0]
            area_count = (df['life_area'] == top_area).sum()
            st.write(f"• **Primary focus area:** {top_area} ({area_count} events)")
            
            # Growth trajectory
            if len(df) >= 3:
                recent_events = df.nlargest(3, 'age')
                recent_avg = recent_events['impact'].mean()
                early_events = df.nsmallest(3, 'age')
                early_avg = early_events['impact'].mean()
                
                if recent_avg > early_avg:
                    st.write("• **Growth trajectory:** Increasing impact over time ↗️")
                else:
                    st.write("• **Growth trajectory:** Stabilizing experiences ➡️")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**🎯 Strengths & Opportunities:**")
            
            # Resilience indicator
            negative_events = df[df['sentiment'] == 'Negative']
            if len(negative_events) > 0:
                avg_negative_impact = negative_events['impact'].mean()
                if avg_negative_impact < 7:
                    st.write("• **Resilience:** Good at managing challenges")
                else:
                    st.write("• **Growth area:** Building resilience strategies")
            
            # Positive event frequency
            positive_ratio = (df['sentiment'] == 'Positive').mean()
            if positive_ratio > 0.5:
                st.write("• **Strength:** Recognizing positive experiences")
            else:
                st.write("• **Opportunity:** Focus on positive moments")
            
            # Life balance
            life_areas = df['life_area'].nunique()
            if life_areas >= 5:
                st.write("• **Balance:** Well-rounded life experiences")
            else:
                st.write("• **Opportunity:** Explore diverse life areas")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Coaching recommendations
        st.markdown("---")
        st.subheader("🎯 Personalized Coaching Recommendations")
        
        recommendations = []
        
        # Based on sentiment balance
        positive_ratio = (df['sentiment'] == 'Positive').mean()
        if positive_ratio < 0.4:
            recommendations.append({
                "area": "Mindset & Perspective",
                "recommendation": "Practice gratitude journaling to identify more positive moments in your daily life.",
                "action": "Write down 3 positive things each day for the next week."
            })
        
        # Based on impact patterns
        high_impact_events = df[df['impact'] >= 8]
        if len(high_impact_events) < len(df) * 0.3:
            recommendations.append({
                "area": "Goal Setting",
                "recommendation": "Set more ambitious goals to create meaningful, high-impact experiences.",
                "action": "Identify one area where you want to create a significant positive change."
            })
        
        # Based on life areas
        life_area_counts = df['life_area'].value_counts()
        if life_area_counts.iloc[0] > len(df) * 0.5:
            recommendations.append({
                "area": "Life Balance",
                "recommendation": f"You're heavily focused on {life_area_counts.index[0]}. Consider diversifying your experiences.",
                "action": "Plan one activity in a different life area this month."
            })
        
        # Based on recent events
        if len(df) >= 5:
            recent_events = df.nlargest(5, 'age')
            if (recent_events['sentiment'] == 'Negative').sum() >= 3:
                recommendations.append({
                    "area": "Stress Management",
                    "recommendation": "Recent events show some challenges. Focus on stress management and self-care.",
                    "action": "Implement a daily 10-minute mindfulness or relaxation practice."
                })
        
        # Display recommendations
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"💡 Recommendation {i}: {rec['area']}"):
                st.write(f"**Insight:** {rec['recommendation']}")
                st.write(f"**Action Step:** {rec['action']}")
                if st.button(f"Mark as Planned", key=f"rec_{i}"):
                    st.success("Great! Remember to follow through on this action.")
        
        # Reflection prompts
        st.markdown("---")
        st.subheader("🤔 Reflection Prompts")
        
        prompts = [
            "What patterns do you notice in your most impactful experiences?",
            "How have your responses to challenges evolved over time?",
            "What life areas deserve more attention in the coming year?",
            "Which experiences taught you the most about yourself?",
            "How can you create more positive, meaningful moments?"
        ]
        
        selected_prompt = st.selectbox("Choose a reflection prompt:", prompts)
        reflection_text = st.text_area("Your reflection:", height=150, placeholder="Take a moment to reflect on this question...")
        
        if st.button("💾 Save Reflection") and reflection_text:
            # Add reflection as a special event
            reflection_event = {
                "age": st.session_state.current_age,
                "title": "Personal Reflection",
                "category": "🧠 Personal Growth",
                "description": f"Prompt: {selected_prompt}\n\nReflection: {reflection_text}",
                "sentiment": "Neutral",
                "impact": 5,
                "life_area": "Personal Growth",
                "lessons_learned": "",
                "current_perspective": "",
                "timestamp": datetime.now().isoformat(),
                "range": next((k for k, v in age_buckets.items() if st.session_state.current_age in v), "Unknown")
            }
            st.session_state.life_events.append(reflection_event)
            st.success("✅ Reflection saved as a life event!")

elif page == "📈 Progress Tracking":
    st.markdown('<div class="section-header"><h2>📈 Progress Tracking</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.life_events:
        st.warning("⚠️ No events to track. Please add some life events first!")
    else:
        df = pd.DataFrame(st.session_state.life_events)
        
        # Progress metrics
        st.subheader("📊 Your Journey Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_events = len(df)
            st.metric("Total Events Recorded", total_events)
        
        with col2:
            if total_events > 0:
                completion_score = min(100, (total_events / 20) * 100)  # Assume 20 events is "complete"
                st.metric("Journey Completion", f"{completion_score:.0f}%")
        
        with col3:
            reflection_events = len([e for e in st.session_state.life_events if "reflection" in e.get('title', '').lower()])
            st.metric("Reflections Added", reflection_events)
        
        with col4:
            if len(df) >= 2:
                df_sorted = df.sort_values('timestamp')
                days_active = (pd.to_datetime(df_sorted.iloc[-1]['timestamp']) - pd.to_datetime(df_sorted.iloc[0]['timestamp'])).days + 1
                st.metric("Days Active", days_active)
        
        # Growth tracking
        st.markdown("---")
        st.subheader("🌱 Personal Growth Tracking")
        
        if len(df) >= 3:
            # Create growth timeline
            df_sorted = df.sort_values('age')
            
            # Calculate moving average of impact
            window_size = min(3, len(df_sorted))
            df_sorted['impact_ma'] = df_sorted['impact'].rolling(window=window_size, center=True).mean()
            
            fig_growth = go.Figure()
            
            # Add individual events
            fig_growth.add_trace(go.Scatter(
                x=df_sorted['age'],
                y=df_sorted['impact'],
                mode='markers',
                name='Individual Events',
                marker=dict(size=8, opacity=0.6),
                text=df_sorted['title'],
                hovertemplate='<b>%{text}</b><br>Age: %{x}<br>Impact: %{y}<extra></extra>'
            ))
            
            # Add trend line
            fig_growth.add_trace(go.Scatter(
                x=df_sorted['age'],
                y=df_sorted['impact_ma'],
                mode='lines',
                name='Growth Trend',
                line=dict(width=3, color='red')
            ))
            
            fig_growth.update_layout(
                title="Personal Growth Trajectory",
                xaxis_title="Age",
                yaxis_title="Impact Score",
                height=400
            )
            
            st.plotly_chart(fig_growth, use_container_width=True)
            
            # Growth insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Growth Analysis:**")
                recent_trend = df_sorted['impact_ma'].iloc[-3:].mean() if len(df_sorted) >= 3 else df_sorted['impact'].mean()
                early_trend = df_sorted['impact_ma'].iloc[:3].mean() if len(df_sorted) >= 3 else df_sorted['impact'].mean()
                
                if recent_trend > early_trend + 0.5:
                    st.success("📈 Positive growth trajectory detected!")
                elif recent_trend < early_trend - 0.5:
                    st.warning("📉 Consider focusing on positive experiences")
                else:
                    st.info("➡️ Stable experience pattern")
            
            with col2:
                st.write("**Milestone Achievements:**")
                milestones = []
                
                if total_events >= 5:
                    milestones.append("✅ Documented 5+ life events")
                if total_events >= 10:
                    milestones.append("✅ Reached 10+ life events")
                if reflection_events >= 1:
                    milestones.append("✅ Added personal reflections")
                if df['life_area'].nunique() >= 5:
                    milestones.append("✅ Explored 5+ life areas")
                
                for milestone in milestones:
                    st.write(milestone)
        
        # Goal setting
        st.markdown("---")
        st.subheader("🎯 Set Your Goals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Suggested Goals:**")
            goals = []
            
            if total_events < 10:
                goals.append(f"Document {10 - total_events} more life events")
            if reflection_events < 3:
                goals.append(f"Add {3 - reflection_events} more reflections")
            if df['life_area'].nunique() < 6:
                goals.append("Explore more diverse life areas")
            
            for goal in goals:
                st.write(f"• {goal}")
        
        with col2:
            st.write("**Custom Goal:**")
            custom_goal = st.text_input("Set a personal goal:")
            if st.button("Add Goal") and custom_goal:
                st.success(f"Goal added: {custom_goal}")

elif page == "💾 Data Management":
    st.markdown('<div class="section-header"><h2>💾 Data Management</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Export Data")
        
        if st.session_state.life_events:
            # Export as JSON
            if st.button("📄 Export as JSON"):
                json_data = json.dumps(st.session_state.life_events, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"life_map_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            
            # Export as CSV
            if st.button("📊 Export as CSV"):
                df = pd.DataFrame(st.session_state.life_events)
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"life_map_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            # Summary report
            if st.button("📋 Generate Summary Report"):
                df = pd.DataFrame(st.session_state.life_events)
                
                report = f"""
# Life Map Summary Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Overview
- Total Events: {len(df)}
- Age Range: {df['age'].min()} - {df['age'].max()} years
- Average Impact: {df['impact'].mean():.1f}/10

## Sentiment Distribution
{df['sentiment'].value_counts().to_string()}

## Top Life Areas
{df['life_area'].value_counts().head().to_string()}

## Most Impactful Events
{df.nlargest(5, 'impact')[['age', 'title', 'impact']].to_string(index=False)}
                """
                
                st.download_button(
                    label="Download Report",
                    data=report,
                    file_name=f"life_map_report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
        else:
            st.info("No data to export. Add some life events first!")
    
    with col2:
        st.subheader("📥 Import Data")
        
        uploaded_file = st.file_uploader("Upload JSON file", type=['json'])
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                if st.button("Import Data"):
                    st.session_state.life_events.extend(imported_data)
                    st.success(f"✅ Imported {len(imported_data)} events!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error importing file: {e}")
        
        st.markdown("---")
        st.subheader("🗑️ Data Management")
        
        if st.button("🔄 Reset All Data", type="secondary"):
            if st.checkbox("I understand this will delete all my data"):
                st.session_state.life_events = []
                st.success("All data cleared!")
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🌱 <strong>Life Map Coaching</strong> - Your Personal Journey Explorer</p>
    <p>Remember: Every experience, positive or challenging, contributes to your unique story and growth.</p>
</div>
""", unsafe_allow_html=True)

