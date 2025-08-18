"""
Machine learning model for player similarity calculation.
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from src.data_loader import get_feature_columns


class PlayerSimilarityModel:
    """
    A machine learning model for calculating player similarity using cosine similarity.
    """
    
    def __init__(self):
        """Initialize the model with a StandardScaler."""
        self.scaler = StandardScaler()
        self.similarity_matrix = None
        self.players_data = None
        self.is_trained = False
        
    def train(self, players_data):
        """
        Train the similarity model on player data.
        
        Args:
            players_data (pd.DataFrame): DataFrame containing player statistics
            
        Returns:
            np.ndarray: Cosine similarity matrix
            
        Why cosine similarity?
        - Measures angle between vectors, not magnitude
        - Good for different scales (goals vs minutes played)
        - Values between -1 and 1 (easy to interpret)
        - Standard choice for content-based recommendations
        """
        if players_data is None or len(players_data) == 0:
            raise ValueError("No data provided for training. Please load player data first.")
        
        self.players_data = players_data
        
        # Get feature columns for similarity calculation
        feature_columns = get_feature_columns()
        
        # Validate that all required columns exist
        missing_columns = [col for col in feature_columns if col not in players_data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Extract feature matrix
        features = players_data[feature_columns].values
        
        # Check for any NaN values
        if np.isnan(features).any():
            raise ValueError("Feature matrix contains NaN values. Please clean your data first.")
        
        # Normalize features (important for fair comparison)
        normalized_features = self.scaler.fit_transform(features)
        
        # Calculate cosine similarity matrix
        self.similarity_matrix = cosine_similarity(normalized_features)
        self.is_trained = True
        
        print("✅ Similarity matrix calculated using only real FBref statistics")
        print(f"📊 Model trained on {len(players_data)} players using {len(feature_columns)} features")
        
        return self.similarity_matrix
    
    def get_similar_players(self, player_index, top_n=5):
        """
        Get the most similar players to a given player.
        
        Args:
            player_index (int): Index of the target player
            top_n (int): Number of similar players to return
            
        Returns:
            list: List of tuples (player_index, similarity_score)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
            
        if player_index >= len(self.similarity_matrix):
            raise ValueError(f"Player index {player_index} out of range. Max index: {len(self.similarity_matrix) - 1}")
        
        # Get similarity scores for the target player
        player_similarities = self.similarity_matrix[player_index]
        
        # Get indices sorted by similarity (excluding the player themselves)
        similar_indices = np.argsort(player_similarities)[::-1]
        
        # Remove the player themselves (similarity = 1.0)
        similar_indices = similar_indices[similar_indices != player_index]
        
        # Get top N similar players with their scores
        top_similar = []
        for i in range(min(top_n, len(similar_indices))):
            idx = similar_indices[i]
            score = player_similarities[idx]
            top_similar.append((idx, score))
        
        return top_similar
    
    def get_player_by_name(self, player_name):
        """
        Find a player by name and return their index and data.
        
        Args:
            player_name (str): Name of the player to find
            
        Returns:
            tuple: (player_index, player_data) or (None, None) if not found
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Find player by exact name match
        matches = self.players_data[self.players_data['player_name'].str.lower() == player_name.lower()]
        
        if len(matches) == 0:
            # Try partial match
            matches = self.players_data[self.players_data['player_name'].str.contains(player_name, case=False, na=False)]
        
        if len(matches) == 0:
            return None, None
        
        # Return first match
        player_data = matches.iloc[0]
        player_index = matches.index[0]
        
        return player_index, player_data
    
    def get_model_info(self):
        """
        Get information about the trained model.
        
        Returns:
            dict: Model information including features and data stats
        """
        if not self.is_trained:
            return {"status": "not_trained"}
        
        feature_columns = get_feature_columns()
        
        return {
            "status": "trained",
            "num_players": len(self.players_data),
            "num_features": len(feature_columns),
            "features": feature_columns,
            "algorithm": "Cosine Similarity",
            "normalization": "StandardScaler",
            "matrix_shape": self.similarity_matrix.shape
        }
