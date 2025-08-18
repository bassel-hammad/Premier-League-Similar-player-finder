# Premier League Midfielder Similarity Finder

A content-based recommendation system that finds similar Premier League midfielders using performance statistics and machine learning.

## 🎯 Project Overview

- **Objective**: Find similar midfielders based on playing style and performance
- **Method**: Content-based filtering with cosine similarity
- **Scope**: Premier League 2024-25 season midfielders only

## 🏗️ Architecture

### Clean Separation of Concerns:
- **`main.py`** - Entry point and launcher
- **`api.py`** - Flask API endpoints and HTTP handling
- **`src/model.py`** - Machine learning model and similarity calculations
- **`src/data_loader.py`** - Data loading and preprocessing
- **`streamlit_app.py`** - Frontend user interface

### Benefits:
- ✅ **Modular Design** - Each file has a single responsibility
- ✅ **Easy Testing** - Components can be tested independently
- ✅ **Maintainable** - Changes to ML logic don't affect API logic
- ✅ **Scalable** - Easy to add new features or swap components
- ✅ **Professional** - Follows software engineering best practices

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
python main.py
```

## 🛠️ Tech Stack

- **Backend**: Flask (Python) with clean architecture
- **ML**: scikit-learn, pandas, numpy
- **API**: RESTful endpoints with CORS support
- **Frontend**: Streamlit
- **Architecture**: Modular design with separation of concerns

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

## 📈 Development Status

- [x] Phase 1: Project setup with virtual environment
- [x] Phase 2: GitHub repository setup  
- [x] Phase 3: Clean modular architecture
- [x] Phase 4: Core similarity algorithm with real data
- [x] Phase 5: Real Premier League data integration
- [x] Phase 6: Streamlit frontend interface
- [ ] Phase 7: Docker containerization (optional)
- [ ] Phase 8: Production deployment (optional)

## 🔧 Development Notes

**Always activate your virtual environment before working:**
```bash
venv\Scripts\activate
```

**To run the application:**
```bash
python main.py
```

**To add new dependencies:**
```bash
pip install <package-name>
pip freeze > requirements.txt  # Update requirements
```

## 📁 Project Structure
```
premier-league-midfielder-similarity/
├── 📂 src/                     # Source code modules
│   ├── __init__.py            # Package initializer
│   ├── data_loader.py         # Data loading and preprocessing
│   └── model.py               # ML model and similarity calculations
├── 📂 data/                   # Data files (ignored by git)
│   ├── .gitkeep              # Preserves folder structure
│   ├── premier_league_data_converted.csv
│   └── Premier League.xlsx
├── 📂 docs/                   # Documentation and test results
│   └── manual_test_results.py
├── 📂 scripts/                # Development and utility scripts
│   ├── analyze_excel.py
│   ├── create_dataset.py
│   ├── enhanced_dataset_analysis.py
│   ├── fix_excel.py
│   └── test_api.py
├── 📂 venv/                   # Virtual environment (not in repo)
├── 🚀 main.py                 # Application entry point
├── 🔌 api.py                  # Flask API endpoints
├── 🎨 streamlit_app.py        # Frontend UI
├── 📋 requirements.txt        # Project dependencies
├── 🚫 .gitignore             # Git ignore rules
└── 📖 README.md              # Project documentation
```
```
premier-league-midfielder-similarity/
├── data/                    # Data files (ignored by git)
│   ├── .gitkeep            # Preserves folder structure
│   ├── premier_league_data_converted.csv
│   └── Premier League.xlsx
├── docs/                   # Documentation and test results
│   └── manual_test_results.py
├── 📂 scripts/                # Development and utility scripts
│   ├── analyze_excel.py       # Excel analysis helper
│   ├── create_dataset.py      # Dataset creation helper
│   ├── enhanced_dataset_analysis.py
│   ├── fix_excel.py          # Excel fixing utility
│   ├── test_api.py           # API testing script
│   └── app_old_monolithic.py # Old monolithic version (backup)
├── 📂 venv/                   # Virtual environment (not in repo)
├── 🚀 main.py                 # Application entry point  
├── 🔌 api.py                  # Flask API endpoints
├── 🎨 streamlit_app.py        # Frontend UI
├── 📋 requirements.txt        # Project dependencies
├── 🚫 .gitignore             # Git ignore rules
└── 📖 README.md              # Project documentation
```

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📄 License

This project is for educational purposes.

---
*Learning project focusing on ML-powered recommendations and API development*