# Student Clustering Project - New Architecture

## 📁 Project Structure Overview

```
Student_Clustering_Project(US)/
│
├── 📂 backend/                          # Backend API Server
│   ├── 📂 app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI/Flask entry point
│   │   ├── config.py                    # Configuration settings
│   │   └── 📂 routes/
│   │       ├── __init__.py
│   │       ├── clustering.py            # Clustering API endpoints
│   │       ├── upload.py                # File upload endpoints
│   │       └── results.py               # Results retrieval endpoints
│   │
│   ├── 📂 ml_models/                    # ML Pipeline (UNCHANGED)
│   │   ├── __init__.py
│   │   ├── preprocessing.py             # Text cleaning & normalization
│   │   ├── feature_engineering.py       # Skill extraction & TF-IDF
│   │   ├── clustering.py                # KMeans, Hierarchical, DBSCAN
│   │   ├── evaluation.py                # Silhouette, Davies-Bouldin scores
│   │   └── visualization.py             # PCA plots & charts
│   │
│   ├── 📂 data/
│   │   ├── resume_dataset.csv
│   │   └── processed_data/
│   │
│   ├── 📂 output/                       # Generated results
│   │   ├── clustering_comparison.png
│   │   ├── kmeans_clusters.png
│   │   ├── evaluation_report.txt
│   │   └── ...other outputs
│   │
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
├── 📂 frontend/                         # React/Vue Frontend App
│   ├── 📂 public/
│   │   └── index.html
│   │
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── UploadForm.jsx
│   │   │   ├── ClusteringResults.jsx
│   │   │   ├── Visualizations.jsx
│   │   │   └── Navigation.jsx
│   │   │
│   │   ├── 📂 pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Upload.jsx
│   │   │   ├── Results.jsx
│   │   │   └── About.jsx
│   │   │
│   │   ├── 📂 services/
│   │   │   └── api.js                   # API service layer
│   │   │
│   │   ├── 📂 styles/
│   │   │   └── App.css
│   │   │
│   │   ├── App.jsx
│   │   └── index.js
│   │
│   ├── package.json
│   ├── .env
│   └── README.md
│
├── 📂 legacy/                           # ⚠️ SAFE BACKUP - Original Streamlit Version
│   ├── README.md                        # Original project documentation
│   ├── main.py                          # Original Streamlit entry point
│   ├── streamlit_app.py                 # Streamlit application
│   ├── requirements.txt                 # Original dependencies
│   └── 📂 src/
│       ├── preprocessing.py
│       ├── feature_engineering.py
│       ├── clustering.py
│       ├── evaluation.py
│       ├── visualization.py
│       └── ...original code files
│
├── 📂 docs/
│   ├── API_DOCUMENTATION.md             # Backend API specs
│   ├── FRONTEND_SETUP.md                # Frontend setup guide
│   ├── BACKEND_SETUP.md                 # Backend setup guide
│   ├── MIGRATION_GUIDE.md               # How to migrate from legacy
│   └── ARCHITECTURE.md                  # System architecture details
│
├── docker-compose.yml                   # Run both backend & frontend
├── .gitignore
├── .env.example
└── README.md                            # Main project documentation
```

---

## 🔄 Architecture Flow

### New Architecture (Frontend-Backend Separated)

```
┌─────────────────────────────────────────┐
│      FRONTEND (React/Vue)               │
│  - Upload Form                          │
│  - Dashboard                            │
│  - Results Visualization                │
└────────────────┬────────────────────────┘
                 │
                 │ HTTP/REST API Calls
                 │
┌────────────────▼────────────────────────┐
│    BACKEND (FastAPI/Flask)              │
│  - /api/upload        (POST)            │
│  - /api/cluster       (POST)            │
│  - /api/results       (GET)             │
│  - /api/visualize     (GET)             │
└────────────────┬────────────────────────┘
                 │
                 │ Uses (Unchanged)
                 │
┌────────────────▼────────────────────────┐
│    ML Pipeline (Scikit-learn)           │
│  1. Preprocessing                       │
│  2. Feature Engineering                 │
│  3. Clustering (KMeans/DBSCAN/etc)     │
│  4. Evaluation                          │
│  5. Visualization                       │
└─────────────────────────────────────────┘
```

---

## 💾 Legacy Version (Streamlit - Safe Backup)

**Location**: `./legacy/`

### When to Use Legacy:
- ✅ If new frontend has issues
- ✅ For quick prototyping
- ✅ As a fallback during development

### Run Legacy Version:
```bash
cd legacy
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 🚀 Getting Started

### Option 1: Run New Architecture (Recommended)

**Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm start
```

**Or use Docker:**
```bash
docker-compose up
```

### Option 2: Run Legacy Streamlit Version

```bash
cd legacy
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js / Vue.js + Tailwind CSS |
| **Backend** | FastAPI / Flask + Uvicorn |
| **ML Engine** | Scikit-learn, Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib |
| **Containerization** | Docker & Docker Compose |

---

## 🔧 Migration Status

- ✅ Project structure reorganized
- ✅ Legacy version backed up in `/legacy/`
- ⏳ Backend API endpoints (in progress)
- ⏳ Frontend components (in progress)
- ⏳ Docker setup (in progress)

---

## 📝 Notes

- **ML Models**: Completely unchanged - same algorithms and performance
- **Safety**: Original Streamlit version preserved in `/legacy/`
- **Flexibility**: Switch between new and old versions anytime
- **Scalability**: New architecture supports easier scaling and deployment
