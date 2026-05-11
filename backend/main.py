"""
FastAPI Backend for Resume Clustering Application
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
import pickle
import io
import PyPDF2
import re
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.feature_engineering import analyze_clusters

app = FastAPI(
    title="Resume Clustering API",
    description="API for clustering resumes based on skills",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://localhost:3005",
        "https://frontend-99yyvtr6u-rajans-projects-0668921c.vercel.app",
        "https://frontend-indol-one-55.vercel.app",
        "*"  # Allow all origins for now
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class DatasetInfo(BaseModel):
    n_samples: int
    n_features: int
    n_clusters: int
    best_algorithm: str

# Global variables to store model
model = None
cluster_profiles = None

def load_model():
    """Load the clustering model"""
    global model, cluster_profiles
    try:
        # Try to find the model file in the parent directory
        model_path = '../clustering_model.pkl'
        if not os.path.exists(model_path):
            # Fallback to absolute path
            model_path = '/Users/gangumallarajanreddy/Downloads/Student_Clustering_Project(US)/clustering_model.pkl'
        
        print(f"Loading model from: {model_path}")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        cluster_profiles = get_cluster_profiles(model)
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def get_cluster_profiles(model):
    """Generate meaningful cluster names based on dominant skills"""
    df = model['df_with_skills']
    cluster_col = f"{model['best_algorithm']}_cluster"
    
    # Define comprehensive skill categories for profiling
    skill_categories = {
        'Web Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'bootstrap', 'jquery'],
        'Data Scientist': ['python', 'machine_learning', 'deep_learning', 'tensorflow', 'pytorch', 'scikit_learn', 'pandas', 'numpy', 'matplotlib', 'seaborn'],
        'Backend Developer': ['java', 'python', 'sql', 'spring', 'django', 'flask', 'postgresql', 'mongodb', 'mysql', 'api'],
        'Mobile Developer': ['android', 'ios', 'react_native', 'flutter', 'kotlin', 'swift', 'mobile', 'xamarin'],
        'DevOps Engineer': ['aws', 'azure', 'docker', 'kubernetes', 'linux', 'jenkins', 'git', 'ci_cd', 'terraform', 'ansible'],
        'Business Analyst': ['excel', 'power_bi', 'tableau', 'sql', 'sap', 'salesforce', 'analytics', 'reporting'],
        'AI/ML Engineer': ['machine_learning', 'deep_learning', 'tensorflow', 'pytorch', 'keras', 'opencv', 'nlp', 'computer_vision'],
        'Full Stack Developer': ['javascript', 'python', 'react', 'node', 'sql', 'html', 'css', 'mongodb', 'express'],
        'Database Administrator': ['sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'database', 'nosql', 'redis'],
        'Cloud Architect': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'cloud', 'microservices'],
        'Software Engineer': ['java', 'python', 'c++', 'javascript', 'algorithms', 'data_structures', 'oop', 'testing'],
        'Frontend Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'typescript', 'sass', 'webpack'],
        'Data Engineer': ['python', 'sql', 'spark', 'hadoop', 'etl', 'data_pipeline', 'airflow', 'kafka'],
        'Security Engineer': ['security', 'cryptography', 'networking', 'penetration_testing', 'firewall', 'ssl', 'authentication'],
        'QA Engineer': ['testing', 'automation', 'selenium', 'junit', 'quality_assurance', 'bug_tracking', 'test_cases'],
        'Product Manager': ['product_management', 'agile', 'scrum', 'requirements', 'roadmap', 'stakeholder', 'analytics'],
        'System Administrator': ['linux', 'windows', 'networking', 'server', 'monitoring', 'backup', 'scripting'],
        'Game Developer': ['unity', 'unreal', 'c++', 'c#', 'game_development', 'graphics', 'animation', 'physics'],
        'Blockchain Developer': ['blockchain', 'solidity', 'ethereum', 'bitcoin', 'smart_contracts', 'web3', 'cryptocurrency'],
        'IoT Developer': ['iot', 'embedded', 'arduino', 'raspberry_pi', 'sensors', 'mqtt', 'edge_computing']
    }
    
    cluster_profiles = {}
    
    for cluster_id in sorted(df[cluster_col].unique()):
        if cluster_id == -1:  # Skip noise points
            continue
            
        cluster_df = df[df[cluster_col] == cluster_id]
        
        # Calculate category scores for this cluster
        category_scores = {}
        for category, skills in skill_categories.items():
            available_skills = [s for s in skills if s in cluster_df.columns]
            if available_skills:
                score = cluster_df[available_skills].mean().mean()
                category_scores[category] = score
        
        # Determine the dominant category with lower threshold
        if category_scores:
            dominant_category = max(category_scores, key=category_scores.get)
            dominant_score = category_scores[dominant_category]
            
            # Lower threshold to ensure more clusters get meaningful names
            if dominant_score > 0.01:  # Lowered from 0.02 to 0.01
                cluster_profiles[cluster_id] = dominant_category
            else:
                # Fallback to descriptive names based on top skills
                top_skills = cluster_df.select_dtypes(include=[np.number]).mean().sort_values(ascending=False).head(3)
                if len(top_skills) > 0:
                    skill_names = [idx.replace('_', ' ').title() for idx in top_skills.index[:2]]
                    cluster_profiles[cluster_id] = f"{' & '.join(skill_names)} Specialist"
                else:
                    # More descriptive fallback names
                    fallback_names = [
                        "Software Developer", "IT Professional", "Systems Engineer", 
                        "Technical Specialist", "Application Developer", "Systems Analyst",
                        "Technology Consultant", "Software Architect", "Engineering Professional"
                    ]
                    cluster_profiles[cluster_id] = fallback_names[cluster_id % len(fallback_names)]
        else:
            # More descriptive fallback names for empty category scores
            fallback_names = [
                "Software Developer", "IT Professional", "Systems Engineer", 
                "Technical Specialist", "Application Developer", "Systems Analyst",
                "Technology Consultant", "Software Architect", "Engineering Professional"
            ]
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
            score += text.count(keyword)
        if score > 0:
            skills[skill] = min(score / 5.0, 1.0)
    return skills

def extract_pdf_text(uploaded_file):
    """Extract PDF text"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except:
        return None

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    if not load_model():
        raise HTTPException(status_code=500, detail="Failed to load model")

@app.get("/")
async def root():
    return {"message": "Resume Clustering API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/api/reload-clusters")
async def reload_clusters():
    """Reload cluster profiles with new names"""
    global cluster_profiles
    try:
        if model:
            cluster_profiles = get_cluster_profiles(model)
            return {"status": "success", "message": "Cluster profiles reloaded", "clusters": cluster_profiles}
        else:
            raise HTTPException(status_code=500, detail="Model not loaded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload clusters: {str(e)}")

@app.get("/api/dataset-info", response_model=DatasetInfo)
async def get_dataset_info():
    """Get dataset information"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    n_clusters = len(np.unique(model['cluster_labels']))
    
    return DatasetInfo(
        n_samples=model['n_samples'],
        n_features=model['n_features'],
        n_clusters=n_clusters,
        best_algorithm=model['best_algorithm']
    )

@app.get("/api/cluster-distribution")
async def get_cluster_distribution():
    """Get cluster distribution data"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    unique, counts = np.unique(model['cluster_labels'], return_counts=True)
    
    # Get meaningful names for clusters
    cluster_names = [cluster_profiles.get(i, f"Cluster {i}") for i in unique]
    
    distribution = []
    for i, (cluster_id, count, name) in enumerate(zip(unique, counts, cluster_names)):
        distribution.append({
            "cluster_id": int(cluster_id),
            "cluster_name": name,
            "count": int(count)
        })
    
    return {"distribution": distribution}

@app.get("/api/clusters-visualization")
async def get_clusters_visualization():
    """Get PCA coordinates for visualization"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Prepare data for visualization
    base_pca = model['pca_coordinates']
    cluster_labels = model['cluster_labels']
    
    visualization_data = []
    for i, (x, y) in enumerate(base_pca):
        cluster_id = int(cluster_labels[i])
        cluster_name = cluster_profiles.get(cluster_id, f"Cluster {cluster_id}")
        
        visualization_data.append({
            "x": float(x),
            "y": float(y),
            "cluster_id": cluster_id,
            "cluster_name": cluster_name,
            "is_user": False
        })
    
    return {"data": visualization_data}

def get_meaningful_cluster_name(cluster_id, cluster_df):
    """Get meaningful cluster name for a given cluster"""
    # Define comprehensive skill categories for profiling
    skill_categories = {
        'Web Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'bootstrap', 'jquery'],
        'Data Scientist': ['python', 'machine_learning', 'deep_learning', 'tensorflow', 'pytorch', 'scikit_learn', 'pandas', 'numpy', 'matplotlib', 'seaborn'],
        'Backend Developer': ['java', 'python', 'sql', 'spring', 'django', 'flask', 'postgresql', 'mongodb', 'mysql', 'api'],
        'Mobile Developer': ['android', 'ios', 'react_native', 'flutter', 'kotlin', 'swift', 'mobile', 'xamarin'],
        'DevOps Engineer': ['aws', 'azure', 'docker', 'kubernetes', 'linux', 'jenkins', 'git', 'ci_cd', 'terraform', 'ansible'],
        'Business Analyst': ['excel', 'power_bi', 'tableau', 'sql', 'sap', 'salesforce', 'analytics', 'reporting'],
        'AI/ML Engineer': ['machine_learning', 'deep_learning', 'tensorflow', 'pytorch', 'keras', 'opencv', 'nlp', 'computer_vision'],
        'Full Stack Developer': ['javascript', 'python', 'react', 'node', 'sql', 'html', 'css', 'mongodb', 'express'],
        'Database Administrator': ['sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'database', 'nosql', 'redis'],
        'Cloud Architect': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'cloud', 'microservices'],
        'Software Engineer': ['java', 'python', 'c++', 'javascript', 'algorithms', 'data_structures', 'oop', 'testing'],
        'Frontend Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'typescript', 'sass', 'webpack'],
        'Data Engineer': ['python', 'sql', 'spark', 'hadoop', 'etl', 'data_pipeline', 'airflow', 'kafka'],
        'Security Engineer': ['security', 'cryptography', 'networking', 'penetration_testing', 'firewall', 'ssl', 'authentication'],
        'QA Engineer': ['testing', 'automation', 'selenium', 'junit', 'quality_assurance', 'bug_tracking', 'test_cases'],
        'Product Manager': ['product_management', 'agile', 'scrum', 'requirements', 'roadmap', 'stakeholder', 'analytics'],
        'System Administrator': ['linux', 'windows', 'networking', 'server', 'monitoring', 'backup', 'scripting'],
        'Game Developer': ['unity', 'unreal', 'c++', 'c#', 'game_development', 'graphics', 'animation', 'physics'],
        'Blockchain Developer': ['blockchain', 'solidity', 'ethereum', 'bitcoin', 'smart_contracts', 'web3', 'cryptocurrency'],
        'IoT Developer': ['iot', 'embedded', 'arduino', 'raspberry_pi', 'sensors', 'mqtt', 'edge_computing']
    }
    
    # Calculate category scores for this cluster
    category_scores = {}
    for category, skills in skill_categories.items():
        available_skills = [s for s in skills if s in cluster_df.columns]
        if available_skills:
            score = cluster_df[available_skills].mean().mean()
            category_scores[category] = score
    
    # Determine the dominant category with lower threshold
    if category_scores:
        dominant_category = max(category_scores, key=category_scores.get)
        dominant_score = category_scores[dominant_category]
        
        # Lower threshold to ensure more clusters get meaningful names
        if dominant_score > 0.01:  # Lowered from 0.02 to 0.01
            return dominant_category
        else:
            # Fallback to descriptive names based on top skills
            top_skills = cluster_df.select_dtypes(include=[np.number]).mean().sort_values(ascending=False).head(3)
            if len(top_skills) > 0:
                skill_names = [idx.replace('_', ' ').title() for idx in top_skills.index[:2]]
                return f"{' & '.join(skill_names)} Specialist"
            else:
                # More descriptive fallback names
                fallback_names = [
                    "Software Developer", "IT Professional", "Systems Engineer", 
                    "Technical Specialist", "Application Developer", "Systems Analyst",
                    "Technology Consultant", "Software Architect", "Engineering Professional"
                ]
                return fallback_names[cluster_id % len(fallback_names)]
    else:
        # More descriptive fallback names for empty category scores
        fallback_names = [
            "Software Developer", "IT Professional", "Systems Engineer", 
            "Technical Specialist", "Application Developer", "Systems Analyst",
            "Technology Consultant", "Software Architect", "Engineering Professional"
        ]
        return fallback_names[cluster_id % len(fallback_names)]

@app.post("/api/pca-visualization")
async def get_pca_visualization_with_user(request: TextAnalysisRequest):
    """Get PCA coordinates including user position"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Process user text
        clean = clean_text(request.text)
        user_skills = extract_skills(clean, model['skill_keywords'])
        
        # Get user features
        user_features = np.array([user_skills.get(skill, 0) for skill in model['feature_columns']])
        
        # Transform user features using the same PCA
        user_pca = model['pca'].transform(model['scaler'].transform(user_features.reshape(1, -1)))
        
        # Get base PCA coordinates for all students
        base_pca = model['pca_coordinates']
        cluster_labels = model['cluster_labels']
        df = model['df_with_skills']
        cluster_col = f"{model['best_algorithm']}_cluster"
        
        visualization_data = []
        
        # Add all student points with meaningful names
        for i, (x, y) in enumerate(base_pca):
            cluster_id = int(cluster_labels[i])
            cluster_df = df[df[cluster_col] == cluster_id]
            cluster_name = get_meaningful_cluster_name(cluster_id, cluster_df)
            visualization_data.append({
                "x": float(x),
                "y": float(y),
                "cluster_id": cluster_id,
                "cluster_name": cluster_name,
                "is_user": False
            })
        
        # Add user point with meaningful name
        user_cluster = model['clustering_algorithm'].fit_predict(
            model['scaler'].transform(np.vstack([model['df_with_skills'][model['feature_columns']].values, user_features]))
        )[-1]
        
        user_cluster_df = df[df[cluster_col] == user_cluster]
        user_cluster_name = get_meaningful_cluster_name(user_cluster, user_cluster_df)
        
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

@app.post("/api/analyze-text", response_model=ClusterResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analyze resume text"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Clean and extract skills
        clean = clean_text(request.text)
        user_skills = extract_skills(clean, model['skill_keywords'])
        
        # Create feature vector
        user_features = np.array([user_skills.get(skill, 0) for skill in model['feature_columns']])
        
        # Combine with base data
        base_features = model['df_with_skills'][model['feature_columns']].values
        combined = np.vstack([base_features, user_features])
        
        # Scale and cluster
        scaled = model['scaler'].transform(combined)
        labels = model['clustering_algorithm'].fit_predict(scaled)
        user_cluster = int(labels[-1])
        
        # Get PCA coordinates
        user_pca = model['pca'].transform(model['scaler'].transform(user_features.reshape(1, -1)))
        
        # Count similar students
        similar = len(model['df_with_skills'][
            model['df_with_skills'][f"{model['best_algorithm']}_cluster"] == user_cluster
        ])
        
        cluster_name = cluster_profiles.get(user_cluster, f"Cluster {user_cluster}")
        
        return ClusterResponse(
            cluster_id=int(user_cluster),
            cluster_name=cluster_name,
            skills=user_skills,
            similar_students=similar,
            total_skills=int(sum(user_skills.values())),
            pca_coordinates=[float(user_pca[0, 0]), float(user_pca[0, 1])],
            extracted_text=clean
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/analyze-file", response_model=ClusterResponse)
async def analyze_file(file: UploadFile = File(...)):
    """Analyze uploaded resume file"""
    print(f"File upload received: {file.filename}, content_type: {file.content_type}")
    
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Check file type
    if file.content_type not in ["text/plain", "application/pdf"]:
        print(f"Unsupported file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Only TXT and PDF files are supported")
    
    try:
        # Extract text from file
        if file.content_type == "text/plain":
            content = await file.read()
            print(f"Text file content length: {len(content)}")
            text = content.decode("utf-8")
            print(f"Decoded text length: {len(text)}")
        elif file.content_type == "application/pdf":
            content = await file.read()
            print(f"PDF file content length: {len(content)}")
            text = extract_pdf_text(content)
            if not text:
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        print(f"Extracted text preview: {text[:200]}...")
        
        # Analyze the extracted text
        request = TextAnalysisRequest(text=text)
        return await analyze_text(request)
    
    except Exception as e:
        print(f"File processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
