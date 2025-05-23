from flask import Flask, request, jsonify
from flask_cors import CORS
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
)
from bonus_calculatorF import bonus_calculator
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_profiles():
    try:
        data = request.json
        ranking_system = UnifiedRankingSystem()
        
        # Initialize platforms
        ranking_system.add_platform("Codeforces", max_rating=3000)
        ranking_system.add_platform("Leetcode", max_rating=2500)
        ranking_system.add_platform("Atcoder", max_rating=2800)
        ranking_system.add_platform("CodeChef", max_rating=1800)
        
        # Process handles
        codeforces_handle = data.get('codeforces')
        leetcode_handle = data.get('leetcode')
        codechef_handle = data.get('codechef')
        
        # Use the first valid handle as the user_id
        user_id = codeforces_handle or leetcode_handle or codechef_handle
        
        if not user_id:
            return jsonify({'error': 'No valid handles provided'}), 400
        
        # Add the user to the system
        ranking_system.add_user(user_id)
    
        # Process Codeforces
        cf_data = None
        if codeforces_handle:
            cf_data = fetch_codeforces_profile_api(codeforces_handle)
            if cf_data:
                cf_rating = int(cf_data["rating"]) if cf_data["rating"] != 'N/A' else None
                if not cf_rating:
                    cf_rating = ranking_system._impute_missing_rating(ranking_system.users[user_id], "Codeforces")
                
                ranking_system.update_platform_stats(
                    "Codeforces",
                    difficulty=2100,
                    participation=0.8,
                    current_ratings={user_id: cf_rating}
                )
        
        # Process Leetcode
        lc_data = None
        if leetcode_handle:
            lc_data = fetch_leetcode_profile(leetcode_handle)
            if lc_data:
                lc_rating = int(lc_data["rating"]) if lc_data["rating"] != 'N/A' else None
                if not lc_rating:
                    lc_rating = ranking_system._impute_missing_rating(ranking_system.users[user_id], "Leetcode")
                
                ranking_system.update_platform_stats(
                    "Leetcode",
                    difficulty=1800,
                    participation=0.7,
                    current_ratings={user_id: lc_rating}
                )

        # Process CodeChef
        cc_data = None
        if codechef_handle:
            cc_data = fetch_codechef_profile(codechef_handle)
            if cc_data:
                cc_rating = int(cc_data["rating"]) if cc_data["rating"] != 'N/A' else None
                if not cc_rating:
                    cc_rating = ranking_system._impute_missing_rating(ranking_system.users[user_id], "CodeChef")
                ranking_system.update_platform_stats(
                    "CodeChef",
                    difficulty=1600,
                    participation=0.6,
                    current_ratings={user_id: cc_rating}
                )

        # Calculate unified ranking
        unified_score = ranking_system.calculate_unified_ranking(user_id)

        return jsonify({
            "user_id": user_id,
            "unified_score": unified_score,
            "codeforces": cf_data,
            "leetcode": lc_data,
            "codechef": cc_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/coursera', methods=['POST'])
def analyze_coursera():
    data = request.json
    profile_url = data.get('url')
    
    if not profile_url:
        return jsonify({'error': 'No profile URL provided'}), 400
    
    try:
        # Reset the bonus calculator
        bonus_calculator.total_bonus_sum = 0
        
        # Run the coursera scraper
        course_data = run_interactive(profile_url)
        
        # Get the total bonus
        total_bonus = bonus_calculator.total_bonus_sum
        
        # Get bonus breakdown
        bonus_breakdown = {
            "institution": 0,
            "duration": 0,
            "field": 0,
            "skills": 0
        }
        
        if course_data and 'bonus_breakdown' in course_data:
            bonus_breakdown = course_data['bonus_breakdown']
        
        return jsonify({
            "total_bonus": total_bonus,
            "bonus_breakdown": bonus_breakdown,
            "percentage": (total_bonus / 45) * 100
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
