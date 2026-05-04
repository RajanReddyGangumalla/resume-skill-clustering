# API Reference

## Module: preprocessing.py

### `load_resume_data(filepath)`
Load resume dataset from CSV file with automatic encoding detection.

```python
df = load_resume_data('data/raw/resume_dataset.csv')
```

**Parameters:**
- `filepath` (str): Path to CSV file

**Returns:**
- `pd.DataFrame`: Loaded data

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If no valid resume column found

---

### `clean_text(text)`
Clean and normalize resume text.

```python
cleaned = clean_text("Check out my Python & Java skills!")
# Output: "check out my python java skills"
```

**Parameters:**
- `text` (str): Raw resume text

**Returns:**
- `str`: Cleaned text

---

## Module: feature_engineering.py

### `extract_skills(resume_text, skill_dict)`
Extract skills from resume text using regex patterns.

```python
skills = extract_skills(resume_text, SKILLS_DICTIONARY)
# Output: {'python': True, 'java': True, 'react': False, ...}
```

**Parameters:**
- `resume_text` (str): Cleaned resume text
- `skill_dict` (dict): Skill vocabulary with patterns

**Returns:**
- `dict`: Binary skill presence indicators

---

### `create_feature_matrix(resumes, skill_dict)`
Create binary feature matrix from resume texts.

```python
X = create_feature_matrix(cleaned_resumes, SKILLS_DICTIONARY)
# Shape: (n_resumes, 40+)
```

**Parameters:**
- `resumes` (list): List of cleaned resume texts
- `skill_dict` (dict): Skill vocabulary

**Returns:**
- `np.ndarray`: Binary feature matrix (n_samples, n_skills)

---

## Module: clustering.py

### `fit_kmeans(X, n_clusters=5, random_state=42)`
Fit K-Means clustering model.

```python
model = fit_kmeans(X, n_clusters=5)
labels = model.labels_
```

**Parameters:**
- `X` (np.ndarray): Feature matrix
- `n_clusters` (int): Number of clusters (default: 5)
- `random_state` (int): Random seed for reproducibility

**Returns:**
- `KMeans`: Fitted scikit-learn KMeans object

---

### `fit_hierarchical(X, n_clusters=5, linkage='ward')`
Fit Hierarchical Clustering model.

```python
model = fit_hierarchical(X, n_clusters=5, linkage='ward')
labels = model.labels_
```

**Parameters:**
- `X` (np.ndarray): Feature matrix
- `n_clusters` (int): Number of clusters (default: 5)
- `linkage` (str): Linkage method ('ward', 'complete', 'average')

**Returns:**
- `AgglomerativeClustering`: Fitted scikit-learn model

---

### `fit_dbscan(X, eps='auto', min_samples=5)`
Fit DBSCAN clustering model.

```python
model = fit_dbscan(X, eps='auto', min_samples=5)
labels = model.labels_
```

**Parameters:**
- `X` (np.ndarray): Feature matrix
- `eps` (float or 'auto'): Neighborhood radius
- `min_samples` (int): Minimum samples in neighborhood

**Returns:**
- `DBSCAN`: Fitted scikit-learn model

---

## Module: evaluation.py

### `calculate_silhouette_score(X, labels)`
Calculate silhouette score for clustering.

```python
score = calculate_silhouette_score(X, labels)
# Returns: float between -1 and 1
```

**Parameters:**
- `X` (np.ndarray): Feature matrix
- `labels` (np.ndarray): Cluster labels

**Returns:**
- `float`: Silhouette score

---

### `compare_models(X, kmeans_labels, hierarchical_labels, dbscan_labels)`
Compare three clustering algorithms.

```python
results = compare_models(X, km_labels, hc_labels, db_labels)
# Returns: dict with scores and best model
```

**Parameters:**
- `X` (np.ndarray): Feature matrix
- `*_labels` (np.ndarray): Labels from each algorithm

**Returns:**
- `dict`: Scores for each algorithm and best model name

---

## Module: visualization.py

### `plot_clusters_pca(X, labels, title, savepath=None)`
Create 2D PCA scatter plot of clusters.

```python
plot_clusters_pca(X, labels, title='K-Means Clusters', 
                  savepath='output/visualizations/kmeans.png')
```

**Parameters:**
- `X` (np.ndarray): Feature matrix
- `labels` (np.ndarray): Cluster labels
- `title` (str): Plot title
- `savepath` (str): File path to save plot (optional)

**Returns:**
- `None` (saves to file)

---

### `plot_skill_heatmap(X, labels, skill_names, savepath=None)`
Create heatmap of skills by cluster.

```python
plot_skill_heatmap(X, labels, skill_names, 
                   savepath='output/visualizations/heatmap.png')
```

**Parameters:**
- `X` (np.ndarray): Feature matrix
- `labels` (np.ndarray): Cluster labels
- `skill_names` (list): Skill column names
- `savepath` (str): File path to save plot

**Returns:**
- `None` (saves to file)

---

## Complete Pipeline Example

```python
from src.preprocessing import load_resume_data, clean_text
from src.feature_engineering import create_feature_matrix
from src.clustering import fit_kmeans, fit_hierarchical, fit_dbscan
from src.evaluation import compare_models
from src.visualization import plot_clusters_pca
from src.config import SKILLS_DICTIONARY

# 1. Load and preprocess
df = load_resume_data('data/raw/resume_dataset.csv')
df['cleaned'] = df['resume'].apply(clean_text)

# 2. Extract features
X = create_feature_matrix(df['cleaned'].tolist(), SKILLS_DICTIONARY)

# 3. Fit models
km = fit_kmeans(X)
hc = fit_hierarchical(X)
db = fit_dbscan(X)

# 4. Evaluate
results = compare_models(X, km.labels_, hc.labels_, db.labels_)
print(f"Best model: {results['best_model']}")

# 5. Visualize
plot_clusters_pca(X, km.labels_, 'K-Means Clusters',
                  'output/visualizations/kmeans.png')
```
