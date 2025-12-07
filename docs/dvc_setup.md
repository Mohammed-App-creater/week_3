# DVC Setup Instructions
## Data Version Control for AlphaCare Insurance Solutions

---

## What is DVC?

**DVC (Data Version Control)** is a version control system for data science and machine learning projects. It works alongside Git to:
- Track large data files without storing them in Git
- Version datasets, models, and experiment results
- Share data across team members
- Reproduce experiments and results

---

## Prerequisites

- Git repository initialized
- Python 3.7+ installed
- pip package manager

---

## Step 1: Install DVC

```bash
# Install DVC
pip install dvc

# Verify installation
dvc version
```

Expected output:
```
DVC version: 3.x.x
```

---

## Step 2: Initialize DVC in Your Project

```bash
# Navigate to project directory
cd c:\Users\yoga\code\10_Academy\week_3

# Initialize DVC
dvc init

# Verify DVC initialization
ls -la .dvc/
```

**What happens**:
- Creates `.dvc/` directory with configuration files
- Creates `.dvcignore` file (similar to `.gitignore`)
- Adds DVC files to Git tracking

**Commit DVC initialization**:
```bash
git add .dvc .dvcignore
git commit -m "chore: initialize DVC for data version control"
```

---

## Step 3: Add Data Files to DVC

### 3.1 Track the Insurance Dataset

```bash
# Add the raw data file to DVC
dvc add data/raw/insurance.csv
```

**What happens**:
- Creates `data/raw/insurance.csv.dvc` (metadata file)
- Adds `data/raw/insurance.csv` to `.gitignore`
- Moves actual data to `.dvc/cache/`

### 3.2 Commit DVC Metadata

```bash
# Add the .dvc file and updated .gitignore to Git
git add data/raw/insurance.csv.dvc data/raw/.gitignore
git commit -m "chore: track insurance.csv with DVC"
```

**Important**: 
- The actual data file (`insurance.csv`) is NOT in Git
- Only the metadata file (`.dvc`) is tracked by Git
- This keeps your Git repository lightweight

---

## Step 4: Configure Remote Storage

DVC needs a remote storage location to share data with team members.

### Option A: Local Remote (for testing)

```bash
# Create a local directory for DVC remote
mkdir -p C:\Users\yoga\dvc-storage

# Configure DVC remote
dvc remote add -d local C:\Users\yoga\dvc-storage

# Verify remote configuration
dvc remote list
```

### Option B: Cloud Storage (recommended for production)

#### Google Drive
```bash
dvc remote add -d gdrive gdrive://your-folder-id
```

#### Amazon S3
```bash
dvc remote add -d s3remote s3://your-bucket-name/path
dvc remote modify s3remote region us-east-1
```

#### Azure Blob Storage
```bash
dvc remote add -d azure azure://your-container-name/path
```

#### Google Cloud Storage
```bash
dvc remote add -d gcs gs://your-bucket-name/path
```

### Commit Remote Configuration

```bash
git add .dvc/config
git commit -m "chore: configure DVC remote storage"
```

---

## Step 5: Push Data to Remote

```bash
# Push data to remote storage
dvc push
```

**What happens**:
- Uploads `insurance.csv` from `.dvc/cache/` to remote storage
- Team members can now pull this data

**Verify**:
```bash
# Check status
dvc status
```

Expected output: `Data and pipelines are up to date.`

---

## Step 6: Pulling Data (for team members)

When a team member clones the repository:

```bash
# Clone the Git repository
git clone <repository-url>
cd week_3

# Pull data from DVC remote
dvc pull
```

**What happens**:
- Downloads `insurance.csv` from remote storage
- Places it in `data/raw/insurance.csv`
- Now they have the exact same data version

---

## Step 7: Updating Data

When you update the dataset:

```bash
# Modify the data file (e.g., add new records)
# Then update DVC tracking

dvc add data/raw/insurance.csv

# Commit the updated .dvc file
git add data/raw/insurance.csv.dvc
git commit -m "data: update insurance dataset with new records"

# Push updated data to remote
dvc push

# Push Git changes
git push
```

---

## Step 8: Verify DVC Setup

### Check DVC Status
```bash
dvc status
```

### Check DVC Cache
```bash
dvc cache dir
ls .dvc/cache/
```

### Check Remote Connection
```bash
dvc remote list
```

### Validate Data Integrity
```bash
# Check MD5 hash of tracked file
dvc status data/raw/insurance.csv.dvc
```

---

## Common DVC Commands

### Tracking Files
```bash
# Track a single file
dvc add data/raw/file.csv

# Track a directory
dvc add data/processed/
```

### Managing Remotes
```bash
# List remotes
dvc remote list

# Add remote
dvc remote add -d myremote /path/to/remote

# Remove remote
dvc remote remove myremote

# Modify remote
dvc remote modify myremote url /new/path
```

### Data Operations
```bash
# Push data to remote
dvc push

# Pull data from remote
dvc pull

# Fetch data (download to cache only)
dvc fetch

# Checkout specific version
dvc checkout
```

### Status and Logs
```bash
# Check status
dvc status

# Show DVC-tracked files
dvc list . --dvc-only

# Show data metrics
dvc metrics show
```

---

## DVC Workflow Integration

### Daily Workflow

1. **Pull latest data**
   ```bash
   git pull
   dvc pull
   ```

2. **Work on analysis**
   - Run notebooks
   - Generate outputs

3. **Update data if needed**
   ```bash
   dvc add data/processed/cleaned_data.csv
   git add data/processed/cleaned_data.csv.dvc
   git commit -m "data: add cleaned dataset"
   dvc push
   git push
   ```

### Branching with DVC

```bash
# Create feature branch
git checkout -b feature/new-analysis

# Work with data
dvc pull

# Make changes
dvc add data/interim/feature_data.csv
git add data/interim/feature_data.csv.dvc
git commit -m "data: add feature engineering dataset"
dvc push

# Merge to main
git checkout main
git merge feature/new-analysis
dvc pull
```

---

## Troubleshooting

### Issue: "dvc pull" fails

**Solution**:
```bash
# Check remote configuration
dvc remote list

# Verify remote path exists
dvc remote list --verbose

# Try fetching first
dvc fetch
dvc checkout
```

### Issue: Large cache size

**Solution**:
```bash
# Remove unused cache files
dvc gc --workspace

# Remove all unused cache
dvc gc --all-commits
```

### Issue: Data file modified but not tracked

**Solution**:
```bash
# Re-add the file
dvc add data/raw/insurance.csv

# Commit changes
git add data/raw/insurance.csv.dvc
git commit -m "data: update tracked file"
dvc push
```

---

## Best Practices

### 1. Track Raw Data
- Always track raw, unmodified data with DVC
- Never edit raw data files directly
- Keep raw data immutable

### 2. Version Processed Data
- Track intermediate and processed datasets
- Document transformations in code
- Use meaningful commit messages

### 3. Use .dvcignore
- Exclude temporary files from DVC tracking
- Similar to `.gitignore` but for DVC

Example `.dvcignore`:
```
# Temporary files
*.tmp
*.temp

# Logs
*.log

# System files
.DS_Store
Thumbs.db
```

### 4. Document Data Changes
- Use descriptive commit messages
- Maintain a CHANGELOG for data versions
- Tag important data versions

```bash
git tag -a data-v1.0 -m "Initial insurance dataset"
git push --tags
```

### 5. Regular Cleanup
```bash
# Remove unused cache (monthly)
dvc gc --workspace

# Verify integrity
dvc status
```

---

## DVC for Task 2 and Beyond

### Task 2: Data Quality Assessment
```bash
# Track cleaned data
dvc add data/processed/insurance_cleaned.csv
git add data/processed/insurance_cleaned.csv.dvc
git commit -m "data: add cleaned insurance dataset"
dvc push
```

### Task 3: Feature Engineering
```bash
# Track engineered features
dvc add data/processed/features.csv
git add data/processed/features.csv.dvc
git commit -m "data: add engineered features for modeling"
dvc push
```

### Task 4: Model Versioning
```bash
# Track trained models
dvc add models/random_forest_v1.pkl
git add models/random_forest_v1.pkl.dvc
git commit -m "model: add Random Forest v1"
dvc push
```

---

## Additional Resources

- **DVC Documentation**: https://dvc.org/doc
- **DVC Tutorial**: https://dvc.org/doc/start
- **DVC with Git**: https://dvc.org/doc/use-cases/versioning-data-and-model-files
- **DVC Remote Storage**: https://dvc.org/doc/command-reference/remote

---

## Summary Checklist

- [ ] Install DVC (`pip install dvc`)
- [ ] Initialize DVC (`dvc init`)
- [ ] Add data files (`dvc add data/raw/insurance.csv`)
- [ ] Configure remote storage (`dvc remote add`)
- [ ] Push data to remote (`dvc push`)
- [ ] Commit DVC files to Git
- [ ] Verify setup (`dvc status`)
- [ ] Document workflow in team README

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Author**: AlphaCare Analytics Team
