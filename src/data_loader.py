"""
Data loading and preprocessing module for Premier League midfielder data.
"""
import pandas as pd
import numpy as np


def load_real_data():
    """
    Load REAL Premier League midfielder data from the downloaded CSV file.
    
    Returns:
        pd.DataFrame: Cleaned midfielder data with calculated features
        
    Real data benefits:
    - 245+ actual Premier League midfielders
    - Real statistics from FBref.com
    - More accurate similarity recommendations
    - 2023-24 season data
    """
    try:
        # Load the full Premier League data with npxG+xAG stats
        print("📊 Loading full Premier League data with npxG+xAG...")
        df = pd.read_csv('data/premier_league_data_converted.csv', skiprows=1)  # Skip header row
        
        # Rename columns based on the actual structure
        df.columns = [
            'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', 'MP', 'Starts', 'Min', '90s',
            'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'xG', 'npxG', 'xAG', 
            'npxG+xAG', 'PrgC', 'PrgP', 'PrgR', 'Gls_per_90', 'Ast_per_90', 'G+A_per_90', 
            'G-PK_per_90', 'G+A-PK_per_90', 'xG_per_90', 'xAG_per_90', 'xG+xAG_per_90', 
            'npxG_per_90', 'npxG+xAG_per_90', 'Matches'
        ]
        
        # Filter for midfielders only
        df = df[df['Pos'].str.contains('MF', na=False)]
        
        print(f"✅ Loaded {len(df)} midfielders with npxG+xAG data!")
        
        # Clean and prepare the data
        df = df.dropna(subset=['Player', 'npxG+xAG_per_90'])  # Remove rows with missing essential data
        
        # Convert numeric columns (including progressive stats)
        numeric_columns = ['Age', 'Min', 'Gls', 'Ast', 'npxG+xAG_per_90', 'Gls_per_90', 'Ast_per_90', 'PrgC', 'PrgP', 'PrgR']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any rows with NaN values after conversion
        df = df.dropna(subset=numeric_columns)
        
        # Filter out players with minimal playing time (less than 100 minutes)
        df = df[df['Min'] >= 100]
        
        # The per-90 stats are already calculated in the dataset
        # Just copy them to match our existing variable names
        df['goals_per_90'] = df['Gls_per_90']
        df['assists_per_90'] = df['Ast_per_90']
        df['npxG_plus_xAG_per_90'] = df['npxG+xAG_per_90']  # This is our new feature!
        
        # Calculate progressive stats per 90 minutes
        df['progressive_carries_per_90'] = (df['PrgC'] / df['Min']) * 90
        df['progressive_passes_per_90'] = (df['PrgP'] / df['Min']) * 90
        df['progressive_receives_per_90'] = (df['PrgR'] / df['Min']) * 90
        
        # Add some realistic derived statistics for better similarity
        df['total_contributions'] = df['Gls'] + df['Ast']
        df['contributions_per_90'] = df['goals_per_90'] + df['assists_per_90']
        
        # Using only real statistics - no estimated values for similarity calculation
        
        # Assign player IDs
        df['player_id'] = range(1, len(df) + 1)
        
        # Reset index to ensure sequential indexing for similarity matrix
        df = df.reset_index(drop=True)
        
        # Rename columns to match existing code structure
        df = df.rename(columns={
            'Player': 'player_name',
            'Squad': 'team',
            'Pos': 'position',
            'Age': 'age',
            'Gls': 'goals',
            'Ast': 'assists',
            'Min': 'minutes_played'
        })
        
        print(f"📈 After filtering: {len(df)} midfielders with significant playing time")
        print(f"🎯 Teams represented: {df['team'].nunique()}")
        print(f"⚽ Position breakdown: {df['position'].value_counts().to_dict()}")
        
        print(f"✅ Loaded {len(df)} real players successfully")
        return df
        
    except FileNotFoundError:
        print("❌ premier_league_data_converted.csv not found!")
        print("📍 Please ensure the file exists in the 'data/' folder")
        raise FileNotFoundError("Required data file not found: data/premier_league_data_converted.csv")
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        raise Exception(f"Failed to load data: {str(e)}")


def get_feature_columns():
    """
    Get the list of feature columns used for similarity calculation.
    
    Returns:
        list: List of column names for ML features
    """
    return [
        'goals_per_90', 'assists_per_90',     # ✅ Real: Basic per-90 rates
        'npxG_plus_xAG_per_90',              # ✅ Real: Expected goals + assists per 90
        'progressive_carries_per_90',         # ✅ Real: Progressive carries per 90
        'progressive_passes_per_90',          # ✅ Real: Progressive passes per 90  
        'progressive_receives_per_90',        # ✅ Real: Progressive receives per 90
        'total_contributions'                # ✅ Real: Total goals + assists
    ]


# Note: This simplified version only loads high-quality real data.
# Removed fallback functions (load_basic_data, load_sample_data) for cleaner code.
# The app now focuses exclusively on real Premier League statistics.
