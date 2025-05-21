import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
import json

# Mock functions to simulate API calls - replace these with actual API imports in production
def fetch_codeforces_profile_api(handle):
    if not handle or handle.lower() == 'invalid':
        return None
    
    # Simulate API call delay
    time.sleep(0.5)
    
    # Mock data for demonstration
    ratings = {
        'tourist': 3800,
        'Petr': 3500,
        'subscriber': 2200,
        'coder': 1800,
        'newbie': 1200
    }
    
    rating = ratings.get(handle.lower(), random.randint(800, 2400))
    
    return {
        "handle": handle,
        "rating": rating,
        "rank": get_cf_rank(rating),
        "maxRating": rating + random.randint(0, 200),
        "contribution": random.randint(-100, 1000),
        "friendOfCount": random.randint(0, 100),
        "lastOnlineTimeSeconds": int(time.time()) - random.randint(0, 86400),
        "registrationTimeSeconds": int(time.time()) - random.randint(86400 * 100, 86400 * 1000)
    }

def fetch_leetcode_profile(handle):
    if not handle or handle.lower() == 'invalid':
        return None
    
    # Simulate API call delay
    time.sleep(0.5)
    
    return {
        "username": handle,
        "ranking": random.randint(1, 100000),
        "rating": random.randint(1500, 2200),
        "problems_solved": {
            "easy": random.randint(10, 100),
            "medium": random.randint(5, 80),
            "hard": random.randint(0, 40)
        }
    }

def fetch_codechef_profile(handle):
    if not handle or handle.lower() == 'invalid':
        return None
    
    # Simulate API call delay
    time.sleep(0.5)
    
    return {
        "username": handle,
        "rating": random.randint(1000, 2000),
        "rank": random.randint(1, 50000),
        "country_rank": random.randint(1, 5000),
        "problems_solved": random.randint(10, 200)
    }

# Helper functions for display
def get_cf_rank(rating):
    if rating < 1200:
        return "Newbie"
    elif rating < 1400:
        return "Pupil"
    elif rating < 1600:
        return "Specialist"
    elif rating < 1900:
        return "Expert"
    elif rating < 2100:
        return "Candidate Master"
    elif rating < 2300:
        return "Master"
    elif rating < 2400:
        return "International Master"
    elif rating < 2600:
        return "Grandmaster"
    elif rating < 3000:
        return "International Grandmaster"
    else:
        return "Legendary Grandmaster"

def get_cf_rank_color(rank):
    color_map = {
        "Newbie": "#808080",
        "Pupil": "#008000",
        "Specialist": "#03A89E",
        "Expert": "#0000FF",
        "Candidate Master": "#AA00AA",
        "Master": "#FF8C00",
        "International Master": "#FF8C00",
        "Grandmaster": "#FF0000",
        "International Grandmaster": "#FF0000",
        "Legendary Grandmaster": "#FF0000"
    }
    return color_map.get(rank, "#000000")

def get_lc_level(problems):
    total = sum(problems.values())
    if total < 50:
        return "Beginner"
    elif total < 150:
        return "Intermediate"
    elif total < 300:
        return "Advanced"
    else:
        return "Expert"

def get_cc_rank(rating):
    if rating < 1400:
        return "1★"
    elif rating < 1600:
        return "2★"
    elif rating < 1800:
        return "3★"
    elif rating < 2000:
        return "4★"
    elif rating < 2200:
        return "5★"
    elif rating < 2500:
        return "6★"
    else:
        return "7★"

# Unified Ranking System Class (Simplified version for Streamlit)
class UnifiedRankingSystem:
    def __init__(self):
        self.platforms = {}
        self.users = {}
        self.final_weights = {}
        
    def add_platform(self, name, max_rating):
        self.platforms[name] = {
            "max_rating": max_rating,
            "difficulty": 0,
            "participation": 0
        }
        
    def add_user(self, user_id):
        self.users[user_id] = {
            "platform_ratings": {},
            "unified_rating": 0,
            "course_bonus": 0,
            "total_rating": 0
        }
        
    def update_platform_stats(self, platform, difficulty, participation, current_ratings):
        self.platforms[platform]["difficulty"] = difficulty
        self.platforms[platform]["participation"] = participation
        
        for user_id, rating in current_ratings.items():
            if user_id in self.users:
                self.users[user_id]["platform_ratings"][platform] = rating
                
        self._update_weights()
        self._calculate_unified_ratings()
        
    def _update_weights(self):
        total_difficulty = sum(platform["difficulty"] for platform in self.platforms.values())
        total_participation = sum(platform["participation"] for platform in self.platforms.values())
        
        for platform, data in self.platforms.items():
            normalized_difficulty = data["difficulty"] / total_difficulty if total_difficulty else 0
            normalized_participation = data["participation"] / total_participation if total_participation else 0
            
            # Simple weighting formula
            self.final_weights[platform] = (normalized_difficulty * 0.6) + (normalized_participation * 0.4)
            
    def _normalize_rating(self, rating, platform):
        max_rating = self.platforms[platform]["max_rating"]
        return (rating / max_rating) * 3000  # Normalize to 3000 scale
        
    def _calculate_unified_ratings(self):
        for user_id, user_data in self.users.items():
            weighted_sum = 0
            weight_sum = 0
            
            for platform, rating in user_data["platform_ratings"].items():
                normalized_rating = self._normalize_rating(rating, platform)
                weight = self.final_weights.get(platform, 0)
                
                weighted_sum += normalized_rating * weight
                weight_sum += weight
                
            # Calculate unified rating
            if weight_sum > 0:
                unified_rating = weighted_sum / weight_sum
            else:
                unified_rating = 0
                
            self.users[user_id]["unified_rating"] = unified_rating
            self.users[user_id]["total_rating"] = unified_rating + self.users[user_id]["course_bonus"]
            
    def _impute_missing_rating(self, user_id, platform):
        user_data = self.users[user_id]
        if not user_data["platform_ratings"]:
            # No ratings yet, start with a default value
            return self.platforms[platform]["max_rating"] * 0.4
            
        # Calculate average normalized rating from other platforms
        normalized_ratings = []
        for p, r in user_data["platform_ratings"].items():
            normalized_ratings.append(self._normalize_rating(r, p))
            
        if normalized_ratings:
            avg_normalized = sum(normalized_ratings) / len(normalized_ratings)
            # Convert back to platform's scale
            return (avg_normalized / 3000) * self.platforms[platform]["max_rating"]
        else:
            return self.platforms[platform]["max_rating"] * 0.4
            
    def get_rankings(self):
        rankings = []
        for user_id, data in self.users.items():
            rankings.append((
                user_id,
                data["unified_rating"],
                data["course_bonus"],
                data["total_rating"]
            ))
        return sorted(rankings, key=lambda x: x[3], reverse=True)

# Function to generate mock activity heatmap data
# Improved heatmap generation function
def draw_heatmap(data):
    # Generate full date range for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=364)  # Exactly 52 weeks
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create dataframe with all dates
    df = pd.DataFrame({'date': date_range})
    
    # Convert input data to dataframe
    data_df = pd.DataFrame(list(data.items()), columns=['date', 'value'])
    data_df['date'] = pd.to_datetime(data_df['date'])
    
    # Merge with full date range
    merged_df = df.merge(data_df, on='date', how='left').fillna({'value': 0})
    
    # Add week number, year and day numbers
    # Using custom week numbering to avoid duplicate indices
    merged_df['year'] = merged_df['date'].dt.isocalendar().year
    merged_df['week'] = merged_df['date'].dt.isocalendar().week
    merged_df['day'] = merged_df['date'].dt.isocalendar().day
    
    # Create a unique week identifier that combines year and week
    merged_df['week_unique'] = (merged_df['date'] - merged_df['date'].min()).dt.days // 7
    
    # Create pivot tables - using the unique week identifier to avoid duplicates
    pivot_value = merged_df.pivot(index='day', columns='week_unique', values='value')
    pivot_date = merged_df.pivot(index='day', columns='week_unique', values='date')
    
    # Generate hover text matrix
    hover_text = []
    max_day = 7  # Monday-Sunday
    max_week = pivot_value.shape[1]
    
    for day in range(1, max_day+1):
        week_text = []
        for week in range(max_week):           
            try:
                date = pivot_date.at[day, week]
                count = pivot_value.at[day, week]
                # Check if the date is a valid datetime (not NaT)
                if pd.notnull(date):
                    date_str = date.strftime("%b %d, %Y")
                    week_text.append(f"{date_str}<br>{count} submission(s)")
                else:
                    week_text.append("No data")
            except KeyError:
                week_text.append("")
        hover_text.append(week_text)
    
    # Create heatmap trace
    heatmap = go.Heatmap(
        z=pivot_value.values,
        x=list(range(max_week)),
        y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        hoverinfo="text",
        text=hover_text,
        colorscale=[
            [0.0, '#ebedf0'],    # 0 submissions
            [0.1, '#9be9a8'],    # 1-2 submissions
            [0.3, '#40c463'],    # 3-4 submissions
            [0.5, '#30a14e'],    # 5-6 submissions
            [1.0, '#216e39']     # 7+ submissions
        ],
        showscale=False,
        zmin=0,
        zmax=10
    )
    
    # Create figure
    fig = go.Figure(data=heatmap)
    
    # Add month separators
    month_lines = []
    month_labels = []
    current_month = None   
    for week in range(max_week):
        week_dates = pivot_date.iloc[:, week]
        date = week_dates.dropna().iloc[0] if not week_dates.dropna().empty else None
        if date and pd.notnull(date):
            month = date.month
            if month != current_month:
                if current_month is not None:
                    month_lines.append(week - 0.5)
                    month_labels.append((week - 0.5, date.strftime('%b')))
                current_month = month
    
    # Add vertical lines for month separators
    for line in month_lines:
        fig.add_vline(
            x=line,
            line_width=1,
            line_color="white",
            opacity=0.5
        )
    
    # Add month labels
    for position, label in month_labels:
        fig.add_annotation(
            x=position,
            y=7.5,
            text=label,
            showarrow=False,
            font=dict(color="gray", size=10),
            xref="x",
            yref="y"
        )
    
    # Update layout
    fig.update_layout(
        title="Coding Activity Heatmap",
        height=300,
        margin=dict(t=40, b=20, l=40, r=20),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 8)),
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            autorange='reversed'
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        plot_bgcolor='white'
    )
    
    return fig

# Helper function to combine heatmaps from multiple platforms
def combine_heatmaps(*heatmaps):
    combined = {}
    for heatmap in heatmaps:
        for date, value in heatmap.items():
            combined[date] = combined.get(date, 0) + value
    return combined

# Helper function to generate mock heatmap data
def generate_heatmap_data(activity_level=0.3):
    # activity_level: float between 0 and 1, higher means more active
    today = datetime.now().date()
    data = {}
    for i in range(365):
        date = today - timedelta(days=i)
        # Simulate activity: more likely to have submissions if activity_level is high
        if random.random() < activity_level:
            data[date.strftime("%Y-%m-%d")] = random.randint(1, 5)
    return data

# Modified Activity Heatmap tab section
# (This section is now handled in the main() function with the correct tab3 definition)


def calculate_course_bonus(course_data):
    if not course_data:
        return 0, {}
    
    # Initialize bonus components
    institution_bonus = 0
    duration_bonus = 0
    field_bonus = 0
    skills_bonus = 0
    
    # Institution tier bonus (max 15 points)
    tier_mapping = {
        "Tier 1": 15,
        "Tier 2": 10,
        "Tier 3": 5,
        "Other": 2
    }
    institution_bonus = tier_mapping.get(course_data.get("institution_tier", "Other"), 0)
    
    # Duration bonus (max 10 points)
    duration = course_data.get("duration", 0)
    if duration >= 12:  # 12+ months
        duration_bonus = 10
    elif duration >= 6:  # 6+ months
        duration_bonus = 6
    elif duration >= 3:  # 3+ months
        duration_bonus = 3
    else:
        duration_bonus = 1
    
    # Field relevance bonus (max 10 points)
    field = course_data.get("field", "").lower()
    if field in ["computer science", "algorithms", "data structures"]:
        field_bonus = 10
    elif field in ["programming", "software engineering", "machine learning"]:
        field_bonus = 8
    elif field in ["mathematics", "statistics", "data science"]:
        field_bonus = 6
    else:
        field_bonus = 2
    
    # Skills bonus (max 10 points)
    skills = course_data.get("skills", [])
    skill_count = len(skills)
    if skill_count >= 5:
        skills_bonus = 10
    elif skill_count >= 3:
        skills_bonus = 6
    elif skill_count >= 1:
        skills_bonus = 3
    
    # Total bonus (max 45 points)
    total_bonus = institution_bonus + duration_bonus + field_bonus + skills_bonus
    
    # Bonus breakdown
    bonus_breakdown = {
        "institution": institution_bonus,
        "duration": duration_bonus,
        "field": field_bonus,
        "skills": skills_bonus
    }
    
    return total_bonus, bonus_breakdown

# Streamlit app
def main():
    st.set_page_config(
        page_title="CP Rating Dashboard",
        page_icon="🏆",
        layout="wide"
    )
    
    st.title("Competitive Programming Unified Rating Dashboard")
    
    # Initialize session state for storing data
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
    if 'ranking_system' not in st.session_state:
        st.session_state.ranking_system = UnifiedRankingSystem()
        # Add platforms
        st.session_state.ranking_system.add_platform("Codeforces", max_rating=3000)
        st.session_state.ranking_system.add_platform("Leetcode", max_rating=2500)
        st.session_state.ranking_system.add_platform("Atcoder", max_rating=2800)
        st.session_state.ranking_system.add_platform("CodeChef", max_rating=1800)
    if 'cf_profile' not in st.session_state:
        st.session_state.cf_profile = None
    if 'lc_profile' not in st.session_state:
        st.session_state.lc_profile = None
    if 'cc_profile' not in st.session_state:
        st.session_state.cc_profile = None
    if 'course_data' not in st.session_state:
        st.session_state.course_data = None
    if 'total_bonus' not in st.session_state:
        st.session_state.total_bonus = 0
    if 'bonus_breakdown' not in st.session_state:
        st.session_state.bonus_breakdown = {}
    if 'heatmap_data' not in st.session_state:
        st.session_state.heatmap_data = {}
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Profile Setup", "Rating Analysis", "Activity Heatmap", "Course Bonus"])
    
    with tab1:
        st.header("Connect Your Competitive Programming Profiles")
        
        # Codeforces
        cf_col1, cf_col2 = st.columns([3, 1])
        with cf_col1:
            cf_handle = st.text_input("Codeforces Handle", value=st.session_state.user_id if st.session_state.user_id else "")
        with cf_col2:
            if st.button("Fetch CF Profile", use_container_width=True):
                with st.spinner("Fetching Codeforces profile..."):
                    cf_profile = fetch_codeforces_profile_api(cf_handle)
                    if cf_profile:
                        st.session_state.cf_profile = cf_profile
                        st.session_state.user_id = cf_handle  # Use as main user ID
                        
                        # Initialize user in the ranking system
                        if cf_handle not in st.session_state.ranking_system.users:
                            st.session_state.ranking_system.add_user(cf_handle)
                            
                        # Update Codeforces stats
                        st.session_state.ranking_system.update_platform_stats(
                            "Codeforces",
                            difficulty=2100,
                            participation=0.8,
                            current_ratings={cf_handle: cf_profile["rating"]}
                        )
                        
                        # Generate heatmap data
                        cf_heatmap = generate_heatmap_data(0.4)
                        st.session_state.heatmap_data["cf"] = cf_heatmap
                        
                        st.success(f"Successfully fetched Codeforces profile for {cf_handle}")
                    else:
                        st.error("Failed to fetch Codeforces profile. Please check the handle.")
        
        # Display Codeforces profile if available
        if st.session_state.cf_profile:
            cf_rating = st.session_state.cf_profile["rating"]
            cf_rank = st.session_state.cf_profile["rank"]
            cf_color = get_cf_rank_color(cf_rank)
            
            st.markdown(f"""
            ### Codeforces Profile
            - **Handle:** {st.session_state.cf_profile["handle"]}
            - **Rating:** {cf_rating}
            - **Rank:** <span style='color:{cf_color}'>{cf_rank}</span>
            - **Max Rating:** {st.session_state.cf_profile["maxRating"]}
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Leetcode
        lc_col1, lc_col2 = st.columns([3, 1])
        with lc_col1:
            lc_handle = st.text_input("Leetcode Username")
        with lc_col2:
            if st.button("Fetch LC Profile", use_container_width=True):
                with st.spinner("Fetching Leetcode profile..."):
                    lc_profile = fetch_leetcode_profile(lc_handle)
                    if lc_profile:
                        st.session_state.lc_profile = lc_profile
                        
                        # Use main user ID from Codeforces
                        if st.session_state.user_id:
                            # Update Leetcode stats
                            st.session_state.ranking_system.update_platform_stats(
                                "Leetcode",
                                difficulty=2100,
                                participation=0.8,
                                current_ratings={st.session_state.user_id: lc_profile["rating"]}
                            )
                            
                            # Generate heatmap data
                            lc_heatmap = generate_heatmap_data(0.3)
                            st.session_state.heatmap_data["lc"] = lc_heatmap
                            
                            st.success(f"Successfully fetched Leetcode profile for {lc_handle}")
                        else:
                            st.warning("Please fetch Codeforces profile first to establish user ID")
                    else:
                        st.error("Failed to fetch Leetcode profile. Please check the username.")
        
        # Display Leetcode profile if available
        if st.session_state.lc_profile:
            st.markdown(f"""
            ### Leetcode Profile
            - **Username:** {st.session_state.lc_profile["username"]}
            - **Rating:** {st.session_state.lc_profile["rating"]}
            - **Ranking:** {st.session_state.lc_profile["ranking"]}
            - **Problems Solved:** 
                - Easy: {st.session_state.lc_profile["problems_solved"]["easy"]}
                - Medium: {st.session_state.lc_profile["problems_solved"]["medium"]}
                - Hard: {st.session_state.lc_profile["problems_solved"]["hard"]}
            """)
        
        st.divider()
        
        # CodeChef
        cc_col1, cc_col2 = st.columns([3, 1])
        with cc_col1:
            cc_handle = st.text_input("CodeChef Username")
        with cc_col2:
            if st.button("Fetch CC Profile", use_container_width=True):
                with st.spinner("Fetching CodeChef profile..."):
                    cc_profile = fetch_codechef_profile(cc_handle)
                    if cc_profile:
                        st.session_state.cc_profile = cc_profile
                        
                        # Use main user ID from Codeforces
                        if st.session_state.user_id:
                            # Update CodeChef stats
                            st.session_state.ranking_system.update_platform_stats(
                                "CodeChef",
                                difficulty=3100,
                                participation=0.5,
                                current_ratings={st.session_state.user_id: cc_profile["rating"]}
                            )
                            
                            # Generate heatmap data
                            cc_heatmap = generate_heatmap_data(0.2)
                            st.session_state.heatmap_data["cc"] = cc_heatmap
                            
                            st.success(f"Successfully fetched CodeChef profile for {cc_handle}")
                        else:
                            st.warning("Please fetch Codeforces profile first to establish user ID")
                    else:
                        st.error("Failed to fetch CodeChef profile. Please check the username.")
        
        # Display CodeChef profile if available
        if st.session_state.cc_profile:
            cc_rating = st.session_state.cc_profile["rating"]
            cc_rank = get_cc_rank(cc_rating)
            
            st.markdown(f"""
            ### CodeChef Profile
            - **Username:** {st.session_state.cc_profile["username"]}
            - **Rating:** {cc_rating}
            - **Stars:** {cc_rank}
            - **Global Rank:** {st.session_state.cc_profile["rank"]}
            - **Country Rank:** {st.session_state.cc_profile["country_rank"]}
            """)
        
        st.divider()
        
        # AtCoder (using imputation)
        if st.session_state.user_id:
            st.markdown("### AtCoder (Imputed)")
            st.info("No AtCoder API implemented. Using imputation based on other platform ratings.")
            
            # Calculate imputed rating
            atcoder_rating = st.session_state.ranking_system._impute_missing_rating(
                st.session_state.user_id, "Atcoder"
            )
            
            # Update AtCoder with imputed rating
            st.session_state.ranking_system.update_platform_stats(
                "Atcoder",
                difficulty=3500,
                participation=0.6,
                current_ratings={st.session_state.user_id: atcoder_rating}
            )
            
            st.markdown(f"**Imputed AtCoder Rating:** {atcoder_rating:.1f}")
    
    with tab2:
        st.header("Rating Analysis")
        
        if st.session_state.user_id:
            # Get user data from ranking system
            user_data = st.session_state.ranking_system.users.get(st.session_state.user_id, {})
            
            # Create columns for stats
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Rating Summary")
                
                # Calculate percentages
                platform_weights = st.session_state.ranking_system.final_weights
                total_weight = sum(platform_weights.values())
                
                # Create gauge chart for unified rating
                unified_rating = user_data.get("unified_rating", 0)
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = unified_rating,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Unified Rating"},
                    gauge = {
                        'axis': {'range': [None, 3000]},
                        'bar': {'color': "#1f77b4"},
                        'steps': [
                            {'range': [0, 1200], 'color': "lightgray"},
                            {'range': [1200, 2000], 'color': "gray"},
                            {'range': [2000, 3000], 'color': "darkgray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': unified_rating
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display platform ratings and weights
                st.subheader("Platform Contributions")
                
                platform_data = []
                for platform, rating in user_data.get("platform_ratings", {}).items():
                    weight = platform_weights.get(platform, 0) / total_weight if total_weight else 0
                    contribution = rating * weight
                    platform_data.append({
                        "Platform": platform,
                        "Rating": rating,
                        "Weight": weight * 100,  # as percentage
                        "Contribution": contribution
                    })
                
                platform_df = pd.DataFrame(platform_data)
                if not platform_df.empty:
                    # Platform weights pie chart
                    fig = go.Figure(data=[go.Pie(
                        labels=platform_df["Platform"],
                        values=platform_df["Weight"],
                        hole=.3,
                        textinfo="label+percent"
                    )])
                    fig.update_layout(title_text="Platform Weights (%)")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Platform data table
                    st.dataframe(
                        platform_df.style.format({
                            "Rating": "{:.1f}",
                            "Weight": "{:.1f}%",
                            "Contribution": "{:.1f}"
                        }),
                        use_container_width=True
                    )
            
            with col2:
                st.subheader("Final Rankings")
                
                # Add course bonus if available
                if st.session_state.total_bonus > 0:
                    user_data["course_bonus"] = st.session_state.total_bonus
                    user_data["total_rating"] = user_data.get("unified_rating", 0) + st.session_state.total_bonus
                
                # Create rating breakdown bar chart
                components = [
                    {"Component": "Base Rating", "Value": user_data.get("unified_rating", 0)},
                    {"Component": "Course Bonus", "Value": user_data.get("course_bonus", 0)}
                ]
                
                components_df = pd.DataFrame(components)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=components_df["Component"],
                    y=components_df["Value"],
                    marker_color=["#1f77b4", "#ff7f0e"]
                ))
                
                fig.update_layout(
                    title_text="Rating Components",
                    xaxis_title="Component",
                    yaxis_title="Points",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Total rating display
                total_rating = user_data.get("total_rating", user_data.get("unified_rating", 0))
                
                st.metric(
                    label="Total Rating",
                    value=f"{total_rating:.1f}",
                    delta=f"+{user_data.get('course_bonus', 0):.1f} from courses" if user_data.get('course_bonus', 0) > 0 else None
                )
                
                # Radar chart for platform ratings
                if user_data.get("platform_ratings"):
                    platforms = list(user_data["platform_ratings"].keys())
                    ratings = list(user_data["platform_ratings"].values())
                    
                    # Normalize ratings for radar chart
                    max_ratings = [st.session_state.ranking_system.platforms[p]["max_rating"] for p in platforms]
                    normalized_ratings = [r/m for r, m in zip(ratings, max_ratings)]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=normalized_ratings,
                        theta=platforms,
                        fill='toself',
                        name='Platform Ratings'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1]
                            )
                        ),
                        showlegend=False,
                        title="Platform Rating Distribution (Normalized)"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please connect at least one platform profile in the Profile Setup tab.")
    
    with tab3:
        st.header("Coding Activity Heatmap")
        
        if st.session_state.heatmap_data:
            # Combine heatmaps from different platforms
            cf_data = st.session_state.heatmap_data.get("cf", {})
            lc_data = st.session_state.heatmap_data.get("lc", {})
            cc_data = st.session_state.heatmap_data.get("cc", {})
            
            combined_data = combine_heatmaps(cf_data, lc_data, cc_data)
            
            # Create a selector for platform
            platform_option = st.selectbox(
                "Select Platform",
                ["All Platforms", "Codeforces", "Leetcode", "CodeChef"]
            )
            
            # Display appropriate heatmap
            if platform_option == "All Platforms":
                heatmap_data = combined_data
                title = "All Platforms Combined"
            elif platform_option == "Codeforces":
                heatmap_data = cf_data
                title = "Codeforces Activity"
            elif platform_option == "Leetcode":
                heatmap_data = lc_data
                title = "Leetcode Activity"
            elif platform_option == "CodeChef":
                heatmap_data = cc_data
                title = "CodeChef Activity"
            
            # Draw heatmap
            fig = draw_heatmap(heatmap_data)
            fig.update_layout(title=title)
            st.plotly_chart(fig, use_container_width=True)
            
            # Activity stats
            total_days = len(heatmap_data)
            total_submissions = sum(heatmap_data.values())
            max_day = max(heatmap_data.values()) if heatmap_data else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Days", total_days)
            with col2:
                st.metric("Total Submissions", total_submissions)
            with col3:
                st.metric("Max Submissions in a Day", max_day)
            
            # Activity trends
            if heatmap_data:
                # Convert to DataFrame for analysis
                trend_df = pd.DataFrame({
                    'date': pd.to_datetime(list(heatmap_data.keys())),
                    'submissions': list(heatmap_data.values())
                }).sort_values('date')
                
                # Add weekday column
                trend_df['weekday'] = trend_df['date'].dt.day_name()
                
                # Weekly activity pattern
                weekly_activity = trend_df.groupby('weekday')['submissions'].mean().reindex([
                    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
                ])
                
                fig = go.Figure(go.Bar(
                    x=weekly_activity.index,
                    y=weekly_activity.values,
                    marker_color='#1f77b4'
                ))
                
                fig.update_layout(
                    title="Average Submissions by Day of Week",
                    xaxis_title="Day of Week",
                    yaxis_title="Average Submissions"
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please connect at least one platform profile to view activity data.")
    
    with tab4:
        st.header("Course Bonus Calculator")
        
        st.write("""
        Add your educational achievements to boost your competitive programming rating.
        The course bonus can add up to 45 points to your total rating.
        """)
        
        # Course input form
        with st.form("course_form"):
            st.subheader("Educational Achievement Details")
            
            # Institution tier
            institution_tier = st.selectbox(
                "Institution Tier",
                ["Tier 1", "Tier 2", "Tier 3", "Other"],
                help="Tier 1: Ivy League, MIT, Stanford, etc. Tier 2: Other top universities. Tier 3: Regional universities."
            )
            
            # Course duration
            duration = st.slider(
                "Course Duration (months)",
                min_value=1,
                max_value=24,
                value=6,
                help="Longer courses provide higher bonus points."
            )
            
            # Field of study
            field = st.selectbox(
                "Field of Study",
                ["Computer Science", "Algorithms", "Data Structures", "Programming", 
                 "Software Engineering", "Machine Learning", "Mathematics", "Statistics", 
                 "Data Science", "Other"]
            )
            
            # Skills gained
            skills_options = [
                "Data Structures", "Algorithms", "Dynamic Programming", "Graph Theory",
                "Machine Learning", "Competitive Programming", "Problem Solving",
                "Python", "C++", "Java", "JavaScript", "Database Systems"
            ]
            skills = st.multiselect(
                "Skills Gained",
                options=skills_options,
                default=[],
                help="Select all skills that apply. More relevant skills provide higher bonus points."
            )
            
            # Certificate URL (optional)
            certificate_url = st.text_input(
                "Certificate URL (optional)",
                help="Link to your course certificate if available."
            )
            
            # Submit button
            submitted = st.form_submit_button("Calculate Bonus")
            
            if submitted:
                # Create course data
                course_data = {
                    "institution_tier": institution_tier,
                    "duration": duration,
                    "field": field,
                    "skills": skills,
                    "certificate_url": certificate_url
                }
                
                # Calculate bonus
                total_bonus, bonus_breakdown = calculate_course_bonus(course_data)
                
                # Save to session state
                st.session_state.course_data = course_data
                st.session_state.total_bonus = total_bonus
                st.session_state.bonus_breakdown = bonus_breakdown
                
                # Update user's course bonus in ranking system
                if st.session_state.user_id:
                    user_data = st.session_state.ranking_system.users.get(st.session_state.user_id, {})
                    user_data["course_bonus"] = total_bonus
                    user_data["total_rating"] = user_data.get("unified_rating", 0) + total_bonus
        
        # Display bonus results
        if st.session_state.total_bonus > 0:
            st.success(f"Course Bonus: {st.session_state.total_bonus:.1f} points ({(st.session_state.total_bonus/45*100):.1f}%)")
            
            # Bonus breakdown
            breakdown = st.session_state.bonus_breakdown
            
            st.subheader("Bonus Breakdown")
            breakdown_data = pd.DataFrame({
                "Component": ["Institution", "Duration", "Field", "Skills"],
                "Points": [
                    breakdown.get("institution", 0),
                    breakdown.get("duration", 0),
                    breakdown.get("field", 0),
                    breakdown.get("skills", 0)
                ],
                "Max Points": [15, 10, 10, 10]
            })
            
            # Create stacked bar chart for bonus breakdown
            fig = go.Figure()
            
            # Add earned points
            fig.add_trace(go.Bar(
                x=breakdown_data["Component"],
                y=breakdown_data["Points"],
                name="Earned Points",
                marker_color="#2ca02c"
            ))
            
            # Add remaining points
            fig.add_trace(go.Bar(
                x=breakdown_data["Component"],
                y=breakdown_data["Max Points"] - breakdown_data["Points"],
                name="Remaining Points",
                marker_color="lightgray"
            ))
            
            fig.update_layout(
                barmode='stack',
                title="Bonus Points Breakdown",
                xaxis_title="Component",
                yaxis_title="Points",
                legend_title="",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.dataframe(
                breakdown_data.style.format({
                    "Points": "{:.1f}",
                    "Max Points": "{:.1f}"
                }),
                use_container_width=True
            )
    
    # Footer
    st.divider()
    st.caption("Competitive Programming Unified Rating Dashboard - Developed with Streamlit")

if __name__ == "__main__":
    main()