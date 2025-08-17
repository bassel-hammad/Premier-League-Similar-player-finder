# Check the downloaded Premier League Excel file
import pandas as pd
import numpy as np

def analyze_excel_file():
    """
    Analyze the downloaded Premier League Excel file
    """
    try:
        print("📊 ANALYZING YOUR DOWNLOADED PREMIER LEAGUE DATA")
        print("=" * 50)
        
        # Read the Excel file
        print("🔍 Loading Excel file...")
        df = pd.read_excel('Premier League.xlsx')
        
        print(f"✅ Successfully loaded Excel file!")
        print(f"📈 Total rows: {len(df)}")
        print(f"📊 Total columns: {len(df.columns)}")
        
        print("\n🏷️ COLUMN NAMES:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        print("\n📋 FIRST 5 ROWS:")
        print(df.head().to_string())
        
        print("\n🎯 DATA TYPES:")
        print(df.dtypes.to_string())
        
        print("\n🔍 MISSING VALUES:")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0].to_string())
        else:
            print("   ✅ No missing values found!")
        
        # Check for position column
        position_cols = [col for col in df.columns if 'pos' in col.lower() or 'position' in col.lower()]
        if position_cols:
            print(f"\n🎯 POSITION COLUMN FOUND: {position_cols[0]}")
            positions = df[position_cols[0]].value_counts()
            print("Position breakdown:")
            print(positions.to_string())
        
        # Check for midfielder-related positions
        midfield_positions = []
        for col in df.columns:
            if 'pos' in col.lower():
                unique_vals = df[col].unique()
                midfield_vals = [val for val in unique_vals if 
                               any(mid in str(val).upper() for mid in ['MF', 'CM', 'CAM', 'CDM', 'DM'])]
                if midfield_vals:
                    midfield_positions.extend(midfield_vals)
        
        if midfield_positions:
            print(f"\n⚽ MIDFIELDER POSITIONS FOUND: {set(midfield_positions)}")
        
        # Look for key statistical columns
        key_stats = ['goal', 'assist', 'pass', 'tackle', 'shot']
        found_stats = []
        
        for stat in key_stats:
            matching_cols = [col for col in df.columns if stat in col.lower()]
            if matching_cols:
                found_stats.extend(matching_cols)
        
        if found_stats:
            print(f"\n📈 KEY STATISTICS FOUND:")
            for stat in found_stats[:10]:  # Show first 10
                print(f"   • {stat}")
        
        # Save as CSV for easier processing
        df.to_csv('premier_league_data_converted.csv', index=False)
        print(f"\n💾 CONVERTED TO CSV: premier_league_data_converted.csv")
        
        return df
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Make sure the Excel file is not open in another program")
        print("2. Check if the file is in the correct folder")
        print("3. Verify the file is not corrupted")
        return None

def identify_midfielder_columns(df):
    """
    Help identify which columns we need for the similarity algorithm
    """
    if df is None:
        return
    
    print("\n🎯 RECOMMENDATIONS FOR YOUR SIMILARITY ALGORITHM:")
    print("=" * 50)
    
    # Suggest which columns to use
    column_suggestions = {
        'player_name': [col for col in df.columns if any(word in col.lower() for word in ['player', 'name'])],
        'position': [col for col in df.columns if any(word in col.lower() for word in ['pos', 'position'])],
        'goals': [col for col in df.columns if any(word in col.lower() for word in ['goal', 'gls'])],
        'assists': [col for col in df.columns if any(word in col.lower() for word in ['assist', 'ast'])],
        'passes': [col for col in df.columns if any(word in col.lower() for word in ['pass', 'pas'])],
        'tackles': [col for col in df.columns if any(word in col.lower() for word in ['tackle', 'tkl'])],
        'age': [col for col in df.columns if 'age' in col.lower()],
    }
    
    print("🔍 COLUMN MAPPING SUGGESTIONS:")
    for purpose, candidates in column_suggestions.items():
        if candidates:
            print(f"   {purpose:12s}: {candidates[0]} (from: {candidates})")
        else:
            print(f"   {purpose:12s}: ❌ Not found")
    
    return column_suggestions

if __name__ == "__main__":
    # Analyze the Excel file
    df = analyze_excel_file()
    
    # Get column suggestions
    suggestions = identify_midfielder_columns(df)
    
    print("\n🚀 NEXT STEPS:")
    print("1. ✅ Your data has been analyzed")
    print("2. 📊 CSV file created for easier processing")
    print("3. 🔄 I'll update your app.py to use this real data")
    print("4. 🎯 Filter for midfielders only")
    print("5. 🚀 Test with real Premier League players!")
