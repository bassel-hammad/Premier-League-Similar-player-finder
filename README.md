# Premier League Midfielder Similarity Finder

A content-based recommendation system that finds similar Premier League midfielders using performance statistics and machine learning.

## 🎯 Project Overview

- **Objective**: Find similar midfielders based on playing style and performance
- **Method**: Content-based filtering with cosine similarity
- **Scope**: Premier League 2024-25 season midfielders only

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **ML**: scikit-learn, pandas, numpy
- **API**: RESTful endpoints with CORS support
- **Testing**: Postman
- **Deployment**: Docker

## 📊 Features

- Find similar players based on performance metrics
- RESTful API for easy integration
- Normalized statistics for fair comparison
- Containerized deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/premier-league-midfielder-similarity.git
cd premier-league-midfielder-similarity
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run application**
```bash
python app.py
```

5. **Test the API**
- Visit: http://localhost:5000/
- Test endpoints with Postman or browser

### Deactivating Virtual Environment
```bash
deactivate
```

## 📋 API Endpoints

- `GET /` - Health check
- `GET /players` - List all midfielders  
- `GET /similar/<player_name>` - Find similar players

## 🧪 Testing

```bash
# Ensure virtual environment is active
# Test API endpoints
curl http://localhost:5000/
curl http://localhost:5000/players
```

## 📈 Development Phases

- [x] Phase 1: Project setup with virtual environment
- [x] Phase 2: GitHub repository setup
- [ ] Phase 3: Basic Flask application
- [ ] Phase 4: Core similarity algorithm
- [ ] Phase 5: Real data integration
- [ ] Phase 6: Docker containerization

## 🔧 Development Notes

**Always activate your virtual environment before working:**
```bash
venv\Scripts\activate
```

**To add new dependencies:**
```bash
pip install <package-name>
pip freeze > requirements.txt  # Update requirements
```

## 📁 Project Structure
```
premier-league-midfielder-similarity/
├── venv/                 # Virtual environment (not in repo)
├── app.py               # Flask application
├── requirements.txt     # Project dependencies
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── Dockerfile          # Container configuration (coming soon)
└── tests/              # Unit tests (coming soon)
```

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📄 License

This project is for educational purposes.

---
*Learning project focusing on ML-powered recommendations and API development*