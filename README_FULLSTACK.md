# Resume Skill Clustering - Full Stack Application

A modern full-stack web application for clustering resumes based on technical skills, built with React and FastAPI.

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python
- **ML Processing**: Scikit-learn, Pandas, NumPy
- **File Processing**: PyPDF2 for PDF text extraction
- **API Documentation**: Auto-generated Swagger docs

### Frontend (React)
- **Framework**: React 18 with TypeScript
- **Styling**: TailwindCSS with custom dark theme
- **Animations**: Framer Motion
- **Charts**: Custom visualization components
- **File Upload**: React Dropzone
- **Notifications**: React Hot Toast

## 📁 Project Structure

```
Student_Clustering_Project(US)/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── clustering_model.pkl # Pre-trained ML model
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx         # Main application
│   │   └── index.tsx       # Entry point
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # TailwindCSS config
├── src/                    # Original ML code
├── data/                   # Dataset files
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/api/health`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   
   The application will be available at `http://localhost:3000`

## 📡 API Endpoints

### Core Endpoints
- `GET /api/health` - Health check
- `GET /api/dataset-info` - Dataset statistics
- `GET /api/cluster-distribution` - Cluster distribution data
- `GET /api/clusters-visualization` - PCA coordinates for visualization

### Analysis Endpoints
- `POST /api/analyze-text` - Analyze resume text
- `POST /api/analyze-file` - Analyze uploaded file (PDF/TXT)

### Request/Response Examples

#### Analyze Text
```bash
curl -X POST "http://localhost:8000/api/analyze-text" \
     -H "Content-Type: application/json" \
     -d '{"text": "Experienced Python developer with machine learning skills..."}'
```

#### Analyze File
```bash
curl -X POST "http://localhost:8000/api/analyze-file" \
     -F "file=@resume.pdf"
```

## 🎨 Features

### Frontend Features
- **Modern UI**: Dark theme with glassmorphism effects
- **Responsive Design**: Works on desktop and mobile
- **File Upload**: Drag-and-drop PDF/TXT file upload
- **Text Input**: Direct text input with character counter
- **Real-time Analysis**: Instant skill extraction and clustering
- **Interactive Visualizations**: Cluster distribution charts
- **Detailed Results**: Skill analysis with proficiency levels
- **Smooth Animations**: Framer Motion animations throughout

### Backend Features
- **RESTful API**: Clean, documented API endpoints
- **File Processing**: PDF text extraction and parsing
- **ML Integration**: Skill extraction and clustering algorithms
- **Error Handling**: Comprehensive error responses
- **CORS Support**: Cross-origin requests enabled
- **Async Processing**: FastAPI's async capabilities

## 🔧 Configuration

### Backend Configuration
- Edit `main.py` to modify:
  - CORS origins
  - File upload limits
  - ML model paths
  - API endpoints

### Frontend Configuration
- Edit `frontend/src/services/api.ts` to change:
  - API base URL
  - Timeout settings
  - Request headers

## 📊 ML Model

The application uses a pre-trained clustering model that:
- Extracts technical skills from resume text
- Maps skills to feature vectors
- Clusters students based on skill similarity
- Provides meaningful cluster names (Web Developer, Data Scientist, etc.)

### Supported Skills
- Programming languages (Python, JavaScript, Java, etc.)
- Frameworks (React, Django, Angular, etc.)
- Cloud platforms (AWS, Azure, GCP)
- Databases (SQL, MongoDB, PostgreSQL)
- DevOps tools (Docker, Kubernetes, Git)
- And many more...

## 🎯 Usage Examples

### 1. Upload Resume
1. Click "File Upload" tab
2. Drag and drop PDF/TXT file or click to browse
3. Wait for analysis to complete
4. View your cluster assignment and skills

### 2. Text Input
1. Click "Text Input" tab
2. Paste your resume text
3. Click "Analyze Resume"
4. Review your results

### 3. View Results
- **Cluster Assignment**: See which skill group you belong to
- **Similar Students**: Number of students in your cluster
- **Skills Found**: List of detected technical skills
- **Proficiency Levels**: Skill strength indicators
- **Position Map**: Your location in the skill space

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if Python 3.8+ is installed
- Ensure virtual environment is activated
- Verify all dependencies are installed
- Check if `clustering_model.pkl` exists in backend directory

**Frontend can't connect to backend:**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `main.py`
- Verify no firewall blocking the connection

**File upload fails:**
- Check file size (max 10MB)
- Ensure file is PDF or TXT format
- Verify PDF contains extractable text

**No skills detected:**
- Add more technical keywords to resume
- Ensure skills are clearly mentioned
- Check for spelling mistakes in skill names

### Development Tips

**Backend Development:**
- Use `uvicorn main.py --reload` for auto-reload
- Check API docs at `http://localhost:8000/docs`
- Use `print()` statements for debugging

**Frontend Development:**
- Use React DevTools for component inspection
- Check browser console for errors
- Use Network tab to monitor API calls

## 🚀 Deployment

### Backend Deployment (Production)
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment (Production)
```bash
# Build for production
npm run build

# Serve static files
npx serve -s build -l 3000
```

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY clustering_model.pkl .

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## 📝 Development Notes

### Adding New Skills
1. Update `skill_keywords` in the ML model
2. Retrain the clustering model
3. Update `skill_categories` in `main.py`
4. Restart the backend

### Customizing UI
1. Modify TailwindCSS classes in components
2. Update color scheme in `tailwind.config.js`
3. Add new animations with Framer Motion
4. Customize notification styles

### Extending API
1. Add new endpoints in `main.py`
2. Update TypeScript types in `frontend/src/types/`
3. Add corresponding service functions
4. Update frontend components

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation at `/docs`
