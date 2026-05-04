"""
Feature engineering module for extracting skills from resumes.
"""

import re
import pandas as pd
import numpy as np


# Define comprehensive skill keywords
SKILL_KEYWORDS = {
    # Programming Languages
    'python': ['python', 'py'],
    'java': ['java'],
    'javascript': ['javascript', 'js'],
    'c++': ['c++', 'cpp'],
    'c#': ['c#', 'csharp', 'c sharp'],
    'php': ['php'],
    'ruby': ['ruby'],
    'go': ['go', 'golang'],
    'swift': ['swift'],
    'kotlin': ['kotlin'],
    'r': [' r ', 'r programming', 'r statistical'],
    'matlab': ['matlab'],
    'scala': ['scala'],
    
    # Web Development
    'html': ['html', 'html5'],
    'css': ['css', 'css3'],
    'react': ['react', 'reactjs', 'react.js'],
    'angular': ['angular', 'angularjs', 'angular.js'],
    'vue': ['vue', 'vuejs', 'vue.js'],
    'node': ['node', 'nodejs', 'node.js'],
    'express': ['express', 'expressjs', 'express.js'],
    'django': ['django'],
    'flask': ['flask'],
    'spring': ['spring', 'spring boot'],
    
    # Data Science & ML
    'machine_learning': ['machine learning', 'ml', 'machinelearning'],
    'deep_learning': ['deep learning', 'dl', 'deeplearning'],
    'data_science': ['data science', 'datascience', 'data scientist'],
    'tensorflow': ['tensorflow', 'tf'],
    'pytorch': ['pytorch', 'torch'],
    'scikit_learn': ['scikit-learn', 'sklearn', 'scikitlearn'],
    'keras': ['keras'],
    'pandas': ['pandas'],
    'numpy': ['numpy'],
    'matplotlib': ['matplotlib'],
    'seaborn': ['seaborn'],
    'opencv': ['opencv', 'cv'],
    
    # Database
    'sql': ['sql'],
    'mysql': ['mysql'],
    'postgresql': ['postgresql', 'postgres'],
    'mongodb': ['mongodb', 'mongo'],
    'oracle': ['oracle'],
    'sqlite': ['sqlite'],
    
    # Cloud & DevOps
    'aws': ['aws', 'amazon web services'],
    'azure': ['azure', 'microsoft azure'],
    'gcp': ['gcp', 'google cloud'],
    'docker': ['docker'],
    'kubernetes': ['kubernetes', 'k8s'],
    'linux': ['linux'],
    'ubuntu': ['ubuntu'],
    'windows': ['windows'],
    'macos': ['macos', 'os x'],
    
    # Mobile Development
    'android': ['android'],
    'ios': ['ios'],
    'react_native': ['react native', 'react-native'],
    'flutter': ['flutter'],
    
    # Other Technologies
    'git': ['git', 'github'],
    'rest_api': ['rest api', 'restful', 'api'],
    'graphql': ['graphql'],
    'microservices': ['microservices'],
    'agile': ['agile', 'scrum'],
    'jira': ['jira'],
    'slack': ['slack'],
    'trello': ['trello'],
    
    # Business & Analytics
    'excel': ['excel', 'microsoft excel'],
    'power_bi': ['power bi', 'powerbi'],
    'tableau': ['tableau'],
    'sap': ['sap'],
    'salesforce': ['salesforce'],
    'crm': ['crm'],
    
    # Testing
    'junit': ['junit'],
    'selenium': ['selenium'],
    'jest': ['jest'],
    'mocha': ['mocha'],
    'cypress': ['cypress']
}


def extract_skills(text, skill_keywords=SKILL_KEYWORDS):
    """Extract skills from text using keyword matching."""
    skills = {}
    
    for skill, keywords in skill_keywords.items():
        score = 0
        for keyword in keywords:
            # Count occurrences of keyword
            count = text.count(keyword)
            if count > 0:
                score += count
        
        # Normalize score (0-1 range)
        if score > 0:
            skills[skill] = min(score / 5.0, 1.0)  # Cap at 1.0
    
    return skills


def create_feature_matrix(df, text_column='cleaned_resume'):
    """Create a feature matrix with skill presence/absence."""
    print("Creating feature matrix...")
    
    # Extract skills for each resume
    skills_list = []
    for text in df[text_column]:
        skills = extract_skills(str(text))
        skills_list.append(skills)
    
    # Create feature dataframe
    feature_df = pd.DataFrame(skills_list)
    
    # Fill missing values with 0
    feature_df = feature_df.fillna(0)
    
    # Combine with original dataframe
    df_with_skills = pd.concat([df.reset_index(drop=True), feature_df], axis=1)
    
    print(f"Feature matrix created: {feature_df.shape}")
    print(f"Number of skills tracked: {len(SKILL_KEYWORDS)}")
    
    return feature_df, df_with_skills


def analyze_clusters(df, cluster_column):
    """Analyze the characteristics of each cluster."""
    print("Analyzing clusters...")
    
    # Define skill categories for analysis
    skill_categories = {
        'Programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift', 'kotlin', 'r', 'matlab', 'scala'],
        'Web Development': ['html', 'css', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring'],
        'Data Science': ['machine_learning', 'deep_learning', 'data_science', 'tensorflow', 'pytorch', 'scikit_learn', 'keras', 'pandas', 'numpy', 'matplotlib', 'seaborn'],
        'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sqlite'],
        'Cloud/DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'linux'],
        'Mobile': ['android', 'ios', 'react_native', 'flutter'],
        'Business': ['excel', 'power_bi', 'tableau', 'sap', 'salesforce', 'crm']
    }
    
    cluster_analysis = {}
    
    for cluster_id in sorted(df[cluster_column].unique()):
        if cluster_id == -1:  # Skip noise points in DBSCAN
            continue
            
        cluster_df = df[df[cluster_column] == cluster_id]
        cluster_size = len(cluster_df)
        
        # Calculate category scores
        category_scores = {}
        for category, skills in skill_categories.items():
            # Only include skills that exist in the dataframe
            available_skills = [s for s in skills if s in cluster_df.columns]
            if available_skills:
                score = cluster_df[available_skills].mean().mean()
                category_scores[category] = score
        
        # Determine dominant category
        if category_scores:
            dominant_category = max(category_scores, key=category_scores.get)
            dominant_score = category_scores[dominant_category]
        else:
            dominant_category = "Mixed"
            dominant_score = 0
        
        # Get top individual skills - only numeric columns
        skill_cols = [col for col in df.columns 
                      if col not in ['cleaned_resume', cluster_column] 
                      and pd.api.types.is_numeric_dtype(df[col])]
        available_skills = [s for s in skill_cols if s in cluster_df.columns]
        
        if available_skills:
            top_skills = cluster_df[available_skills].mean().sort_values(ascending=False).head(5)
        else:
            top_skills = pd.Series()
        
        cluster_analysis[cluster_id] = {
            'size': cluster_size,
            'percentage': (cluster_size / len(df)) * 100,
            'dominant_category': dominant_category,
            'category_score': dominant_score,
            'category_scores': category_scores,
            'top_skills': top_skills
        }
        
        print(f"\nCluster {cluster_id}: {cluster_size} students ({(cluster_size/len(df)*100):.1f}%)")
        print(f"  Dominant Profile: {dominant_category} (score: {dominant_score:.2f})")
        print(f"  Top Skills:")
        for skill, score in top_skills.items():
            print(f"    {skill}: {score:.3f}")
    
    return cluster_analysis


def print_skill_statistics(df):
    """Print statistics about skill distribution."""
    print("\n" + "="*50)
    print("SKILL DISTRIBUTION STATISTICS")
    print("="*50)
    
    skill_cols = [col for col in df.columns 
                  if col not in ['cleaned_resume'] 
                  and pd.api.types.is_numeric_dtype(df[col])]
    
    print(f"Total skills tracked: {len(skill_cols)}")
    
    # Most common skills
    skill_means = df[skill_cols].mean().sort_values(ascending=False)
    print("\nTop 10 Most Common Skills:")
    for skill, mean in skill_means.head(10).items():
        print(f"  {skill}: {mean:.3f}")
    
    # Least common skills
    print("\nTop 10 Least Common Skills:")
    for skill, mean in skill_means.tail(10).items():
        print(f"  {skill}: {mean:.3f}")
    
    print("="*50)
