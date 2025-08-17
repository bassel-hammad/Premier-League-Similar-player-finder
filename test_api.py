import requests
import json

BASE_URL = "http://localhost:5000"

def test_all_endpoints():
    """
    Comprehensive API testing to validate our similarity algorithm
    """
    print("🧪 Testing Premier League Midfielder Similarity API")
    print("="*60)
    
    try:
        # Test 1: Health Check
        print("\n1. Testing Health Check...")
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()['message']}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Make sure Flask app is running!")
        print("Run: python app.py")
        return
    
    # Test 2: Get All Players
    print("\n2. Testing Get All Players...")
    response = requests.get(f"{BASE_URL}/players")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Player Count: {data['count']}")
    print(f"First Player: {data['players'][0]['player_name']}")
    
    # Test 3: Get Specific Player
    print("\n3. Testing Get Player Details...")
    response = requests.get(f"{BASE_URL}/players/1")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Player: {data['player']['player_name']}")
    print(f"Goals: {data['player']['goals']}, Assists: {data['player']['assists']}")
    
    # Test 4: Similarity Search
    print("\n4. Testing Similarity Search...")
    response = requests.get(f"{BASE_URL}/similar/Kevin De Bruyne")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Target: {data['target_player']['name']}")
    print("Similar Players:")
    for player in data['similar_players']:
        print(f"  - {player['player_name']}: {player['similarity_score']}")
    
    # Test 5: POST Request
    print("\n5. Testing POST Request...")
    post_data = {"player_name": "Bruno Fernandes", "top_n": 3}
    response = requests.post(f"{BASE_URL}/similar", json=post_data)
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Similar to Bruno: {[p['player_name'] for p in data['similar_players']]}")
    
    # Test 6: Error Handling
    print("\n6. Testing Error Handling...")
    response = requests.get(f"{BASE_URL}/similar/NonExistentPlayer")
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json()['error']}")

if __name__ == "__main__":
    test_all_endpoints()