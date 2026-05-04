# Notebooks Guide

## Overview

Interactive Jupyter notebooks for exploring and understanding the clustering pipeline.

## Notebooks

### 1. 01_exploratory_analysis.ipynb
**Purpose**: Initial data exploration and quality assessment

**Contents**:
- Load and inspect resume dataset
- Text statistics (length, word count, encoding)
- Identify most common skills mentioned
- Visualize resume characteristics
- Check for missing/malformed data

**Expected Output**: Data quality report, skill frequency charts

---

### 2. 02_feature_engineering.ipynb
**Purpose**: Demonstrate skill extraction and feature creation

**Contents**:
- Preprocessing pipeline walkthrough
- Skill dictionary overview (40+ skills)
- Binary encoding demonstration
- Feature matrix creation
- Skill coverage analysis

**Expected Output**: Feature vectors, skill distribution plots

---

### 3. 03_clustering_analysis.ipynb
**Purpose**: Compare and analyze clustering algorithms

**Contents**:
- K-Means clustering with elbow method
- Hierarchical clustering with dendrograms
- DBSCAN with eps optimization
- Silhouette score comparison
- Cluster profile interpretation
- PCA visualizations

**Expected Output**: Algorithm comparison, cluster profiles, visualizations

---

## Running Notebooks

```bash
# Install Jupyter
pip install jupyter

# Start Jupyter server
jupyter notebook

# Navigate to notebooks/ folder
```

## Requirements

Ensure `requirements.txt` is installed:

```bash
pip install -r ../requirements.txt
```

## Tips

- Run cells sequentially (top to bottom)
- Modify parameters to experiment
- Save outputs using notebook cells
- Export plots as PNG for reports
