"""
Save the trained clustering model to PKL file
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Import our modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing import load_dataset, identify_resume_column, preprocess_resumes, clean_text, remove_stopwords
from feature_engineering import create_feature_matrix, extract_skills, SKILL_KEYWORDS
from clustering import apply_all_clustering
from evaluation import compare_algorithms, select_best_algorithm


def save_clustering_model():
    """Train and save the clustering model"""
    
    print("Loading and preprocessing data...")
    
    # Load dataset
    df = load_dataset('data/Resume_Data.csv')
    resume_col = identify_resume_column(df)
    df_processed = preprocess_resumes(df, resume_col)
    
    # Create feature matrix
    feature_df, df_with_skills = create_feature_matrix(df_processed)
    X = feature_df.values
    
    print("Applying clustering algorithms...")
    
    # Apply clustering
    clustering_results = apply_all_clustering(X, kmeans_k=5, hierarchical_k=5)
    
    # Add cluster labels to dataframe
    for algorithm, labels in clustering_results.items():
        df_with_skills[f'{algorithm}_cluster'] = labels
    
    # Evaluate and select best
    comparison_df = compare_algorithms(X, clustering_results)
    best_algorithm = select_best_algorithm(comparison_df)
    
    print(f"Best algorithm: {best_algorithm}")
    
    # Train the best algorithm on the full dataset
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    if best_algorithm == 'kmeans':
        n_clusters = 10  # Fixed to 10 clusters for better granularity
        final_clustering = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    elif best_algorithm == 'hierarchical':
        n_clusters = 12  # Fixed to 12 clusters for better granularity
        from sklearn.cluster import AgglomerativeClustering
        final_clustering = AgglomerativeClustering(n_clusters=n_clusters)
    else:  # dbscan
        final_clustering = DBSCAN(eps=0.8, min_samples=5)
    
    final_labels = final_clustering.fit_predict(X_scaled)
    
    # Create PCA for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Prepare model dictionary
    model_data = {
        'clustering_algorithm': final_clustering,
        'scaler': scaler,
        'pca': pca,
        'feature_columns': feature_df.columns.tolist(),
        'skill_keywords': SKILL_KEYWORDS,
        'best_algorithm': best_algorithm,
        'cluster_labels': final_labels,
        'df_with_skills': df_with_skills,
        'comparison_df': comparison_df,
        'pca_coordinates': X_pca,
        'n_features': X.shape[1],
        'n_samples': X.shape[0]
    }
    
    # Save the model
    print("Saving model to PKL file...")
    with open('clustering_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("✅ Model saved successfully as 'clustering_model.pkl'")
    
    # Save additional info
    model_info = {
        'best_algorithm': best_algorithm,
        'n_clusters': len(np.unique(final_labels)) - (1 if -1 in final_labels else 0),
        'n_samples': X.shape[0],
        'n_features': X.shape[1],
        'silhouette_score': comparison_df.loc[comparison_df['algorithm'] == best_algorithm, 'silhouette_score'].iloc[0]
    }
    
    with open('model_info.txt', 'w') as f:
        f.write("Clustering Model Information\n")
        f.write("=" * 30 + "\n")
        for key, value in model_info.items():
            f.write(f"{key}: {value}\n")
    
    print("✅ Model info saved as 'model_info.txt'")
    
    return model_data


if __name__ == "__main__":
    try:
        model = save_clustering_model()
        print("\n🎉 Model saving completed successfully!")
    except Exception as e:
        print(f"❌ Error saving model: {e}")
        import traceback
        traceback.print_exc()
