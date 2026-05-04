"""
Evaluation module for comparing clustering algorithms.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import warnings
warnings.filterwarnings('ignore')


def calculate_silhouette_score(X, labels):
    """Calculate silhouette score for clustering results."""
    # Filter out noise points (label -1)
    if -1 in labels:
        mask = labels != -1
        if len(np.unique(labels[mask])) < 2:
            return 0
        return silhouette_score(X[mask], labels[mask])
    else:
        if len(np.unique(labels)) < 2:
            return 0
        return silhouette_score(X, labels)


def calculate_davies_bouldin_score(X, labels):
    """Calculate Davies-Bouldin score for clustering results."""
    # Filter out noise points (label -1)
    if -1 in labels:
        mask = labels != -1
        if len(np.unique(labels[mask])) < 2:
            return float('inf')
        return davies_bouldin_score(X[mask], labels[mask])
    else:
        if len(np.unique(labels)) < 2:
            return float('inf')
        return davies_bouldin_score(X, labels)


def calculate_calinski_harabasz_score(X, labels):
    """Calculate Calinski-Harabasz score for clustering results."""
    # Filter out noise points (label -1)
    if -1 in labels:
        mask = labels != -1
        if len(np.unique(labels[mask])) < 2:
            return 0
        return calinski_harabasz_score(X[mask], labels[mask])
    else:
        if len(np.unique(labels)) < 2:
            return 0
        return calinski_harabasz_score(X, labels)


def evaluate_clustering(X, labels, algorithm_name):
    """Evaluate clustering results using multiple metrics."""
    print(f"Evaluating {algorithm_name} clustering...")
    
    # Calculate metrics
    silhouette = calculate_silhouette_score(X, labels)
    davies_bouldin = calculate_davies_bouldin_score(X, labels)
    calinski_harabasz = calculate_calinski_harabasz_score(X, labels)
    
    # Calculate cluster statistics
    n_clusters = len(np.unique(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    
    # Calculate noise percentage
    noise_percentage = (n_noise / len(labels)) * 100 if len(labels) > 0 else 0
    
    evaluation = {
        'algorithm': algorithm_name,
        'n_clusters': n_clusters,
        'n_noise': n_noise,
        'noise_percentage': noise_percentage,
        'silhouette_score': silhouette,
        'davies_bouldin_score': davies_bouldin,
        'calinski_harabasz_score': calinski_harabasz
    }
    
    print(f"  Silhouette Score: {silhouette:.3f}")
    print(f"  Davies-Bouldin Score: {davies_bouldin:.3f}")
    print(f"  Calinski-Harabasz Score: {calinski_harabasz:.1f}")
    
    return evaluation


def compare_algorithms(X, clustering_results):
    """Compare multiple clustering algorithms."""
    print("\n" + "="*50)
    print("CLUSTERING ALGORITHM COMPARISON")
    print("="*50)
    
    evaluations = []
    
    for algorithm, labels in clustering_results.items():
        evaluation = evaluate_clustering(X, labels, algorithm)
        evaluations.append(evaluation)
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame(evaluations)
    
    print("\nComparison Summary:")
    print(comparison_df.round(3))
    
    return comparison_df


def select_best_algorithm(comparison_df, primary_metric='silhouette_score'):
    """Select the best clustering algorithm based on evaluation metrics."""
    print(f"\nSelecting best algorithm based on {primary_metric}...")
    
    # For silhouette score, higher is better
    if primary_metric == 'silhouette_score':
        best_idx = comparison_df[primary_metric].idxmax()
    # For Davies-Bouldin score, lower is better
    elif primary_metric == 'davies_bouldin_score':
        best_idx = comparison_df[primary_metric].idxmin()
    # For Calinski-Harabasz score, higher is better
    elif primary_metric == 'calinski_harabasz_score':
        best_idx = comparison_df[primary_metric].idxmax()
    else:
        best_idx = comparison_df[primary_metric].idxmax()
    
    best_algorithm = comparison_df.loc[best_idx, 'algorithm']
    best_score = comparison_df.loc[best_idx, primary_metric]
    
    print(f"Best algorithm: {best_algorithm}")
    print(f"Best {primary_metric}: {best_score:.3f}")
    
    return best_algorithm


def print_detailed_comparison(comparison_df):
    """Print detailed comparison of clustering algorithms."""
    print("\n" + "="*60)
    print("DETAILED CLUSTERING COMPARISON")
    print("="*60)
    
    metrics = ['silhouette_score', 'davies_bouldin_score', 'calinski_harabasz_score']
    
    for metric in metrics:
        print(f"\n{metric.replace('_', ' ').title()}:")
        
        if metric == 'silhouette_score' or metric == 'calinski_harabasz_score':
            # Higher is better
            sorted_df = comparison_df.sort_values(metric, ascending=False)
            symbol = "↑"
        else:
            # Lower is better
            sorted_df = comparison_df.sort_values(metric, ascending=True)
            symbol = "↓"
        
        for idx, row in sorted_df.iterrows():
            algorithm = row['algorithm']
            score = row[metric]
            print(f"  {algorithm}: {score:.3f} {symbol}")
    
    print("\nAlgorithm Rankings:")
    rankings = {}
    
    # Rank by each metric
    for metric in metrics:
        if metric == 'silhouette_score' or metric == 'calinski_harabasz_score':
            sorted_df = comparison_df.sort_values(metric, ascending=False)
        else:
            sorted_df = comparison_df.sort_values(metric, ascending=True)
        
        for rank, (idx, row) in enumerate(sorted_df.iterrows(), 1):
            algorithm = row['algorithm']
            if algorithm not in rankings:
                rankings[algorithm] = []
            rankings[algorithm].append(rank)
    
    # Calculate average rank
    avg_rankings = {}
    for algorithm, ranks in rankings.items():
        avg_rankings[algorithm] = np.mean(ranks)
    
    print("\nAverage Ranking (lower is better):")
    for algorithm, avg_rank in sorted(avg_rankings.items(), key=lambda x: x[1]):
        print(f"  {algorithm}: {avg_rank:.1f}")


def analyze_cluster_stability(X, algorithm, n_runs=10):
    """Analyze the stability of clustering algorithm over multiple runs."""
    print(f"\nAnalyzing stability of {algorithm}...")
    
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    all_labels = []
    
    for run in range(n_runs):
        if algorithm == 'kmeans':
            clustering = KMeans(n_clusters=5, random_state=run, n_init=10)
        elif algorithm == 'hierarchical':
            clustering = AgglomerativeClustering(n_clusters=5)
        elif algorithm == 'dbscan':
            clustering = DBSCAN(eps=0.8, min_samples=5)
        else:
            continue
        
        labels = clustering.fit_predict(X_scaled)
        all_labels.append(labels)
    
    # Calculate stability metrics
    stability_scores = []
    for i in range(n_runs):
        for j in range(i+1, n_runs):
            # Calculate Adjusted Rand Index between runs
            from sklearn.metrics import adjusted_rand_score
            ari = adjusted_rand_score(all_labels[i], all_labels[j])
            stability_scores.append(ari)
    
    avg_stability = np.mean(stability_scores)
    std_stability = np.std(stability_scores)
    
    print(f"  Average stability: {avg_stability:.3f}")
    print(f"  Stability std: {std_stability:.3f}")
    
    return avg_stability, std_stability
