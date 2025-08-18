"""
Main launcher for the Premier League Midfielder Similarity Finder.
Run this file to start the API service.
"""

# Simply import and run the API
from api import app, initialize_service

if __name__ == '__main__':
    print("🚀 Starting Premier League Midfielder Similarity Finder...")
    
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
