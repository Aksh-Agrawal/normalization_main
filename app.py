from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
import calendar
import streamlit as st
import time
import random

from main import UnifiedRankingSystem
from rating_scraper_api.CodeForces_api import fetch_codeforces_profile_api
from rating_scraper_api.leetcode_api import fetch_leetcode_profile
from rating_scraper_api.CodeChef_api import fetch_codechef_profile
from heatmap.heat_map import get_codeforces_heatmap, get_leetcode_heatmap, get_codechef_heatmap, combine_heatmaps

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_profiles():
    data = request.json
    ranking_system = UnifiedRankingSystem()
    
    # Initialize platforms
    ranking_system.add_platform("Codeforces", max_rating=3000)
    ranking_system.add_platform("Leetcode", max_rating=2500)
    ranking_system.add_platform("CodeChef", max_rating=1800)
    
    # Process handles
    user_id = data.get('codeforces') or data.get('leetcode') or data.get('codechef')
    if not user_id:
        return jsonify({'error': 'No valid handles provided'}), 400
    
    ranking_system.add_user(user_id)
    
    # Fetch and process profiles
    results = {}
    
    if data.get('codeforces'):
        cf_data = fetch_codeforces_profile_api(data['codeforces'])
        if cf_data:
            results['codeforces'] = cf_data
    
    if data.get('leetcode'):
        lc_data = fetch_leetcode_profile(data['leetcode'])
        if lc_data:
            results['leetcode'] = lc_data
    
    if data.get('codechef'):
        cc_data = fetch_codechef_profile(data['codechef'])
        if cc_data:
            results['codechef'] = cc_data
    
    return jsonify(results)

def draw_heatmap(heatmap_data):
    """
    Draw a GitHub-style contribution heatmap
    
    Parameters:
    -----------
    heatmap_data : dict
        Dictionary with dates as keys and contribution counts as values
    
    Returns:
    --------
    fig : matplotlib.figure.Figure
        The matplotlib figure object with the heatmap
    """
    # Convert the heatmap data to a DataFrame
    data = []
    for date_str, value in heatmap_data.items():
        try:
            date = pd.to_datetime(date_str)
            data.append({'date': date, 'value': value})
        except:
            # Skip invalid dates
            continue
    
    if not data:
        # Return an empty figure if no data
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.text(0.5, 0.5, "No data available", ha='center', va='center', fontsize=16)
        plt.tight_layout()
        return fig
    
    # Create DataFrame from data
    df = pd.DataFrame(data)
    
    # Ensure 'date' column is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract day of week and week number
    df['day'] = df['date'].dt.dayofweek
    df['week'] = df['date'].dt.isocalendar().week
    
    # Add year to handle week numbers across year boundaries
    df['year'] = df['date'].dt.isocalendar().year
    
    # Create adjusted week number to ensure continuous sequence across years
    df['week_adj'] = (df['year'] - df['year'].min()) * 53 + df['week']
    
    # Handle duplicate combinations by aggregating values
    merged_df = df.groupby(['day', 'week_adj'], as_index=False)['value'].sum()
    
    # Create the pivot table, handling duplicates by aggregation
    pivot_value = merged_df.pivot(index='day', columns='week_adj', values='value')
    
    # Create a custom colormap for the heatmap
    colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']
    github_cmap = LinearSegmentedColormap.from_list('github', colors)
    
    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot the heatmap
    heatmap = ax.pcolor(pivot_value, cmap=github_cmap, edgecolors='w', linewidths=1)
    
    # Set y-axis labels for days of the week
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax.set_yticks(np.arange(0.5, len(days)))
    ax.set_yticklabels(days)
    
    # Add month labels on x-axis
    week_indices = pivot_value.columns
    if not week_indices.empty:
        # Create a mapping from week_adj to actual date
        week_to_date = {}
        for _, row in df.iterrows():
            week_adj = row['week_adj']
            date = row['date']
            if week_adj not in week_to_date:
                week_to_date[week_adj] = date
        
        # Place month labels at appropriate positions
        month_positions = []
        month_labels = []
        current_month = None
        
        for week in week_indices:
            if week in week_to_date:
                date = week_to_date[week]
                # Check if this is a valid datetime
                if pd.notna(date):
                    try:
                        month = date.month
                        if month != current_month:
                            current_month = month
                            col_idx = week_indices.get_loc(week)
                            month_positions.append(col_idx)
                            month_labels.append(date.strftime('%b'))
                    except:
                        # Skip if date can't be formatted
                        continue
        
        # Set x-axis ticks and labels for months
        ax.set_xticks(month_positions)
        ax.set_xticklabels(month_labels)
    
    # Add title and adjust layout
    ax.set_title('Contribution Activity')
    plt.tight_layout()
    
    return fig

def main():
    # Set up Streamlit page
    st.set_page_config(page_title="Coding Profile Analyzer", layout="wide")
    st.title("📊 Coding Profile Analyzer")
    
    # Initialize session state for sharing data between tabs
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'unified_rating' not in st.session_state:
        st.session_state.unified_rating = None
    if 'course_bonus' not in st.session_state:
        st.session_state.course_bonus = 0
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Profile Analysis", "Activity Heatmap", "Course Bonus"])
    
    with tab1:
        st.header("Profile Analysis")
        
        # Input fields for coding platform handles
        col1, col2, col3 = st.columns(3)
        with col1:
            codeforces_handle = st.text_input("Codeforces Handle", key="cf_handle")
        with col2:
            leetcode_handle = st.text_input("LeetCode Handle", key="lc_handle")
        with col3:
            codechef_handle = st.text_input("CodeChef Handle", key="cc_handle")
            
        # Analysis button
        if st.button("Analyze Profiles"):
            if not (codeforces_handle or leetcode_handle or codechef_handle):
                st.error("Please enter at least one platform handle")
            else:
                with st.spinner("Analyzing profiles..."):
                    # Create progress simulation
                    progress_bar = st.progress(0)
                    for i in range(100):
                        # Update progress bar
                        progress_bar.progress(i + 1)
                        # Sleep for a short time to simulate work
                        time.sleep(0.02)
                    
                    # Perform actual analysis
                    results = {}
                    ranking_system = UnifiedRankingSystem()
                    
                    # Initialize platforms
                    ranking_system.add_platform("Codeforces", max_rating=3000)
                    ranking_system.add_platform("Leetcode", max_rating=2500)
                    ranking_system.add_platform("CodeChef", max_rating=1800)
                    
                    # Process handles
                    user_id = codeforces_handle or leetcode_handle or codechef_handle
                    ranking_system.add_user(user_id)
                      # Fetch and display profiles
                    if codeforces_handle:
                        cf_data = fetch_codeforces_profile_api(codeforces_handle)
                        if cf_data:
                            results['codeforces'] = cf_data
                            st.subheader("Codeforces Profile")
                            st.json(cf_data)
                            if cf_data.get("rating") != 'N/A':
                                cf_rating = int(cf_data["rating"])
                                ranking_system.update_platform_stats(
                                    "Codeforces",
                                    difficulty=2100,
                                    participation=0.8,
                                    current_ratings={user_id: cf_rating}
                                )
                    
                    if leetcode_handle:
                        lc_data = fetch_leetcode_profile(leetcode_handle)
                        if lc_data:
                            results['leetcode'] = lc_data
                            st.subheader("LeetCode Profile")
                            st.json(lc_data)
                            if lc_data.get("rating") != 'N/A':
                                lc_rating = int(lc_data["rating"])
                                ranking_system.update_platform_stats(
                                    "Leetcode",
                                    difficulty=2100,
                                    participation=0.8,
                                    current_ratings={user_id: lc_rating}
                                )
                    
                    if codechef_handle:
                        cc_data = fetch_codechef_profile(codechef_handle)
                        if cc_data:
                            results['codechef'] = cc_data
                            st.subheader("CodeChef Profile")
                            st.json(cc_data)
                            if cc_data.get("rating") != 'N/A':
                                cc_rating = int(cc_data["rating"])
                                ranking_system.update_platform_stats(
                                    "CodeChef",
                                    difficulty=3100,
                                    participation=0.5,
                                    current_ratings={user_id: cc_rating}
                                )
                      # Calculate and display normalized rating
                    st.subheader("Unified Rating")
                    
                    if user_id in ranking_system.users:
                        user = ranking_system.users[user_id]
                        
                        # Store user_id in session state for use across tabs
                        st.session_state.user_id = user_id
                        st.session_state.unified_rating = user.unified_rating
                        
                        # Display unified rating
                        st.success(f"Unified Rating: {user.unified_rating:.1f}")
                        
                        # Show detailed breakdown
                        st.subheader("Rating Breakdown")
                        
                        # Create columns for each platform
                        cols = st.columns(len(user.platform_ratings))
                        
                        # Display rating for each platform
                        for i, (platform, rating) in enumerate(user.platform_ratings.items()):
                            weight = ranking_system.final_weights.get(platform, 0)
                            with cols[i]:
                                st.metric(
                                    f"{platform}", 
                                    f"{rating:.1f}", 
                                    f"Weight: {weight:.2f}"
                                )
                        
                        # If course bonus exists, include it in the total
                        if st.session_state.course_bonus > 0:
                            st.subheader("Total Score with Course Bonus")
                            total_score = user.unified_rating + st.session_state.course_bonus
                            st.success(f"Total Score: {total_score:.1f}")
                            st.info(f"Includes course bonus of {st.session_state.course_bonus:.1f} points")
    
    with tab2:
        st.header("Activity Heatmap")
        
        # Use the same handles from tab1 or let users input different ones
        use_same_handles = st.checkbox("Use same handles as Profile Analysis", value=True)
        if not use_same_handles:
            col1, col2, col3 = st.columns(3)
            with col1:
                cf_handle_heatmap = st.text_input("Codeforces Handle", key="cf_handle_hm")
            with col2:
                lc_handle_heatmap = st.text_input("LeetCode Handle", key="lc_handle_hm")
            with col3:
                cc_handle_heatmap = st.text_input("CodeChef Handle", key="cc_handle_hm")
        else:
            # Access handles from the first tab using session_state
            cf_handle_heatmap = st.session_state.get('cf_handle', '')
            lc_handle_heatmap = st.session_state.get('lc_handle', '')
            cc_handle_heatmap = st.session_state.get('cc_handle', '')
        
        if st.button("Generate Heatmap"):
            if not (cf_handle_heatmap or lc_handle_heatmap or cc_handle_heatmap):
                st.error("Please enter at least one platform handle")
            else:
                with st.spinner("Generating heatmap..."):
                    # Fetch heatmap data
                    heatmap_data = {}
                    
                    if cf_handle_heatmap:
                        cf_heatmap = get_codeforces_heatmap(cf_handle_heatmap)
                        heatmap_data.update(cf_heatmap)
                    
                    if lc_handle_heatmap:
                        lc_heatmap = get_leetcode_heatmap(lc_handle_heatmap)
                        heatmap_data.update(lc_heatmap)
                    
                    if cc_handle_heatmap:
                        cc_heatmap = get_codechef_heatmap(cc_handle_heatmap)
                        heatmap_data.update(cc_heatmap)
                    
                    # Generate and display heatmap
                    if heatmap_data:
                        fig = draw_heatmap(heatmap_data)
                        st.pyplot(fig)
                        
                        # Show activity statistics
                        total_contributions = sum(heatmap_data.values())
                        active_days = len(heatmap_data)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Contributions", total_contributions)
                        with col2:
                            st.metric("Active Days", active_days)
                    else:
                        st.error("No activity data found for the provided handles")
    with tab3:
        st.header("Course and Certification Bonus")
        st.info("This section allows you to enter your completed courses and certifications to calculate bonus points.")
        
        # Coursera profile URL input
        coursera_url = st.text_input("Coursera Profile URL", placeholder="https://www.coursera.org/user/...")
        
        if st.button("Calculate Course Bonus"):
            if not coursera_url:
                st.error("Please enter your Coursera profile URL")
            else:
                with st.spinner("Calculating course bonus..."):                    # Import necessary modules here to avoid circular imports
                    from cousera.run import run_interactive
                    from bonus_calculatorF import bonus_calculator
                    from bonus_calculatorF.bonus_calculator import calculate_profile_bonus
                    
                    # Progress simulation
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.01)
                    
                    try:
                        # Run the coursera scraper with the provided URL
                        course_data = run_interactive(coursera_url)
                        
                        if course_data:                            # Calculate bonus using the actual bonus calculator
                            bonus_result = calculate_profile_bonus(course_data)
                            total_bonus = bonus_calculator.total_bonus_sum
                            
                            # Display the calculated bonus
                            st.success(f"Course Bonus Calculated: {total_bonus:.2f} points")
                            st.success(f"Unified Total Rating: {total_bonus+total_score:.2f} points")
                            
                            # Show bonus breakdown
                            st.subheader("Bonus Breakdown")
                            col1, col2 = st.columns(2)
                            
                            # Get detailed breakdown
                            breakdown = bonus_result.get('breakdown', {})
                            with col1:
                                st.metric("Institution Quality", f"{breakdown.get('institution', 0):.2f}")
                                st.metric("Course Duration", f"{breakdown.get('duration', 0):.2f}")
                            with col2:
                                st.metric("Field Relevance", f"{breakdown.get('field', 0):.2f}")
                                st.metric("Skills Acquired", f"{breakdown.get('skills', 0):.2f}")
                              # Store the bonus in session state for use across tabs
                            st.session_state.course_bonus = total_bonus
                            
                            # If there's an active user profile, show combined score
                            if st.session_state.unified_rating is not None:
                                st.subheader("Combined Score")
                                total_score = st.session_state.unified_rating + total_bonus
                                st.success(f"Total Score: {total_score:.1f}")
                                st.info(f"Base Rating: {st.session_state.unified_rating:.1f} + Bonus: {total_bonus:.1f}")
                        else:
                            st.warning("Could not retrieve course data. Using simulated bonus.")
                            total_bonus = random.uniform(5, 45)
                            st.success(f"Course Bonus (Simulated): {total_bonus:.2f} points")
                            
                            # Show dummy bonus breakdown
                            st.subheader("Bonus Breakdown (Simulated)")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Institution Quality", f"{random.uniform(0, 15):.2f}")
                                st.metric("Course Duration", f"{random.uniform(0, 10):.2f}")
                            with col2:
                                st.metric("Field Relevance", f"{random.uniform(0, 10):.2f}")
                                st.metric("Skills Acquired", f"{random.uniform(0, 10):.2f}")
                    except Exception as e:
                        st.error(f"Error calculating bonus: {str(e)}")
                        st.info("Using backup simulation method...")
                        total_bonus = random.uniform(5, 45)
                        st.success(f"Course Bonus (Simulated): {total_bonus:.2f} points")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        app.run(debug=True)
    else:
        main()