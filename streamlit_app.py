import streamlit as st
import requests
import json
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Premier League Midfielder Finder",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        margin-bottom: 30px;
    }
    .player-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1f4e79;
    }
    .player-card h3 {
        color: #1f4e79 !important;
        margin-top: 0;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .player-card p {
        color: #333333 !important;
        margin: 5px 0;
    }
    .similarity-score {
        font-size: 24px;
        font-weight: bold;
        color: #28a745;
    }
    .stMetric > div > div > div > div {
        color: #1f4e79;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:5000"

# Helper Functions
@st.cache_data
def get_players():
    """Fetch all players from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/players")
        if response.status_code == 200:
            return response.json()["players"]
        else:
            st.error(f"Failed to fetch players: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API. Make sure Flask app is running!")
        st.info("Run: `python app.py` in your terminal")
        return []

@st.cache_data
def get_player_details(player_id):
    """Fetch detailed stats for a specific player"""
    try:
        response = requests.get(f"{API_BASE_URL}/players/{player_id}")
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return result["player"]
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def get_similar_players(player_name, top_n=5):
    """Find similar players"""
    try:
        # URL encode the player name
        encoded_name = requests.utils.quote(player_name)
        response = requests.get(f"{API_BASE_URL}/similar/{encoded_name}?top_n={top_n}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error finding similar players: {response.json().get('error', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">🏆 Premier League Midfielder Similarity Finder</h1>', unsafe_allow_html=True)
    st.markdown("### Discover midfielders with similar playing styles using machine learning!")
    st.markdown("---")
    
    # Sidebar for controls
    st.sidebar.header("🎯 Search Controls")
    
    # Get players
    players = get_players()
    
    if not players:
        st.warning("⚠️ No players available. Make sure the Flask API is running.")
        st.info("💡 **To start the API:**\n1. Open terminal\n2. Run: `python app.py`\n3. Refresh this page")
        return
    
    # Player selection
    player_names = [player["player_name"] for player in players]
    selected_player_name = st.sidebar.selectbox(
        "🎮 Choose a midfielder:",
        options=player_names,
        index=0,
        help="Select a Premier League midfielder to find similar players"
    )
    
    # Number of similar players
    top_n = st.sidebar.slider(
        "📊 Number of similar players:",
        min_value=3,
        max_value=10,
        value=5,
        help="How many similar players to show"
    )
    
    # Find similar button
    find_similar = st.sidebar.button(
        "🔍 Find Similar Players",
        type="primary",
        use_container_width=True
    )
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    # Selected player info
    with col1:
        st.subheader("🎯 Selected Player")
        
        # Always show selected player name first
        st.markdown(f"""
        <div class="player-card">
            <h3>{selected_player_name}</h3>
        """, unsafe_allow_html=True)
        
        selected_player = next((p for p in players if p["player_name"] == selected_player_name), None)
        
        if selected_player:
            # Show basic info from players list
            st.markdown(f"""
            <p><strong>Team:</strong> {selected_player['team']}</p>
            <p><strong>Position:</strong> {selected_player['position']}</p>
            <hr>
            """, unsafe_allow_html=True)
            
            # Try to get detailed player stats
            player_details = get_player_details(selected_player["player_id"])
            
            if player_details:
                # Add detailed stats if available
                try:
                    # Handle different possible field names and missing values
                    goals = player_details.get('goals', player_details.get('Gls', 'N/A'))
                    assists = player_details.get('assists', player_details.get('Ast', 'N/A'))
                    
                    # Handle minutes played
                    minutes = player_details.get('minutes_played', 
                             player_details.get('Min', 
                             player_details.get('minutes', 0)))
                    
                    # Show progressive stats instead of fake pass accuracy
                    prog_passes = player_details.get('progressive_passes_per_90', 'N/A')
                    
                    st.markdown(f"""
                    <p><strong>Goals:</strong> {goals}</p>
                    <p><strong>Assists:</strong> {assists}</p>
                    <p><strong>Progressive Passes/90:</strong> {prog_passes:.1f}</p>
                    <p><strong>Minutes Played:</strong> {minutes:,}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f"""
                    <p><em>Basic stats available</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    # Show error in expander for debugging
                    with st.expander("Debug Info"):
                        st.error(f"Stats parsing error: {e}")
                        st.json(player_details)
            else:
                st.markdown(f"""
                <p><em>Loading detailed stats...</em></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <p><strong>Error:</strong> Player not found in list</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Similar players results
    with col2:
        st.subheader("⚡ Similar Players")
        
        if find_similar:
            with st.spinner("🔄 Finding similar players..."):
                similarity_data = get_similar_players(selected_player_name, top_n)
                
                if similarity_data:
                    st.success(f"✅ Found {len(similarity_data['similar_players'])} similar players!")
                    
                    # Display algorithm info
                    with st.expander("🔬 Algorithm Details"):
                        algo_info = similarity_data.get('algorithm_info', {})
                        st.write(f"**Method:** {algo_info.get('method', 'N/A')}")
                        st.write(f"**Features Used:** {algo_info.get('features_used', 'N/A')}")
                        st.write(f"**Normalization:** {algo_info.get('normalization', 'N/A')}")
                    
                    # Display similar players
                    for i, player in enumerate(similarity_data['similar_players'], 1):
                        with st.container():
                            col_rank, col_info, col_score = st.columns([0.5, 2.5, 1])
                            
                            with col_rank:
                                st.markdown(f"### #{i}")
                            
                            with col_info:
                                st.markdown(f"""
                                **{player['player_name']}**  
                                {player['team']} • {player['position']}  
                                ⚽ {player['key_stats']['goals']} goals • 🎯 {player['key_stats']['assists']} assists
                                """)
                            
                            with col_score:
                                st.metric(
                                    "Similarity",
                                    f"{player['similarity_score']:.3f}",
                                    help="Cosine similarity score (0-1, higher is more similar)"
                                )
                            
                            st.markdown("---")
                else:
                    st.error("❌ Failed to get similarity results")
        else:
            st.info("👆 Click 'Find Similar Players' to see recommendations!")
    
    # Footer with dataset info
    st.markdown("---")
    st.markdown("### 📊 Dataset Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Players", len(players))
    with col2:
        positions = [p["position"] for p in players]
        unique_positions = len(set(positions))
        st.metric("Positions", unique_positions)
    with col3:
        teams = [p["team"] for p in players]
        unique_teams = len(set(teams))
        st.metric("Teams", unique_teams)

# Sidebar additional info
def show_sidebar_info():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    This app uses **cosine similarity** to find Premier League midfielders 
    with similar playing styles based on:
    
    - ⚽ Goals & Assists
    - 🎯 Passing accuracy & volume
    - 🛡️ Defensive actions
    - 🏃 Physical metrics
    
    **Algorithm:** Content-based filtering with StandardScaler normalization
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("🔗 **Tech Stack:**")
    st.sidebar.markdown("• Flask API")
    st.sidebar.markdown("• Scikit-learn ML")
    st.sidebar.markdown("• Streamlit Frontend")
    st.sidebar.markdown("• Python 3.12")

if __name__ == "__main__":
    main()
    show_sidebar_info()
