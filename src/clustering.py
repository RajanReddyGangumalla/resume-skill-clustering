"""
Clustering module for applying various clustering algorithms.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')


def kmeans_clustering(X, n_clusters=5, random_state=42):
    """Apply K-Means clustering."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = kmeans.fit_predict(X)
    return labels, kmeans


def hierarchical_clustering(X, n_clusters=5):
    """Apply Agglomerative Hierarchical clustering."""
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    labels = hierarchical.fit_predict(X)
    return labels, hierarchical


def dbscan_clustering(X, eps=0.5, min_samples=5):
    """Apply DBSCAN clustering."""
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X)
    return labels, dbscan


def apply_all_clustering(X, kmeans_k=5, hierarchical_k=5, dbscan_eps=0.8, dbscan_min_samples=5):
    """Apply all three clustering algorithms."""
    print("Applying clustering algorithms...")
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    results = {}
    
    # K-Means
    print("Running K-Means clustering...")
    kmeans_labels, kmeans_model = kmeans_clustering(X_scaled, n_clusters=kmeans_k)
    results['kmeans'] = kmeans_labels
    
    # Hierarchical
    print("Running Hierarchical clustering...")
    hierarchical_labels, hierarchical_model = hierarchical_clustering(X_scaled, n_clusters=hierarchical_k)
    results['hierarchical'] = hierarchical_labels
    
    # DBSCAN
    print("Running DBSCAN clustering...")
    dbscan_labels, dbscan_model = dbscan_clustering(X_scaled, eps=dbscan_eps, min_samples=dbscan_min_samples)
    results['dbscan'] = dbscan_labels
    
    # Print summary
    print("\nClustering Results Summary:")
    for algorithm, labels in results.items():
        n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        print(f"{algorithm.title()}: {n_clusters} clusters, {n_noise} noise points")
    
    return results


def optimize_kmeans(X, max_k=10):
    """Find optimal number of clusters for K-Means using elbow method."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    inertias = []
    silhouette_scores = []
    k_range = range(2, max_k + 1)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        inertias.append(kmeans.inertia_)
        
        if len(np.unique(labels)) > 1:
            silhouette_scores.append(silhouette_score(X_scaled, labels))
        else:
            silhouette_scores.append(0)
    
    return k_range, inertias, silhouette_scores


def optimize_dbscan(X, eps_range=None, min_samples_range=None):
    """Find optimal parameters for DBSCAN."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    if eps_range is None:
        eps_range = np.arange(0.3, 1.5, 0.1)
    if min_samples_range is None:
        min_samples_range = range(3, 11)
    
    best_score = -1
    best_params = {}
    results = []
    
    for eps in eps_range:
        for min_samples in min_samples_range:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            labels = dbscan.fit_predict(X_scaled)
            
            n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
            n_noise = list(labels).count(-1)
            
            # Calculate silhouette score (only if we have more than 1 cluster and not all noise)
            if n_clusters > 1 and n_noise < len(X) * 0.9:
                score = silhouette_score(X_scaled[labels != -1], labels[labels != -1])
            else:
                score = -1
            
            results.append({
                'eps': eps,
                'min_samples': min_samples,
                'n_clusters': n_clusters,
                'n_noise': n_noise,
                'silhouette_score': score
            })
            
            if score > best_score:
                best_score = score
                best_params = {'eps': eps, 'min_samples': min_samples}
    
    return results, best_params, best_score


def print_clustering_info(labels, algorithm_name):
    """Print information about clustering results."""
    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    print(f"\n{algorithm_name} Results:")
    print(f"  Number of clusters: {n_clusters}")
    print(f"  Number of noise points: {n_noise}")
    
    if n_clusters > 0:
        cluster_sizes = []
        for cluster_id in np.unique(labels):
            if cluster_id != -1:
                size = list(labels).count(cluster_id)
                cluster_sizes.append(size)
        
        print(f"  Average cluster size: {np.mean(cluster_sizes):.1f}")
        print(f"  Largest cluster: {max(cluster_sizes)}")
        print(f"  Smallest cluster: {min(cluster_sizes)}")
