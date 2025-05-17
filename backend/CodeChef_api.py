import requests
import re
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def fetch_codechef_profile(username):
    url = f"https://www.codechef.com/users/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {'error': f"Failed to fetch profile. HTTP {response.status_code}"}
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Rating
        rating_tag = soup.find("div", class_="rating-number")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        # Stars
        stars_tag = soup.find("span", class_="rating")
        stars = stars_tag.text.strip() if stars_tag else "N/A"

        # Global Rank
        global_rank = "N/A"
        global_rank_tag = soup.find('td', string=re.compile("Global Rank"))
        if global_rank_tag and global_rank_tag.find_next_sibling("td"):
            global_rank = global_rank_tag.find_next_sibling("td").text.strip()

        # Fully Solved
        fully_solved = "N/A"
        match = re.search(r'Fully Solved\s*\((\d+)\)', html)
        if match:
            fully_solved = match.group(1)

        activity_map = extract_activity_heatmap(html, soup)

        return {
            'username': username,
            'rating': rating,
            'stars': stars,
            'global_rank': global_rank,
            'fully_solved': fully_solved,
            'activity_map': activity_map
        }
    except requests.RequestException as e:
        return {'error': f"Connection error: {str(e)}"}
    except Exception as e:
        return {'error': f"Unexpected error: {str(e)}"}

def extract_activity_heatmap(html, soup=None):
    if soup is None:
        soup = BeautifulSoup(html, 'html.parser')

    activity_grid = {}

    try:
        rects = soup.select('svg rect[data-date]')
        for rect in rects:
            date = rect.get('data-date')
            count = int(rect.get('data-count', '0'))
            level = int(rect.get('data-level', '0'))
            if date:
                activity_grid[date] = {'count': count, 'level': level}

        if not activity_grid:
            return {'error': 'No activity data found'}

        return {
            'cells': activity_grid
        }
    except Exception as e:
        return {'error': f"Heatmap extraction error: {str(e)}"}

def print_codechef_profile(profile):
    if 'error' in profile:
        print(f"\nError: {profile['error']}")
        return

    print(f"\n👤 CodeChef Profile: @{profile['username']}")
    print(f"⭐ Rating        : {profile['rating']}")
    print(f"🌟 Stars         : {profile['stars']}")
    print(f"🌍 Global Rank   : {profile['global_rank']}")
    print(f"✅ Fully Solved  : {profile['fully_solved']}")

    activity_map = profile['activity_map']
    if not activity_map or 'error' in activity_map:
        print("\n📉 Activity Map: Not available or error in parsing.")
        return

    cells = activity_map['cells']
    active_days = sum(1 for d in cells.values() if d['count'] > 0)
    total_days = len(cells)
    percent = (active_days / total_days) * 100 if total_days > 0 else 0

    print("\n📊 Activity Summary:")
    print(f"  Active Days     : {active_days}/{total_days} ({percent:.1f}%)")

    level_counts = {i: 0 for i in range(5)}
    for data in cells.values():
        lvl = data.get('level', 0)
        if lvl in level_counts:
            level_counts[lvl] += 1

    for i in range(5):
        label = ["No", "Light", "Medium", "High", "Very High"][i]
        print(f"  {label:<12} (Level {i}): {level_counts[i]}")

    print("\n🗓️  Activity Heatmap (ASCII):")
    print("     " + " ".join(["M", "T", "W", "T", "F", "S", "S"]))
    week = ["·"] * 7
    all_dates = sorted(cells.keys())
    if not all_dates:
        print("No heatmap data")
        return

    start_date = datetime.strptime(all_dates[0], "%Y-%m-%d")
    end_date = datetime.strptime(all_dates[-1], "%Y-%m-%d")
    date = start_date

    while date <= end_date:
        if date.weekday() == 0:
            week = []

        day_str = date.strftime("%Y-%m-%d")
        if day_str in cells:
            level = cells[day_str]['level']
            symbol = ["·", "▪", "▪▪", "▪▪▪", "▪▪▪▪"][level]
        else:
            symbol = " "

        week.append(f"{symbol:2}")
        if len(week) == 7:
            print("     " + " ".join(week))
        date += timedelta(days=1)

    # Streak Calculation
    print("\n🔥 Activity Streaks:")
    streaks = []
    current_streak = []
    prev_date = None

    for date_str in sorted(cells.keys()):
        if cells[date_str]['count'] > 0:
            curr_date = datetime.strptime(date_str, "%Y-%m-%d")
            if prev_date and (curr_date - prev_date).days == 1:
                current_streak.append(curr_date)
            else:
                if current_streak:
                    streaks.append(current_streak)
                current_streak = [curr_date]
            prev_date = curr_date

    if current_streak:
        streaks.append(current_streak)

    if streaks:
        longest = max(streaks, key=len)
        print(f"  🔁 Longest streak: {len(longest)} days ({longest[0].date()} → {longest[-1].date()})")
        latest = streaks[-1]
        if (datetime.today().date() - latest[-1].date()).days == 0:
            print(f"  🚀 Current streak: {len(latest)} days (Ongoing)")
        else:
            print(f"  ⏹️  Current streak ended at {latest[-1].date()} ({len(latest)} days)")
    else:
        print("  No streaks found.")

if __name__ == "__main__":
    username = input("Enter CodeChef Username: ").strip()
    profile = fetch_codechef_profile(username)
    print_codechef_profile(profile)
