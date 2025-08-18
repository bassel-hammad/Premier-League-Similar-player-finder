# Fix the Excel file reading with proper header structure
import pandas as pd
import numpy as np

def fix_excel_reading():
    """
    Fix the Excel file reading to handle FBref's multi-row header structure
    """
    try:
        print("🔧 FIXING EXCEL FILE STRUCTURE")
        print("=" * 40)
        
        # Read with the first row as header (the actual column names)
        print("📊 Reading Excel file with proper header...")
        df = pd.read_excel('Premier League.xlsx', header=1)  # Use row 1 as header
        
        print(f"✅ Successfully loaded with proper headers!")
        print(f"📈 Total rows: {len(df)}")
        print(f"📊 Total columns: {len(df.columns)}")
        
        print("\n🏷️ ACTUAL COLUMN NAMES:")
        for i, col in enumerate(df.columns[:15], 1):  # Show first 15 columns
            print(f"   {i:2d}. {col}")
        if len(df.columns) > 15:
            print(f"   ... and {len(df.columns) - 15} more columns")
        
        print("\n📋 FIRST 5 PLAYERS:")
        # Show key columns
        key_cols = []
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in ['player', 'rk', 'pos', 'squad', 'age', 'gls', 'ast']):
                key_cols.append(col)
        
        if key_cols:
            print(df[key_cols[:8]].head().to_string())  # Show first 8 relevant columns
        else:
            print(df.iloc[:, :8].head().to_string())  # Show first 8 columns
        
        # Look for position column
        position_col = None
        for col in df.columns:
            if 'pos' in str(col).lower():
                position_col = col
                break
        
        if position_col:
            print(f"\n🎯 POSITION COLUMN FOUND: '{position_col}'")
            positions = df[position_col].value_counts().head(10)
            print("Top 10 positions:")
            print(positions.to_string())
            
            # Find midfielders
            midfield_positions = df[df[position_col].str.contains('MF|CM|CAM|CDM|DM', na=False, case=False)]
            print(f"\n⚽ MIDFIELDERS FOUND: {len(midfield_positions)} players")
            
        # Clean column names and save
        df.columns = df.columns.str.strip()  # Remove whitespace
        df.to_csv('premier_league_clean.csv', index=False)
        
        print(f"\n💾 SAVED CLEAN DATA: premier_league_clean.csv")
        
        return df, position_col
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None

def create_midfielder_dataset(df, position_col):
    """
    Filter for midfielders and prepare for similarity algorithm
    """
    if df is None or position_col is None:
        return None
    
    try:
        print("\n🎯 CREATING MIDFIELDER DATASET")
        print("=" * 35)
        
        # Filter for midfielders
        midfielders = df[df[position_col].str.contains('MF|CM|CAM|CDM|DM', na=False, case=False)]
        
        print(f"✅ Filtered {len(midfielders)} midfielders from {len(df)} total players")
        
        # Find relevant columns for similarity
        important_cols = {}
        
        # Map columns to our algorithm needs
        for col in df.columns:
            col_lower = str(col).lower()
            if 'player' in col_lower:
                important_cols['player_name'] = col
            elif col_lower == 'pos':
                important_cols['position'] = col
            elif col_lower == 'squad':
                important_cols['team'] = col
            elif col_lower == 'age':
                important_cols['age'] = col
            elif col_lower == 'gls':
                important_cols['goals'] = col
            elif col_lower == 'ast':
                important_cols['assists'] = col
            elif 'min' == col_lower:
                important_cols['minutes'] = col
        
        print("\n📊 MAPPED COLUMNS:")
        for purpose, col_name in important_cols.items():
            print(f"   {purpose:12s}: {col_name}")
        
        # Create clean midfielder dataset
        if len(important_cols) >= 4:  # At least player, position, team, and one stat
            clean_midfielders = midfielders[list(important_cols.values())].copy()
            clean_midfielders.columns = list(important_cols.keys())
            
            # Save midfielder dataset
            clean_midfielders.to_csv('midfielders_only.csv', index=False)
            
            print(f"\n💾 SAVED MIDFIELDER DATA: midfielders_only.csv")
            print(f"📈 {len(clean_midfielders)} midfielders ready for similarity algorithm")
            
            # Show sample
            print("\n📋 SAMPLE MIDFIELDERS:")
            print(clean_midfielders.head(10).to_string())
            
            return clean_midfielders
        else:
            print("❌ Could not find enough relevant columns")
            return None
            
    except Exception as e:
        print(f"❌ Error creating midfielder dataset: {str(e)}")
        return None

if __name__ == "__main__":
    # Fix Excel reading
    df, position_col = fix_excel_reading()
    
    # Create midfielder dataset
    if df is not None:
        midfielders = create_midfielder_dataset(df, position_col)
        
        if midfielders is not None:
            print("\n🚀 SUCCESS! Your real Premier League data is ready!")
            print("✅ midfielders_only.csv contains your cleaned midfielder data")
            print("🔄 Ready to update your app.py with real data!")
        else:
            print("⚠️ Could not create clean midfielder dataset")
    else:
        print("❌ Could not read Excel file properly")
