from flask import Flask, request, jsonify

from logic_formulas.formula_main import UnifiedRankingSystem, User
from rating_scraper_api.CodeForces_api import fetch_codeforces_profile_api
from rating_scraper_api.leetcode_api import fetch_leetcode_profile
from rating_scraper_api.CodeChef_api import fetch_codechef_profile
from cousera.run import run_interactive
from heatmap.heat_map import (
    get_codeforces_heatmap,
    get_leetcode_heatmap,
    get_codechef_heatmap,
    combine_heatmaps,
    draw_github_style_heatmap,
)
from bonus_calculatorF import bonus_calculator

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Starization API!"})

@app.route("/analyze", methods=["POST"])
def analyze_user():
    data = request.get_json()

    handle_CF = data.get("codeforces")
    handle_LC = data.get("leetcode")
    handle_CC = data.get("codechef")
    coursera_url = data.get("coursera_url")

    ranking_system = UnifiedRankingSystem()
    ranking_system.add_platform("Codeforces", max_rating=3000)
    ranking_system.add_platform("Leetcode", max_rating=2500)
    ranking_system.add_platform("Atcoder", max_rating=2800)
    ranking_system.add_platform("CodeChef", max_rating=1800)

    user_id = handle_CF or handle_LC or handle_CC
    if not user_id:
        return jsonify({"error": "At least one valid platform handle required."}), 400

    ranking_system.add_user(user_id)

    # ----- Codeforces -----
    if handle_CF:
        profile_CF = fetch_codeforces_profile_api(handle_CF)
        rating = int(profile_CF["rating"]) if profile_CF and profile_CF["rating"] != "N/A" else ranking_system._impute_missing_rating(User(user_id), "Codeforces")
        ranking_system.update_platform_stats("Codeforces", 2100, 0.8, {user_id: rating})

    # ----- Leetcode -----
    if handle_LC:
        profile_LC = fetch_leetcode_profile(handle_LC)
        rating = int(profile_LC["rating"]) if profile_LC and profile_LC["rating"] != "N/A" else ranking_system._impute_missing_rating(ranking_system.users[user_id], "Leetcode")
        ranking_system.update_platform_stats("Leetcode", 2100, 0.8, {user_id: rating})

    # ----- CodeChef -----
    if handle_CC:
        profile_CC = fetch_codechef_profile(handle_CC)
        rating = int(profile_CC["rating"]) if profile_CC and profile_CC["rating"] != "N/A" else ranking_system._impute_missing_rating(ranking_system.users[user_id], "CodeChef")
        ranking_system.update_platform_stats("CodeChef", 3100, 0.5, {user_id: rating})

    # ----- Atcoder -----
    atcoder_rating = ranking_system._impute_missing_rating(ranking_system.users[user_id], "Atcoder")
    ranking_system.update_platform_stats("Atcoder", 3500, 0.6, {user_id: atcoder_rating})

    # ----- Coursera -----
    if coursera_url:
        course_data = run_interactive(coursera_url)
        total_bonus = bonus_calculator.total_bonus_sum
        ranking_system.users[user_id].course_bonus = total_bonus
        ranking_system.users[user_id].total_rating = ranking_system.users[user_id].unified_rating + total_bonus
    else:
        total_bonus = 0

    # ----- Final Rankings -----
    rankings = ranking_system.get_rankings()
    user = ranking_system.users[user_id]

    result = {
        "user_id": user_id,
        "unified_rating": user.unified_rating,
        "course_bonus": user.course_bonus,
        "total_rating": user.total_rating,
        "platform_breakdown": user.platform_ratings,
        "ranking_position": next((i+1 for i, x in enumerate(rankings) if x[0] == user_id), None)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
