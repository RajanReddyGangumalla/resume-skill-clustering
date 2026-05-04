# Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: "No Resume Column Found"

**Error Message:**
```
ValueError: No valid resume column detected in dataset
```

**Causes:**
- CSV doesn't have a resume text column
- Column name is not in the common list
- Column name has uppercase letters (e.g., "Resume" vs "resume")

**Solutions:**

1. **Rename your column** to one of these:
   - `resume`, `text`, `content`, `description`, `profile`, `skills`, `summary`

2. **Modify config.py** to add custom column name:
   ```python
   COMMON_RESUME_COLUMNS = [
       'resume', 'text', 'my_custom_column'
   ]
   ```

3. **Preprocess CSV before running**:
   ```python
   df = pd.read_csv('data/raw/resume_dataset.csv')
   df = df.rename(columns={'Resume Text': 'resume'})
   df.to_csv('data/raw/resume_dataset.csv', index=False)
   ```

---

### Issue 2: "UnicodeDecodeError: 'utf-8' codec can't decode byte"

**Error Message:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 100
```

**Causes:**
- CSV file has non-UTF-8 encoding (e.g., Latin-1, ISO-8859-1)
- Mixed encodings in file

**Solutions:**

1. **Let auto-detection handle it** (should work):
   ```python
   # preprocessing.py handles this automatically
   df = load_resume_data('data/raw/resume_dataset.csv')
   ```

2. **Manually specify encoding**:
   ```python
   import chardet
   with open('data/raw/resume_dataset.csv', 'rb') as f:
       result = chardet.detect(f.read())
   encoding = result['encoding']
   df = pd.read_csv('data/raw/resume_dataset.csv', encoding=encoding)
   ```

3. **Convert file to UTF-8**:
   ```bash
   iconv -f ISO-8859-1 -t UTF-8 old_file.csv > new_file.csv
   ```

---

### Issue 3: "Empty Feature Matrix"

**Error Message:**
```
ValueError: Feature matrix has shape (n, 0). No skills detected.
```

**Causes:**
- Resume text doesn't contain any recognized skills
- Skill dictionary is incomplete
- Text preprocessing removed too much

**Solutions:**

1. **Check skill coverage**:
   ```python
   from src.config import SKILLS_DICTIONARY
   print(f"Skills in dictionary: {len(SKILLS_DICTIONARY)}")
   print(list(SKILLS_DICTIONARY.keys())[:10])  # View first 10
   ```

2. **Add custom skills to config.py**:
   ```python
   SKILLS_DICTIONARY = {
       # ...existing skills...
       'rust': ['rust'],
       'elixir': ['elixir'],
       'solidity': ['solidity'],
   }
   ```

3. **Verify resume quality**:
   ```python
   df = load_resume_data('data/raw/resume_dataset.csv')
   print(df['resume'].head())
   print(df['resume'].str.len().describe())
   ```

---

### Issue 4: "Out of Memory (MemoryError)"

**Error Message:**
```
MemoryError: Unable to allocate memory
```

**Causes:**
- Dataset too large (>100K resumes)
- Feature matrix dimensions too high
- PCA calculation on large dataset

**Solutions:**

1. **Reduce dataset size**:
   ```python
   df = df.sample(n=5000, random_state=42)  # Use 5000 samples
   ```

2. **Reduce skill dictionary**:
   ```python
   # Keep only top 20 skills
   SKILLS_DICTIONARY = {k: v for k, v in list(SKILLS_DICTIONARY.items())[:20]}
   ```

3. **Use sparse matrices** (modify feature_engineering.py):
   ```python
   from scipy.sparse import csr_matrix
   X_sparse = csr_matrix(X)
   ```

4. **Process in batches** (modify clustering.py):
   ```python
   batch_size = 1000
   for i in range(0, len(X), batch_size):
       batch = X[i:i+batch_size]
       # Process batch
   ```

---

### Issue 5: "DBSCAN Creates Too Many Clusters"

**Error Message:**
```
DBSCAN found 50+ clusters (too many)
```

**Causes:**
- eps parameter too small
- min_samples too low
- Data is sparse with many outliers

**Solutions:**

1. **Adjust DBSCAN parameters** in config.py:
   ```python
   DBSCAN_EPS = 0.8  # Increase from 0.5
   DBSCAN_MIN_SAMPLES = 10  # Increase from 5
   ```

2. **Use eps='auto' with different quantile**:
   ```python
   # In clustering.py, modify auto-tuning:
   distances = np.sort(nbrs.kneighbors_distance(X), axis=0)
   distances = distances[:, -1]
   eps = np.percentile(distances, 90)  # 90th percentile instead of 80th
   ```

3. **Calculate eps manually**:
   ```python
   from sklearn.neighbors import NearestNeighbors
   neighbors = NearestNeighbors(n_neighbors=5)
   neighbors_fit = neighbors.fit(X)
   distances, indices = neighbors_fit.kneighbors(X)
   distances = np.sort(distances[:, -1], axis=0)
   # Plot and find elbow
   plt.plot(distances)
   plt.show()
   ```

---

### Issue 6: "Silhouette Score is Very Low"

**Error Message:**
```
Silhouette Score: 0.05 (too low!)
```

**Causes:**
- Clusters are not well-separated
- Wrong number of clusters (k too high or low)
- Features not normalized properly

**Solutions:**

1. **Try different cluster counts**:
   ```python
   scores = {}
   for k in range(2, 10):
       model = KMeans(n_clusters=k)
       labels = model.fit_predict(X)
       score = silhouette_score(X, labels)
       scores[k] = score
   best_k = max(scores, key=scores.get)
   ```

2. **Normalize features** (modify feature_engineering.py):
   ```python
   from sklearn.preprocessing import StandardScaler
   scaler = StandardScaler()
   X = scaler.fit_transform(X)
   ```

3. **Use different linkage method** (for Hierarchical):
   ```python
   # Try 'complete' or 'average' instead of 'ward'
   model = AgglomerativeClustering(linkage='complete')
   ```

---

### Issue 7: "Main.py Runs Slowly"

**Error Message:**
```
Running... (no progress, very slow)
```

**Causes:**
- Large dataset (>50K resumes)
- Inefficient clustering parameters
- Disk I/O bottleneck
- CPU-intensive PCA

**Solutions:**

1. **Enable parallel processing** in config.py:
   ```python
   N_JOBS = -1  # Use all CPU cores
   ```

2. **Reduce features**:
   ```python
   # Use top 20 skills instead of 40+
   X = X[:, :20]
   ```

3. **Skip PCA for large datasets**:
   ```python
   # In main.py, comment out PCA visualization
   # plot_clusters_pca(X, labels, title)
   ```

4. **Use sample for testing**:
   ```python
   df = df.sample(n=1000, random_state=42)
   ```

---

## Debug Mode

Enable verbose logging to troubleshoot issues:

```python
# In main.py or config.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.debug(f"Loaded {len(df)} resumes")
logger.debug(f"Feature matrix shape: {X.shape}")
logger.debug(f"Silhouette score: {score}")
```

---

## Getting Help

1. **Check output files**:
   - `output/reports/evaluation_report.txt` - Detailed metrics
   - Visualizations - Visual inspection of results

2. **Review notebooks**:
   - `notebooks/01_exploratory_analysis.ipynb` - Data insights
   - `notebooks/03_clustering_analysis.ipynb` - Algorithm diagnostics

3. **Run tests**:
   ```bash
   pytest tests/ -v --tb=short
   ```

4. **Contact support** with:
   - Dataset sample (first 10 rows)
   - Full error message and traceback
   - System info (Python version, OS)
   - Steps to reproduce
