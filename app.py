"""
Student Resume Clustering App
Upload your resume to find your skill cluster among students
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import warnings
import re
import io
import PyPDF2
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from src.feature_engineering import analyze_clusters
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="Resume Clustering",
    page_icon="📄",
    layout="wide"
)

# Dark theme UI design for better visibility
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles with dark background */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background: transparent;
    }
    
    /* Header with better contrast */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern metric cards with consistent sizing */
    .metric-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.15);
        transition: all 0.3s ease;
        margin: 0.8rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.25);
    }
    
    .metric-card h3 {
        font-size: 1.6rem;
        margin: 0;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
        line-height: 1.2;
        letter-spacing: -0.5px;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        white-space: nowrap;
    }
    
    /* Clean section headers for dark theme */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #ffffff;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #475569;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern result cards for dark theme */
    .result-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
        border: 1px solid #334155;
        transition: all 0.2s ease;
    }
    
    .result-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
        border-color: #6366f1;
    }
    
    .result-card h4 {
        color: #6366f1;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }
    
    .result-card h3 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean skill items for dark theme */
    .skill-item {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.6rem 0;
        border-left: 4px solid #6366f1;
        color: #e2e8f0;
        font-weight: 500;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .skill-item:hover {
        background: linear-gradient(135deg, #475569 0%, #64748b 100%);
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    
    /* Modern success box for dark theme */
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        font-family: 'Inter', sans-serif;
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .success-box h3 {
        font-size: 1.4rem;
        margin: 0 0 0.8rem 0;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    
    .success-box p {
        font-size: 1rem;
        margin: 0;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
        opacity: 0.95;
    }
    
    /* Modern warning box for dark theme */
    .warning-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.25);
        font-family: 'Inter', sans-serif;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Clean chart containers for dark theme */
    .js-plotly-plot .plotly {
        background: #1e293b !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        border: 1px solid #334155;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern widgets for dark theme */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid #475569 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.2s ease !important;
        background: #1e293b !important;
        color: #e2e8f0 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.25) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px rgba(99, 102, 241, 0.35) !important;
    }
    
    /* Modern file uploader for dark theme */
    .stFileUploader > div {
        border: 2px dashed #6366f1 !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        transition: all 0.3s ease !important;
        color: #e2e8f0 !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #8b5cf6 !important;
        background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Fix file uploader - hide all default text and create clean interface */
    .stFileUploader {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Hide all Streamlit default elements */
    .stFileUploader > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Hide the label completely */
    .stFileUploader label {
        display: none !important;
    }
    
    /* Hide all spans to prevent double text */
    .stFileUploader span {
        display: none !important;
    }
    
    /* Custom upload area */
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: #1e293b !important;
        border: 2px dashed #475569 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 0 !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #6366f1 !important;
    }
    
    /* Hide all default text elements */
    .stFileUploader [data-testid="stFileUploaderDropzone"] div:not(:last-child) {
        display: none !important;
    }
    
    /* Clean upload button */
    .stFileUploader button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        display: block !important;
        margin: 0 auto !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    .stFileUploader button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Hide help icon */
    .stFileUploader svg,
    .stFileUploader .st-emotion-cache-1l9m2vo,
    .stFileUploader .streamlit-optional {
        display: none !important;
    }
    
    /* Clean spacing */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    .stColumns > div {
        padding: 0.5rem !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)


def load_model():
    """Load the clustering model"""
    try:
        with open('clustering_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except:
        st.error("Model not found. Please run save_model.py first.")
        return None


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
            if dominant_score > 0.02:  # Lowered from 0.1 to 0.02
                cluster_profiles[cluster_id] = dominant_category
            else:
                # Fallback to descriptive names based on top skills
                top_skills = cluster_df.select_dtypes(include=[np.number]).mean().sort_values(ascending=False).head(3)
                if len(top_skills) > 0:
                    skill_names = [idx.replace('_', ' ').title() for idx in top_skills.index[:2]]
                    cluster_profiles[cluster_id] = f"{' & '.join(skill_names)} Specialist"
                else:
                    cluster_profiles[cluster_id] = f"Technical Professional {cluster_id}"
        else:
            cluster_profiles[cluster_id] = f"Technical Professional {cluster_id}"
    
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
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except:
        return None


def main():
    st.markdown('<h1 class="main-header">📄 Resume Skill Clustering</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find your skill cluster among students</p>', unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    if not model:
        return
    
    # Generate cluster profiles with meaningful names
    cluster_profiles = get_cluster_profiles(model)
    
    # Sidebar with better styling
    st.sidebar.markdown("## 📝 Upload Your Resume")
    
    # Input method
    input_method = st.sidebar.radio("Choose method:", ["📝 Text Input", "📁 File Upload"])
    
    resume_text = ""
    
    if input_method == "📝 Text Input":
        resume_text = st.sidebar.text_area("Paste your resume text:", height=200, placeholder="Copy and paste your complete resume here...")
    else:
        # File upload section
        st.sidebar.markdown("### 📁 Upload Resume")
        
        uploaded_file = st.sidebar.file_uploader(
            "Upload your resume file", 
            type=['txt', 'pdf'], 
            help="Supported formats: TXT, PDF"
        )
        
        if uploaded_file:
            st.sidebar.markdown("### 📄 File Status")
            if uploaded_file.type == "text/plain":
                resume_text = str(uploaded_file.read(), "utf-8")
                st.sidebar.success("✅ Text file loaded successfully")
                st.sidebar.info(f"📝 {uploaded_file.name}")
            elif uploaded_file.type == "application/pdf":
                resume_text = extract_pdf_text(uploaded_file)
                if resume_text:
                    st.sidebar.success("✅ PDF text extracted successfully")
                    st.sidebar.info(f"📄 {uploaded_file.name}")
                else:
                    st.sidebar.error("❌ Could not extract PDF text")
                    st.sidebar.info("💡 Try converting PDF to text file")
    
    # Analyze button
    if st.sidebar.button("Analyze", type="primary"):
        if resume_text:
            with st.spinner("Analyzing..."):
                # Clean and extract skills
                clean = clean_text(resume_text)
                user_skills = extract_skills(clean, model['skill_keywords'])
                
                # Create feature vector
                user_features = np.array([user_skills.get(skill, 0) for skill in model['feature_columns']])
                
                # Combine with base data
                base_features = model['df_with_skills'][model['feature_columns']].values
                combined = np.vstack([base_features, user_features])
                
                # Scale and cluster
                scaled = model['scaler'].transform(combined)
                labels = model['clustering_algorithm'].fit_predict(scaled)
                user_cluster = labels[-1]
                
                # Store results
                st.session_state.results = {
                    'skills': user_skills,
                    'cluster': user_cluster,
                    'features': user_features
                }
                
                st.success("Analysis complete!")
    
    # Show dataset info with better styling
    st.markdown('<h2 class="section-header">📊 Dataset Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{model['n_samples']:,}</h3>
            <p>Students</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{model['n_features']}</h3>
            <p>Skills</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        n_clusters = len(np.unique(model['cluster_labels']))
        st.markdown(f"""
        <div class="metric-card">
            <h3>{n_clusters}</h3>
            <p>Clusters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{model['best_algorithm'].title()}</h3>
            <p>Algorithm</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cluster distribution with better styling and meaningful names
    st.markdown('<h2 class="section-header">📈 Cluster Distribution</h2>', unsafe_allow_html=True)
    
    unique, counts = np.unique(model['cluster_labels'], return_counts=True)
    
    # Create bar chart with modern gradient colors and meaningful cluster names
    fig = go.Figure()
    
    # Get meaningful names for clusters
    cluster_names = [cluster_profiles.get(i, f"Cluster {i}") for i in unique]
    
    fig.add_trace(go.Bar(
        x=cluster_names, 
        y=counts,
        marker=dict(
            color='#6366f1',
            line=dict(color='#8b5cf6', width=2)
        ),
        text=counts,
        textposition='auto',
        textfont=dict(color='white', size=12),
        hovertemplate='<b>%{x}</b><br>Students: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Students per Cluster",
            x=0.5,
            font=dict(size=16, color='#ffffff', family='Inter')
        ),
        xaxis_title="Cluster",
        yaxis_title="Number of Students",
        plot_bgcolor='#0f172a',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0', family='Inter'),
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    # Add dark grid lines
    fig.update_yaxes(showgrid=True, gridcolor='#334155', gridwidth=1)
    fig.update_xaxes(showgrid=False)
    
    st.plotly_chart(fig, width='stretch')
    
    # Show results if available
    if 'results' in st.session_state:
        results = st.session_state.results
        
        st.markdown('<h2 class="section-header">🎯 Your Analysis Results</h2>', unsafe_allow_html=True)
        
        # Results metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cluster_name = cluster_profiles.get(results['cluster'], f"Cluster {results['cluster']}")
            st.markdown(f"""
            <div class="result-card">
                <h4 style="color: #667eea; margin: 0 0 0.5rem 0;">Your Profile</h4>
                <h3 style="margin: 0; color: #2c3e50; font-size: 1.2rem;">{cluster_name}</h3>
                <p style="margin: 0.3rem 0 0 0; color: #7f8c8d; font-size: 0.8rem;">Cluster {results['cluster']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            similar = len(model['df_with_skills'][
                model['df_with_skills'][f"{model['best_algorithm']}_cluster"] == results['cluster']
            ])
            st.markdown(f"""
            <div class="result-card">
                <h4 style="color: #667eea; margin: 0 0 0.5rem 0;">Similar Students</h4>
                <h3 style="margin: 0; color: #2c3e50;">{similar}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_skills = sum(results['skills'].values())
            st.markdown(f"""
            <div class="result-card">
                <h4 style="color: #667eea; margin: 0 0 0.5rem 0;">Skills Found</h4>
                <h3 style="margin: 0; color: #2c3e50;">{int(total_skills)}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Skills found with better styling
        st.markdown('<h3 style="color: #2c3e50; margin: 2rem 0 1rem 0;">🔍 Skills Found in Your Resume</h3>', unsafe_allow_html=True)
        
        found_skills = {k: v for k, v in results['skills'].items() if v > 0}
        
        if found_skills:
            for skill, score in sorted(found_skills.items(), key=lambda x: x[1], reverse=True)[:10]:
                skill_name = skill.replace('_', ' ').title()
                st.markdown(f"""
                <div class="skill-item">
                    <strong>{skill_name}</strong> - Score: {score:.2f}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ No technical skills detected. Try adding more specific skill keywords.</div>', unsafe_allow_html=True)
        
        # Visualization with better styling
        st.markdown('<h3 style="color: #2c3e50; margin: 2rem 0 1rem 0;">📊 Your Position in Skill Space</h3>', unsafe_allow_html=True)
        
        # PCA visualization
        base_pca = model['pca_coordinates']
        user_pca = model['pca'].transform(model['scaler'].transform(results['features'].reshape(1, -1)))
        
        fig = go.Figure()
        
        # Plot base clusters with better colors and meaningful names
        colors = px.colors.qualitative.Set1
        for cluster_id in np.unique(model['cluster_labels']):
            mask = model['cluster_labels'] == cluster_id
            color = colors[cluster_id % len(colors)]
            cluster_name = cluster_profiles.get(cluster_id, f"Cluster {cluster_id}")
            fig.add_trace(go.Scatter(
                x=base_pca[mask, 0],
                y=base_pca[mask, 1],
                mode='markers',
                name=cluster_name,
                marker=dict(size=6, color=color, opacity=0.7),
                hovertemplate=f'<b>{cluster_name}</b><br>PC1: %{{x:.2f}}<br>PC2: %{{y:.2f}}<extra></extra>'
            ))
        
        # Plot user with enhanced styling
        user_cluster_name = cluster_profiles.get(results['cluster'], f"Cluster {results['cluster']}")
        fig.add_trace(go.Scatter(
            x=[user_pca[0, 0]],
            y=[user_pca[0, 1]],
            mode='markers',
            name=f'You: {user_cluster_name}',
            marker=dict(color='red', size=20, symbol='star', line=dict(width=2, color='white')),
            hovertemplate=f'<b>You: {user_cluster_name}</b><br>PC1: %{{x:.2f}}<br>PC2: %{{y:.2f}}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Your Position in the Skill Cluster Map",
            xaxis_title=f"PC1 ({model['pca'].explained_variance_ratio_[0]:.1%} variance)",
            yaxis_title=f"PC2 ({model['pca'].explained_variance_ratio_[1]:.1%} variance)",
            height=500,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#1e293b',
            font=dict(color='#e2e8f0', family='Inter'),
            legend=dict(
                x=1.02,
                y=1,
                bgcolor='#1e293b',
                bordercolor='#334155',
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Success message with meaningful cluster name
        cluster_name = cluster_profiles.get(results['cluster'], f"Cluster {results['cluster']}")
        st.markdown(f"""
        <div class="success-box">
            <h3>🎉 Analysis Complete!</h3>
            <p>You've been identified as a <strong>{cluster_name}</strong> with {similar} similar students in your cluster.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
