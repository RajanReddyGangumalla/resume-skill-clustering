import sys
import os
import json
import numpy as np
import pandas as pd
import pickle
import re
import io
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import PyPDF2

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Create FastAPI app
app = FastAPI()

# Data models
class TextAnalysisRequest(BaseModel):
    text: str

class ClusterResponse(BaseModel):
    cluster_id: int
    cluster_name: str
    skills: Dict[str, float]
    similar_students: int
    total_skills: int
    pca_coordinates: List[float]
    extracted_text: Optional[str] = None

# Global variables
model = None
cluster_profiles = None

def load_model():
    """Load the clustering model"""
    global model, cluster_profiles
    try:
        model_path = backend_path / 'clustering_model.pkl'
        if not model_path.exists():
            model_path = backend_path.parent / 'clustering_model.pkl'
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        cluster_profiles = get_cluster_profiles(model)
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def get_cluster_profiles(model_data):
    """Generate meaningful cluster names"""
    df = model_data['df_with_skills']
    cluster_col = f"{model_data['best_algorithm']}_cluster"
    
    skill_categories = {
        'Web Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask'],
        'Data Scientist': ['python', 'machine_learning', 'deep_learning', 'tensorflow', 'pytorch', 'scikit_learn', 'pandas', 'numpy'],
        'Backend Developer': ['java', 'python', 'sql', 'spring', 'django', 'flask', 'postgresql', 'mongodb', 'mysql'],
        'Mobile Developer': ['android', 'ios', 'react_native', 'flutter', 'kotlin', 'swift', 'mobile'],
        'DevOps Engineer': ['aws', 'azure', 'docker', 'kubernetes', 'linux', 'jenkins', 'git', 'ci_cd'],
        'Business Analyst': ['excel', 'power_bi', 'tableau', 'sql', 'sap', 'salesforce', 'analytics'],
        'AI/ML Engineer': ['machine_learning', 'deep_learning', 'tensorflow', 'pytorch', 'keras', 'opencv'],
        'Full Stack Developer': ['javascript', 'python', 'react', 'node', 'sql', 'html', 'css'],
        'Data Engineer': ['python', 'sql', 'spark', 'hadoop', 'etl', 'data_pipeline', 'airflow'],
        'Software Engineer': ['java', 'python', 'c++', 'javascript', 'algorithms', 'data_structures'],
        'Frontend Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'typescript'],
        'Product Manager': ['product_management', 'agile', 'scrum', 'requirements', 'roadmap'],
        'Security Engineer': ['security', 'cryptography', 'networking', 'penetration_testing'],
        'QA Engineer': ['testing', 'automation', 'selenium', 'junit', 'quality_assurance']
    }
    
    cluster_profiles = {}
    
    for cluster_id in sorted(df[cluster_col].unique()):
        if cluster_id == -1:
            continue
            
        cluster_df = df[df[cluster_col] == cluster_id]
        
        category_scores = {}
        for category, skills in skill_categories.items():
            available_skills = [s for s in skills if s in cluster_df.columns]
            if available_skills:
                score = cluster_df[available_skills].mean().mean()
                category_scores[category] = score
        
        if category_scores:
            dominant_category = max(category_scores, key=category_scores.get)
            dominant_score = category_scores[dominant_category]
            
            if dominant_score > 0.01:
                cluster_profiles[cluster_id] = dominant_category
            else:
                top_skills = cluster_df.select_dtypes(include=[np.number]).mean().sort_values(ascending=False).head(3)
                if len(top_skills) > 0:
                    skill_names = [idx.replace('_', ' ').title() for idx in top_skills.index[:2]]
                    cluster_profiles[cluster_id] = f"{' & '.join(skill_names)} Specialist"
                else:
                    fallback_names = ["Software Developer", "IT Professional", "Systems Engineer"]
                    cluster_profiles[cluster_id] = fallback_names[cluster_id % len(fallback_names)]
    
    return cluster_profiles

def clean_text(text):
    """Clean text"""
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text, skill_keywords):
    """Extract skills"""
    skills = {}
    for skill, keywords in skill_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        if score > 0:
            skills[skill] = min(score / len(keywords), 1.0)
    return skills

def extract_pdf_text(content):
    """Extract text from PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except:
        return ""

# Load model on startup
if not load_model():
    print("Warning: Model failed to load")

@app.get("/")
async def root():
    return {"message": "Resume Clustering API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/analyze-text", response_model=ClusterResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analyze resume text"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        clean = clean_text(request.text)
        user_skills = extract_skills(clean, model['skill_keywords'])
        
        user_features = np.array([user_skills.get(skill, 0) for skill in model['feature_columns']])
        scaled = model['scaler'].transform(user_features.reshape(1, -1))
        labels = model['clustering_algorithm'].fit_predict(
            np.vstack([model['df_with_skills'][model['feature_columns']].values, user_features])
        )
        user_cluster = int(labels[-1])
        
        user_pca = model['pca'].transform(model['scaler'].transform(user_features.reshape(1, -1)))
        
        similar = len(model['df_with_skills'][
            model['df_with_skills'][f"{model['best_algorithm']}_cluster"] == user_cluster
        ])
        
        cluster_name = cluster_profiles.get(user_cluster, f"Cluster {user_cluster}")
        
        return ClusterResponse(
            cluster_id=user_cluster,
            cluster_name=cluster_name,
            skills=user_skills,
            similar_students=similar,
            total_skills=int(sum(user_skills.values())),
            pca_coordinates=[float(user_pca[0, 0]), float(user_pca[0, 1])],
            extracted_text=clean
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-file", response_model=ClusterResponse)
async def analyze_file(file: UploadFile = File(...)):
    """Analyze uploaded resume file"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if file.content_type not in ["text/plain", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Only TXT and PDF files are supported")
    
    try:
        if file.content_type == "text/plain":
            content = await file.read()
            text = content.decode("utf-8")
        elif file.content_type == "application/pdf":
            content = await file.read()
            text = extract_pdf_text(content)
            if not text:
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        request = TextAnalysisRequest(text=text)
        return await analyze_text(request)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@app.post("/pca-visualization")
async def get_pca_visualization_with_user(request: TextAnalysisRequest):
    """Get PCA coordinates including user position"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        clean = clean_text(request.text)
        user_skills = extract_skills(clean, model['skill_keywords'])
        user_features = np.array([user_skills.get(skill, 0) for skill in model['feature_columns']])
        user_pca = model['pca'].transform(model['scaler'].transform(user_features.reshape(1, -1)))
        
        base_pca = model['pca_coordinates']
        cluster_labels = model['cluster_labels']
        df = model['df_with_skills']
        cluster_col = f"{model['best_algorithm']}_cluster"
        
        visualization_data = []
        
        for i, (x, y) in enumerate(base_pca):
            cluster_id = int(cluster_labels[i])
            cluster_df = df[df[cluster_col] == cluster_id]
            cluster_name = cluster_profiles.get(cluster_id, f"Cluster {cluster_id}")
            visualization_data.append({
                "x": float(x),
                "y": float(y),
                "cluster_id": cluster_id,
                "cluster_name": cluster_name,
                "is_user": False
            })
        
        user_cluster = model['clustering_algorithm'].fit_predict(
            model['scaler'].transform(np.vstack([model['df_with_skills'][model['feature_columns']].values, user_features]))
        )[-1]
        
        user_cluster_df = df[df[cluster_col] == user_cluster]
        user_cluster_name = cluster_profiles.get(user_cluster, f"Cluster {user_cluster}")
        
        visualization_data.append({
            "x": float(user_pca[0, 0]),
            "y": float(user_pca[0, 1]),
            "cluster_id": int(user_cluster),
            "cluster_name": user_cluster_name,
            "is_user": True
        })
        
        return {"data": visualization_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PCA visualization failed: {str(e)}")

# Export for Vercel
app = app

import json

def handler(request):
    """
    Vercel serverless function handler
    """
    # Set proper headers to prevent download
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Health check endpoint
    if request.method == 'GET' and request.url.endswith('/health'):
        response_data = {
            "status": "healthy",
            "model_loaded": True,
            "message": "Resume Clustering API is running"
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }
    
    # Root endpoint
    if request.method == 'GET' and request.url.endswith('/'):
        response_data = {
            "message": "Resume Clustering API",
            "version": "1.0.0",
            "endpoints": [
                "/health",
                "/dataset-info",
                "/analyze-text",
                "/analyze-file",
                "/pca-visualization"
            ]
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }
    
    # Default response
    response_data = {
        "message": "Resume Clustering API",
        "status": "running",
        "available_endpoints": ["/health", "/"]
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(response_data)
    }
