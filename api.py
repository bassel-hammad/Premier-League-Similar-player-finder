"""
Flask API for Premier League Midfielder Similarity Finder.
Clean separation of concerns: this file only handles HTTP requests and responses.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import load_real_data
from src.model import PlayerSimilarityModel

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend integration

# Global model instance
similarity_model = PlayerSimilarityModel()


@app.route('/')
def health_check():
    """
    Health check endpoint - verify API is running.
    
    Returns:
        JSON response with API status and basic info
    """
    model_info = similarity_model.get_model_info()
    
    return jsonify({
        "status": "online",
        "service": "Premier League Midfielder Similarity Finder",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "model": model_info,
        "endpoints": {
            "health": "/",
            "players": "/players",
            "player_details": "/players/<id>",
            "similarity": "/similar/<name>",
            "similarity_post": "/similar"
        }
    })


@app.route('/players', methods=['GET'])
def get_all_players():
    """
    Get list of all available players.
    
    Returns:
        JSON response with player list
    """
    try:
        if not similarity_model.is_trained:
            return jsonify({
                "success": False,
                "error": "Model not trained. Please initialize the service."
            }), 500
        
        players_data = similarity_model.players_data
        
        # Convert to list of dictionaries for JSON response
        players_list = []
        for _, player in players_data.iterrows():
            players_list.append({
                "player_id": int(player['player_id']),
                "player_name": player['player_name'],
                "team": player['team'],
                "position": player['position'],
                "age": int(player['age']),
                "goals": int(player['goals']),
                "assists": int(player['assists'])
            })
        
        return jsonify({
            "success": True,
            "count": len(players_list),
            "players": players_list
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error retrieving players: {str(e)}"
        }), 500


@app.route('/players/<int:player_id>', methods=['GET'])
def get_player_details(player_id):
    """
    Get detailed statistics for a specific player.
    
    Args:
        player_id (int): Player ID
        
    Returns:
        JSON response with detailed player stats
    """
    try:
        if not similarity_model.is_trained:
            return jsonify({
                "success": False,
                "error": "Model not trained. Please initialize the service."
            }), 500
        
        players_data = similarity_model.players_data
        
        # Find player by ID
        player_row = players_data[players_data['player_id'] == player_id]
        
        if player_row.empty:
            return jsonify({
                "success": False,
                "error": f"Player with ID {player_id} not found"
            }), 404
        
        player = player_row.iloc[0]
        
        # Return detailed player information
        player_details = {
            "player_id": int(player['player_id']),
            "player_name": player['player_name'],
            "team": player['team'],
            "position": player['position'],
            "age": int(player['age']),
            "basic_stats": {
                "goals": int(player['goals']),
                "assists": int(player['assists']),
                "minutes_played": int(player['minutes_played']),
                "goals_per_90": round(float(player['goals_per_90']), 2),
                "assists_per_90": round(float(player['assists_per_90']), 2)
            },
            "advanced_stats": {
                "npxG_plus_xAG_per_90": round(float(player['npxG_plus_xAG_per_90']), 2),
                "progressive_carries_per_90": round(float(player['progressive_carries_per_90']), 2),
                "progressive_passes_per_90": round(float(player['progressive_passes_per_90']), 2),
                "progressive_receives_per_90": round(float(player['progressive_receives_per_90']), 2),
                "total_contributions": int(player['total_contributions'])
            }
        }
        
        return jsonify({
            "success": True,
            "player": player_details
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error retrieving player details: {str(e)}"
        }), 500


@app.route('/similar/<player_name>', methods=['GET'])
def find_similar_players(player_name):
    """
    Find players similar to the specified player.
    
    Args:
        player_name (str): Name of the target player
        
    Returns:
        JSON response with similar players list
    """
    try:
        if not similarity_model.is_trained:
            return jsonify({
                "success": False,
                "error": "Model not trained. Please initialize the service."
            }), 500
        
        # Get query parameters
        top_n = request.args.get('top_n', default=5, type=int)
        top_n = max(1, min(top_n, 20))  # Limit between 1 and 20
        
        # Find the target player
        player_index, target_player = similarity_model.get_player_by_name(player_name)
        
        if player_index is None:
            return jsonify({
                "success": False,
                "error": f"Player '{player_name}' not found. Please check the spelling."
            }), 404
        
        # Get similar players
        similar_players = similarity_model.get_similar_players(player_index, top_n)
        
        # Format results
        results = []
        players_data = similarity_model.players_data
        
        for similar_index, similarity_score in similar_players:
            similar_player = players_data.iloc[similar_index]
            results.append({
                "player_id": int(similar_player['player_id']),
                "player_name": similar_player['player_name'],
                "team": similar_player['team'],
                "position": similar_player['position'],
                "similarity_score": round(float(similarity_score), 3),
                "key_stats": {
                    "goals": int(similar_player['goals']),
                    "assists": int(similar_player['assists']),
                    "progressive_passes_per_90": float(similar_player['progressive_passes_per_90']),
                    "npxG_plus_xAG_per_90": float(similar_player['npxG_plus_xAG_per_90'])
                }
            })
        
        # Get target player info
        return jsonify({
            "success": True,
            "target_player": {
                "name": target_player['player_name'],
                "team": target_player['team'],
                "position": target_player['position']
            },
            "similar_players": results,
            "algorithm_info": {
                "method": "Cosine Similarity",
                "features_used": 6,  # Real features only: goals/90, assists/90, npxG+xAG/90, 3 progressive stats, total_contributions
                "normalization": "StandardScaler"
            }
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error finding similar players: {str(e)}"
        }), 500


@app.route('/similar', methods=['POST'])
def find_similar_players_post():
    """
    Find similar players using POST request with JSON body.
    
    Expected JSON:
    {
        "player_name": "Kevin De Bruyne",
        "top_n": 5
    }
    
    Returns:
        JSON response with similar players list
    """
    try:
        if not similarity_model.is_trained:
            return jsonify({
                "success": False,
                "error": "Model not trained. Please initialize the service."
            }), 500
        
        # Parse JSON request
        data = request.get_json()
        
        if not data or 'player_name' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'player_name' in request body"
            }), 400
        
        player_name = data['player_name']
        top_n = data.get('top_n', 5)
        top_n = max(1, min(top_n, 20))  # Limit between 1 and 20
        
        # Find the target player
        player_index, target_player = similarity_model.get_player_by_name(player_name)
        
        if player_index is None:
            return jsonify({
                "success": False,
                "error": f"Player '{player_name}' not found. Please check the spelling."
            }), 404
        
        # Get similar players
        similar_players = similarity_model.get_similar_players(player_index, top_n)
        
        # Format results
        results = []
        players_data = similarity_model.players_data
        
        for similar_index, similarity_score in similar_players:
            similar_player = players_data.iloc[similar_index]
            results.append({
                "player_id": int(similar_player['player_id']),
                "player_name": similar_player['player_name'],
                "team": similar_player['team'],
                "position": similar_player['position'],
                "similarity_score": round(float(similarity_score), 3),
                "key_stats": {
                    "goals": int(similar_player['goals']),
                    "assists": int(similar_player['assists']),
                    "progressive_passes_per_90": float(similar_player['progressive_passes_per_90']),
                    "npxG_plus_xAG_per_90": float(similar_player['npxG_plus_xAG_per_90'])
                }
            })
        
        return jsonify({
            "success": True,
            "target_player": {
                "name": target_player['player_name'],
                "team": target_player['team'],
                "position": target_player['position']
            },
            "similar_players": results,
            "algorithm_info": {
                "method": "Cosine Similarity",
                "features_used": 6,
                "normalization": "StandardScaler"
            }
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error finding similar players: {str(e)}"
        }), 500


def initialize_service():
    """
    Initialize the similarity service by loading data and training the model.
    This runs once when the server starts.
    """
    try:
        print("🚀 Initializing Premier League Midfielder Similarity Finder...")
        print("📊 Loading player data...")
        
        # Load data
        players_data = load_real_data()
        
        print("🔧 Training similarity model...")
        
        # Train model
        similarity_model.train(players_data)
        
        print("✅ Service initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize service: {str(e)}")
        return False


if __name__ == '__main__':
    # Initialize the service
    if initialize_service():
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
            debug=True,
            host='0.0.0.0',
            port=5000
        )
    else:
        print("❌ Failed to start service due to initialization errors")
        exit(1)
