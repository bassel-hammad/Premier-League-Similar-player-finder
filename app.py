from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend integration

# Global variables for our data and models
players_data = None
similarity_matrix = None
scaler = StandardScaler()

def load_sample_data():
    """
    Load sample Premier League midfielder data.
    
    Why sample data first?
    - Quick to test and develop with
    - No API rate limits or authentication needed
    - Easy to understand the data structure
    - Can focus on the ML algorithm
    """
    global players_data
    
    # Sample data representing real midfielder statistics
    # Expanded dataset: 20 Premier League midfielders across different playing styles
    sample_players = {
        'player_id': range(1, 21),
        'player_name': [
            # Original 10 players
            'Kevin De Bruyne', 'Bruno Fernandes', 'Mason Mount',
            'Declan Rice', 'Rodri', 'Jordan Henderson', 
            'James Maddison', 'Conor Gallagher', 'Yves Bissouma',
            'Martin Odegaard',
            # Additional 10 players for better recommendations
            'Bernardo Silva', 'Phil Foden', 'Ilkay Gündogan',
            'Casemiro', 'Fabinho', 'N\'Golo Kanté',
            'Luka Modrić', 'Bukayo Saka', 'Harvey Elliott',
            'Alexis Mac Allister'
        ],
        'team': [
            # Original teams
            'Manchester City', 'Manchester United', 'Chelsea',
            'Arsenal', 'Manchester City', 'Al-Ettifaq',
            'Tottenham', 'Chelsea', 'Brighton', 'Arsenal',
            # Additional teams
            'Manchester City', 'Manchester City', 'Manchester City',
            'Manchester United', 'Liverpool', 'Chelsea',
            'Real Madrid', 'Arsenal', 'Liverpool',
            'Brighton'
        ],
        'position': [
            # Original positions
            'CAM', 'CAM', 'CAM', 'CDM', 'CDM', 'CM', 'CAM', 'CM', 'CDM', 'CAM',
            # Additional positions - more variety for better similarity
            'CAM', 'CAM', 'CM', 'CDM', 'CDM', 'CM', 'CM', 'RW', 'CAM', 'CM'
        ],
        
        # Attacking Statistics
        'goals': [
            # Original 10 players
            7, 8, 3, 1, 2, 1, 4, 3, 2, 8,
            # Additional 10 players
            9, 11, 5, 1, 2, 3, 6, 12, 3, 4
        ],
        'assists': [
            # Original 10 players  
            18, 10, 4, 2, 9, 3, 9, 5, 1, 10,
            # Additional 10 players
            7, 8, 7, 1, 3, 4, 8, 7, 4, 6
        ],
        'shots_per_game': [
            # Original 10 players
            2.1, 2.8, 1.4, 0.5, 1.2, 0.8, 2.3, 1.9, 0.7, 2.5,
            # Additional 10 players
            2.4, 2.9, 1.8, 0.4, 0.6, 1.1, 1.5, 3.1, 1.6, 1.7
        ],
        'key_passes_per_game': [
            # Original 10 players
            3.2, 2.4, 1.2, 0.8, 1.6, 1.0, 2.1, 1.5, 0.6, 2.8,
            # Additional 10 players
            2.6, 2.2, 2.0, 0.5, 0.7, 1.2, 2.4, 2.3, 1.8, 1.9
        ],
        
        # Passing Statistics  
        'pass_accuracy': [
            # Original 10 players
            87.5, 82.1, 85.2, 89.3, 91.2, 88.7, 83.4, 84.6, 86.8, 88.9,
            # Additional 10 players
            89.1, 86.7, 90.4, 88.2, 89.8, 87.3, 91.5, 84.9, 85.1, 88.0
        ],
        'passes_per_game': [
            # Original 10 players
            67.8, 58.4, 45.6, 73.2, 89.1, 52.3, 49.7, 56.8, 48.9, 61.2,
            # Additional 10 players
            72.4, 64.1, 82.7, 65.3, 71.8, 58.2, 75.6, 52.1, 44.3, 59.7
        ],
        'long_passes_per_game': [
            # Original 10 players
            4.2, 3.8, 2.1, 5.6, 7.3, 4.1, 3.2, 2.9, 3.7, 4.0,
            # Additional 10 players
            3.9, 3.1, 6.2, 4.8, 5.4, 3.5, 5.8, 2.7, 2.4, 3.6
        ],
        
        # Defensive Statistics
        'tackles_per_game': [
            # Original 10 players
            1.2, 1.6, 2.1, 3.4, 2.8, 2.5, 0.9, 2.3, 3.1, 1.4,
            # Additional 10 players
            1.8, 1.3, 1.9, 3.2, 2.9, 2.7, 2.1, 0.8, 1.1, 2.2
        ],
        'interceptions_per_game': [
            # Original 10 players
            0.8, 1.2, 1.5, 2.1, 1.9, 1.7, 0.6, 1.8, 2.3, 1.0,
            # Additional 10 players
            1.4, 1.1, 1.6, 2.0, 1.8, 2.1, 1.5, 0.7, 0.9, 1.7
        ],
        
        # Physical Statistics
        'distance_covered_per_game': [
            # Original 10 players
            10.2, 10.8, 11.1, 11.5, 10.9, 10.3, 10.6, 11.3, 11.2, 10.7,
            # Additional 10 players
            10.4, 10.9, 10.8, 11.4, 11.1, 11.6, 10.5, 11.0, 10.3, 11.2
        ],
        'minutes_played': [
            # Original 10 players
            2340, 2567, 1890, 2456, 2678, 1567, 2123, 1987, 2234, 2456,
            # Additional 10 players
            2789, 2234, 2567, 2345, 2123, 1987, 2456, 2678, 1789, 2234
        ]
    }
    
    players_data = pd.DataFrame(sample_players)
    print(f"✅ Loaded {len(players_data)} players successfully")
    return players_data

def calculate_similarity_matrix():
    """
    Calculate cosine similarity between all players.
    
    Why cosine similarity?
    - Measures angle between vectors, not magnitude
    - Good for different scales (goals vs minutes played)
    - Values between -1 and 1 (easy to interpret)
    - Standard choice for content-based recommendations
    """
    global similarity_matrix, scaler
    
    if players_data is None:
        raise ValueError("No data loaded. Call load_sample_data() first.")
    
    # Select numerical features for similarity calculation
    feature_columns = [
        'goals', 'assists', 'shots_per_game', 'key_passes_per_game',
        'pass_accuracy', 'passes_per_game', 'long_passes_per_game',
        'tackles_per_game', 'interceptions_per_game', 'distance_covered_per_game'
    ]
    
    # Extract feature matrix
    features = players_data[feature_columns].values
    
    # Normalize features (important for fair comparison)
    # StandardScaler: mean=0, std=1 for each feature
    normalized_features = scaler.fit_transform(features)
    """
    We use StandardScaler: z = (x - μ) / std

    Why:
    Equal Contribution: Each feature contributes equally to similarity
    Scale Independence: Goals vs minutes_played treated fairly
    Standard Practice: Most common in ML literature
    Zero Mean: Centers data around origin
    Cosine Friendly: Perfect for cosine similarity calculations

    """
    
    # Calculate cosine similarity matrix
    similarity_matrix = cosine_similarity(normalized_features)
    
    print("✅ Similarity matrix calculated")
    return similarity_matrix

# API Endpoints

@app.route('/')
def health_check():
    """
    Health check endpoint - confirms API is running.
    Good practice for monitoring and debugging.
    """
    return jsonify({
        "message": "Premier League Midfielder Similarity Finder API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /": "Health check",
            "GET /players": "List all players",
            "GET /players/<player_id>": "Get specific player details",
            "GET /similar/<player_name>": "Find similar players",
            "POST /similar": "Find similar players with parameters"
        }
    })

@app.route('/players', methods=['GET'])
def get_all_players():
    """
    Get list of all available players.
    Useful for frontend dropdowns and data exploration.
    """
    try:
        if players_data is None:
            load_sample_data()
        
        # Convert to list of dictionaries for JSON response
        players_list = players_data[[
            'player_id', 'player_name', 'team', 'position'
        ]].to_dict('records')
        
        return jsonify({
            "success": True,
            "count": len(players_list),
            "players": players_list
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/players/<int:player_id>', methods=['GET'])
def get_player_details(player_id):
    """
    Get detailed statistics for a specific player.
    Shows all the features we use for similarity calculation.
    """
    try:
        if players_data is None:
            load_sample_data()
        
        # Find player by ID
        player = players_data[players_data['player_id'] == player_id]
        
        if player.empty:
            return jsonify({
                "success": False,
                "error": f"Player with ID {player_id} not found"
            }), 404
        
        # Convert to dictionary and format response
        player_data = player.iloc[0].to_dict()
        
        return jsonify({
            "success": True,
            "player": player_data
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/similar/<player_name>', methods=['GET'])
def find_similar_players(player_name):
    """
    Find players similar to the given player name.
    This is the core functionality of our recommendation system.
    """
    try:
        # Load data and calculate similarities if not done yet
        if players_data is None:
            load_sample_data()
        if similarity_matrix is None:
            calculate_similarity_matrix()
        
        # Get optional parameter for number of results
        top_n = request.args.get('top_n', default=5, type=int)
        
        # Find the target player
        target_player = players_data[
            players_data['player_name'].str.lower() == player_name.lower()
        ]
        
        if target_player.empty:
            return jsonify({
                "success": False,
                "error": f"Player '{player_name}' not found",
                "available_players": players_data['player_name'].tolist()
            }), 404
        
        # Get player index
        player_index = target_player.index[0]
        
        # Get similarity scores for this player
        similarity_scores = similarity_matrix[player_index]
        
        # Create list of (index, similarity_score) pairs
        player_similarities = list(enumerate(similarity_scores))
        
        # Sort by similarity (descending) and exclude the player themselves
        player_similarities.sort(key=lambda x: x[1], reverse=True)
        similar_players = player_similarities[1:top_n+1]  # Skip self (index 0)
        
        # Format results
        results = []
        for idx, similarity_score in similar_players:
            similar_player = players_data.iloc[idx]
            results.append({
                "player_id": int(similar_player['player_id']),
                "player_name": similar_player['player_name'],
                "team": similar_player['team'],
                "position": similar_player['position'],
                "similarity_score": round(float(similarity_score), 3),
                "key_stats": {
                    "goals": int(similar_player['goals']),
                    "assists": int(similar_player['assists']),
                    "pass_accuracy": float(similar_player['pass_accuracy']),
                    "tackles_per_game": float(similar_player['tackles_per_game'])
                }
            })
        
        return jsonify({
            "success": True,
            "target_player": {
                "name": target_player.iloc[0]['player_name'],
                "team": target_player.iloc[0]['team'],
                "position": target_player.iloc[0]['position']
            },
            "similar_players": results,
            "algorithm_info": {
                "method": "Cosine Similarity",
                "features_used": 10,
                "normalization": "StandardScaler"
            }
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/similar', methods=['POST'])
def find_similar_players_post():
    """
    Find similar players using POST request with JSON parameters.
    Allows more flexible querying with additional parameters.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'player_name' not in data:
            return jsonify({
                "success": False,
                "error": "JSON body with 'player_name' field is required"
            }), 400
        
        player_name = data['player_name']
        top_n = data.get('top_n', 5)
        position_filter = data.get('position_filter', None)  # Future feature
        
        # Use the existing GET logic
        # In a larger app, we'd extract this to a shared function
        return find_similar_players(player_name)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Initialize data when the app starts
def initialize_app():
    """
    Initialize the application with data and calculations.
    This runs once when the server starts.
    """
    print("🚀 Initializing Premier League Midfielder Similarity Finder...")
    print("📊 Loading player data...")
    load_sample_data()
    print("🔧 Calculating similarity matrix...")
    calculate_similarity_matrix()
    print("✅ Application ready!")

if __name__ == '__main__':
    # Initialize the application
    initialize_app()
    
    print("\n" + "="*50)
    print("🌟 Premier League Midfielder Similarity Finder")
    print("="*50)
    print("📍 Server: http://localhost:5000")
    print("📋 Available endpoints:")
    print("   GET  /                     - API info")
    print("   GET  /players              - List all players")
    print("   GET  /players/<id>         - Player details")
    print("   GET  /similar/<name>       - Find similar players")
    print("   POST /similar              - Find similar (JSON)")
    print("="*50)
    
    # Run the Flask development server
    app.run(
        debug=True,      # Auto-reload on code changes
        host='0.0.0.0',  # Accept connections from any IP
        port=5000        # Standard Flask port
    )