# System Architecture

## Overview

The Student Clustering Project follows a modular, layered architecture designed for maintainability, scalability, and reproducibility.

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│         PRESENTATION LAYER                          │
│  (main.py, visualizations, reports)                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         APPLICATION LAYER                           │
│  (clustering.py, evaluation.py, visualization.py)   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         FEATURE ENGINEERING LAYER                   │
│  (feature_engineering.py, preprocessing.py)         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         DATA LAYER                                  │
│  (data loading, file I/O, config management)        │
└─────────────────────────────────────────────────────┘
```

## Module Responsibilities

### config.py
- Centralized configuration management
- Skill dictionary definitions
- Algorithm parameters
- File paths and constants

### preprocessing.py
- CSV loading with encoding detection
- Column name detection
- Text cleaning (lowercase, special chars, URLs)
- Missing value handling

### feature_engineering.py
- Skill extraction using regex patterns
- Binary feature encoding
- Feature matrix creation
- Skill vocabulary management

### clustering.py
- K-Means implementation (k-means++)
- Hierarchical Clustering (Ward linkage)
- DBSCAN (with eps auto-tuning)
- Model fitting and prediction

### evaluation.py
- Silhouette score calculation
- Davies-Bouldin Index
- Calinski-Harabasz Score
- Model comparison and selection

### visualization.py
- PCA dimensionality reduction
- Scatter plot generation
- Heatmap creation
- Plot styling and formatting

### utils.py
- Helper functions
- File I/O utilities
- Error handling
- Logging setup

## Data Flow

```
┌──────────────────┐
│ resume_dataset   │
│    (CSV)         │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ PREPROCESSING        │
│ - Load CSV           │
│ - Clean text         │
│ - Handle encoding    │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ FEATURE ENGINEERING  │
│ - Extract skills     │
│ - Binary encoding    │
│ - Create vectors     │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ CLUSTERING (3 algorithms)        │
│ ┌─────────┐ ┌─────────┐ ┌──────┐│
│ │ K-Means │ │Hierarch │ │DBSCAN││
│ └─────────┘ └─────────┘ └──────┘│
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────┐
│ EVALUATION           │
│ - Silhouette scores  │
│ - Model comparison   │
│ - Best model select  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ VISUALIZATION        │
│ - PCA reduction      │
│ - Scatter plots      │
│ - Heatmaps           │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────┐
│ OUTPUT                   │
│ - Models (pkl)           │
│ - Reports (txt, json)    │
│ - Visualizations (png)   │
└──────────────────────────┘
```

## Design Patterns

### 1. Modular Design
Each component has single responsibility and can be tested independently.

### 2. Configuration Management
All parameters in `config.py` for easy modification without code changes.

### 3. Pipeline Pattern
Sequential processing stages with clear inputs/outputs.

### 4. Model Persistence
Clustering models saved as pickle files for reuse.

### 5. Error Handling
Try-catch blocks with informative error messages.

## Scalability Considerations

- **Vectorization**: NumPy for efficient numerical operations
- **Memory**: Stream processing for large datasets
- **Parallelization**: scikit-learn parallelism enabled
- **Caching**: Preprocessed features saved to disk

## Testing Strategy

```
tests/
├── test_preprocessing.py      # CSV loading, text cleaning
├── test_feature_engineering.py # Skill extraction, vectorization
├── test_clustering.py         # Algorithm implementations
└── test_utils.py              # Helper functions
```

Run tests with:
```bash
pytest tests/ -v
```
