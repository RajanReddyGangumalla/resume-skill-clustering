# Data Directory

## Structure

```
data/
├── raw/
│   └── resume_dataset.csv          # Original unprocessed resume data
├── processed/
│   ├── cleaned_resumes.csv         # Cleaned resume text
│   ├── skill_vectors.pkl           # Binary encoded skill features
│   └── cluster_assignments.csv     # Final cluster assignments
└── README.md
```

## File Descriptions

### raw/resume_dataset.csv
- **Format**: CSV (comma or semicolon delimited)
- **Encoding**: UTF-8 or Latin-1 (auto-detected)
- **Required Column**: Text field containing resume content
- **Common Column Names**: resume, text, content, description, profile, skills, summary

### processed/
Generated during pipeline execution. Contains:
- Cleaned resume text after preprocessing
- Binary skill vectors (features)
- Final cluster assignments with metrics

## Usage

Place your resume dataset in `raw/` folder before running:

```bash
python main.py
```

Processed files will be automatically generated in `processed/` directory.

## Data Format Example

| ID | Resume | Company | Position |
|----|--------|---------|----------|
| 1 | "Experienced Python developer with..." | TechCorp | Senior Dev |
| 2 | "Full-stack engineer proficient in..." | StartupXYZ | Full-Stack |

**Note**: Only the resume text column is required for clustering.
