import requests
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from bs4 import BeautifulSoup
import json
import re
from matplotlib.colors import LinearSegmentedColormap
import calendar

# ------------------ LeetCode Heatmap ------------------

def get_leetcode_heatmap(username):
    query = {
        "query": """
        query userCalendar($username: String!) {
            matchedUser(username: $username) {
                userCalendar {
                    submissionCalendar
                }
            }
        }
        """,
        "variables": {"username": username}
    }

    response = requests.post("https://leetcode.com/graphql", json=query)
    data = response.json()

    try:
        submission_data = data['data']['matchedUser']['userCalendar']['submissionCalendar']
        heatmap = {}
        for timestamp, count in eval(submission_data).items():
            date = datetime.datetime.fromtimestamp(int(timestamp)).date()
            heatmap[str(date)] = int(count)
        return heatmap
    except:
        print("LeetCode user not found or no data.")
        return {}

# ------------------ Codeforces Heatmap ------------------

def get_codeforces_heatmap(username):
    url = f'https://codeforces.com/api/user.status?handle={username}&from=1&count=10000'
    response = requests.get(url).json()
    heatmap = {}
    if response['status'] != 'OK':
        print("Codeforces user not found or error.")
        return {}
    for sub in response['result']:
        date = datetime.datetime.fromtimestamp(sub['creationTimeSeconds']).date()
        date_str = str(date)
        heatmap[date_str] = heatmap.get(date_str, 0) + 1
    return heatmap

# ------------------ CodeChef Heatmap ------------------

def get_codechef_heatmap(username):
    url = f"https://www.codechef.com/users/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    script = soup.find("script", string=lambda s: s and "activityData" in s)
    if not script:
        print("CodeChef activityData not found.")
        return {}

    match = re.search(r'activityData\s*=\s*(\{.*?\});', script.string, re.DOTALL)
    if not match:
        print("CodeChef activityData parse error.")
        return {}

    raw_data = match.group(1)
    data = json.loads(raw_data)
    heatmap = {}
    for entry in data.get('data', []):
        date = entry['date']
        count = entry['value']
        heatmap[date] = heatmap.get(date, 0) + count
    return heatmap

# ------------------ Combine Heatmaps ------------------

def combine_heatmaps(*heatmaps):
    combined = {}
    for heatmap in heatmaps:
        for date, count in heatmap.items():
            combined[date] = combined.get(date, 0) + count
    return combined

# ------------------ Draw GitHub-style Heatmap ------------------

def draw_github_style_heatmap(heatmap_data, title="Coding Activity"):
    # Create a date range for the last year
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365)
    
    # Create a list of all dates in the range
    date_range = [start_date + datetime.timedelta(days=x) for x in range(366)]
    
    # Create a DataFrame with all dates
    all_dates_df = pd.DataFrame({
        'date': date_range,
        'count': [heatmap_data.get(str(date), 0) for date in date_range]
    })
    
    # Calculate additional columns
    all_dates_df['weekday'] = all_dates_df['date'].apply(lambda x: x.weekday())
    all_dates_df['week_number'] = all_dates_df['date'].apply(lambda x: (x - start_date).days // 7)
    
    # Create a pivot table for the heatmap
    pivot_table = all_dates_df.pivot_table(
        index='weekday', 
        columns='week_number',
        values='count', 
        fill_value=0
    )
    
    # Sort weekdays so Sunday is at the top (GitHub style)
    pivot_table = pivot_table.sort_index(ascending=False)
    
    # Calculate max value for color scaling
    max_value = max(all_dates_df['count'].max(), 1)  # Avoid division by zero
    
    # Create GitHub-like color map (white to darker green)
    github_colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']
    github_cmap = LinearSegmentedColormap.from_list('github', github_colors)
    
    # --- Custom Drawing with Borders and Spacing ---
    fig, ax = plt.subplots(figsize=(16, 3))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    n_weeks = pivot_table.shape[1]
    n_days = 7  # Always 7 days in a week
    
    box_size = 1
    gap = 0.15  # Small gap between boxes
    
    # Draw each box manually
    for week in range(n_weeks):
        for day in range(n_days):
            count = pivot_table.iloc[day, week] if week in pivot_table.columns and day in pivot_table.index else 0
            # Map count to color
            if count == 0:
                color = github_colors[0]
            elif count < 4:
                color = github_colors[1]
            elif count < 10:
                color = github_colors[2]
            elif count < 20:
                color = github_colors[3]
            else:
                color = github_colors[4]
            rect = plt.Rectangle(
                (week * (box_size + gap), day * (box_size + gap)),
                box_size, box_size,
                facecolor=color,
                edgecolor='black',
                linewidth=1.2
            )
            ax.add_patch(rect)
    
    # Set limits and invert y-axis so Sunday is at the top
    ax.set_xlim(0, n_weeks * (box_size + gap))
    ax.set_ylim(n_days * (box_size + gap), 0)
    
    # Remove all spines and ticks
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add month labels on top
    month_labels = []
    month_positions = []
    for i, date in enumerate(date_range):
        if date.day == 1:
            month_labels.append(date.strftime('%b'))
            month_positions.append((i // 7) * (box_size + gap))
    ax.set_xticks(month_positions)
    ax.set_xticklabels(month_labels, color='white')
    ax.tick_params(axis='x', length=0, pad=5, colors='white')
    
    # Add weekday labels
    weekday_labels = ['Mon', '', 'Wed', '', 'Fri', '', 'Sun']
    ax.set_yticks([(i + 0.5) * (box_size + gap) for i in range(7)])
    ax.set_yticklabels(weekday_labels, color='white')
    ax.tick_params(axis='y', length=0, pad=10, colors='white')
    
    # Add legend
    legend_labels = ['No contributions', '1-3 contributions', '4-9 contributions', 
                     '10-19 contributions', '20+ contributions']
    from matplotlib.patches import Patch
    handles = [Patch(facecolor=color, edgecolor='black', linewidth=1.2) for color in github_colors]
    plt.figlegend(handles, legend_labels, loc='upper center', 
                  ncol=5, frameon=False, bbox_to_anchor=(0.5, 0), 
                  bbox_transform=fig.transFigure, labelcolor='white')
    
    # Add title
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.95, color='white')
    
    # Adjust layout
    plt.subplots_adjust(top=0.85, bottom=0.2)
    plt.tight_layout()
    plt.show()

    # Return statistics for summary
    total_contributions = all_dates_df['count'].sum()
    active_days = (all_dates_df['count'] > 0).sum()
    max_streak = calculate_max_streak(all_dates_df)
    current_streak = calculate_current_streak(all_dates_df)
    
    return {
        'total_contributions': total_contributions,
        'active_days': active_days,
        'max_streak': max_streak,
        'current_streak': current_streak
    }

def calculate_max_streak(df):
    """Calculate the longest streak of consecutive days with contributions."""
    streak = 0
    max_streak = 0
    for _, row in df.sort_values('date').iterrows():
        if row['count'] > 0:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    return max_streak

def calculate_current_streak(df):
    """Calculate the current streak of consecutive days with contributions."""
    streak = 0
    for _, row in df.sort_values('date', ascending=False).iterrows():
        if row['count'] > 0:
            streak += 1
        else:
            break
    return streak

# ------------------ Main Execution with UI ------------------

def main():
    print("\n" + "="*50)
    print("📊 Cross-Platform Coding Activity Visualization 📊")
    print("="*50)
    print("Track your coding activity from LeetCode, Codeforces, and CodeChef")
    print("in a GitHub-style contribution graph\n")
    
    # Get usernames with validation
    leetcode_user = input("Enter LeetCode username (or leave blank to skip): ").strip()
    codeforces_user = input("Enter Codeforces username (or leave blank to skip): ").strip()
    codechef_user = input("Enter CodeChef username (or leave blank to skip): ").strip()
    
    if not (leetcode_user or codeforces_user or codechef_user):
        print("\n⚠️ Error: Please enter at least one username")
        return
    
    print("\n🔄 Fetching your coding activity data...")
    
    # Get heatmaps with progress indicators
    leet = {}
    cf = {}
    cc = {}
    
    if leetcode_user:
        print("  • Retrieving LeetCode data...", end="", flush=True)
        leet = get_leetcode_heatmap(leetcode_user)
        print(" ✅" if leet else " ❌")
        
    if codeforces_user:
        print("  • Retrieving Codeforces data...", end="", flush=True)
        cf = get_codeforces_heatmap(codeforces_user)
        print(" ✅" if cf else " ❌")
        
    if codechef_user:
        print("  • Retrieving CodeChef data...", end="", flush=True)
        cc = get_codechef_heatmap(codechef_user)
        print(" ✅" if cc else " ❌")
    
    # Combine the heatmaps
    combined = combine_heatmaps(leet, cf, cc)
    
    if not combined:
        print("\n❌ No activity data found. Please check your usernames and try again.")
        return
    
    # Generate title based on active platforms
    platforms = []
    if leet: platforms.append("LeetCode")
    if cf: platforms.append("Codeforces")
    if cc: platforms.append("CodeChef")
    
    title = "Coding Activity: " + " + ".join(platforms)
    
    print("\n📈 Generating GitHub-style contribution graph...")
    stats = draw_github_style_heatmap(combined, title)
    
    # Display statistics
    print("\n📊 Activity Summary:")
    print(f"  • Total contributions: {stats['total_contributions']}")
    print(f"  • Active days: {stats['active_days']} out of 365")
    print(f"  • Longest streak: {stats['max_streak']} days")
    print(f"  • Current streak: {stats['current_streak']} days")
    
    print("\n✨ Done! Your coding activity graph has been displayed.")

if __name__ == "__main__":
    main()