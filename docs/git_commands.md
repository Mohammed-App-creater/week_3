# Git Commands for Task 1 Workflow

## Initial Repository Setup

### 1. Initialize Git Repository (if not already initialized)
```bash
cd c:\Users\yoga\code\10_Academy\week_3
git init
```

### 2. Configure Git (if first time)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Add Remote Repository
```bash
# Replace <repository-url> with your actual GitHub repository URL
git remote add origin <repository-url>
```

## Task 1 Branch Workflow

### 4. Create and Switch to task-1 Branch
```bash
# Create and switch to task-1 branch
git checkout -b task-1

# Verify you're on the correct branch
git branch
```

### 5. Stage All Files
```bash
# Add all project files
git add .

# Or add specific files/directories
git add README.md
git add .gitignore
git add .github/
git add src/
git add notebooks/
git add docs/
git add requirements.txt
```

### 6. Initial Commit
```bash
git commit -m "feat: initialize project structure for ACIS insurance analytics

- Add comprehensive README with project overview and dataset description
- Create .gitignore for Python, Jupyter, and DVC
- Set up GitHub Actions CI/CD pipeline
- Create folder structure (src/, notebooks/, data/, outputs/, docs/)
- Add requirements.txt with core dependencies"
```

### 7. Push task-1 Branch to GitHub
```bash
# Push task-1 branch to remote
git push -u origin task-1
```

## Subsequent Commits During Task 1

### 8. Commit EDA Plan
```bash
git add docs/eda_plan.md
git commit -m "docs: add comprehensive EDA plan for insurance data analysis"
git push
```

### 9. Commit EDA Notebook
```bash
git add notebooks/task1_eda.ipynb
git add outputs/plots/
git commit -m "feat: implement complete EDA notebook with visualizations

- Add data loading and type conversion
- Implement missing value analysis
- Calculate loss ratios by province, vehicle type, and gender
- Add claim frequency and severity metrics
- Generate correlation matrix and time series plots
- Save all visualizations to outputs/plots/"
git push
```

### 10. Commit Source Code Utilities
```bash
git add src/
git commit -m "feat: add data processing and visualization utilities

- Create data_loader.py for data import functions
- Add data_cleaning.py with cleaning utilities
- Implement visualization.py with plotting functions"
git push
```

### 11. Commit Insights and Reports
```bash
git add docs/insights.md
git add docs/interim_report.md
git commit -m "docs: add EDA insights and interim report

- Document key findings from loss ratio analysis
- Identify geographic and demographic risk patterns
- Outline hypotheses for Task 3 testing
- Create professional interim report for stakeholders"
git push
```

### 12. Commit DVC Setup
```bash
git add .dvc/
git add data/raw/.gitignore
git add data/raw/insurance.csv.dvc
git commit -m "chore: initialize DVC for data version control

- Initialize DVC in project
- Track insurance.csv with DVC
- Configure local remote storage"
git push
```

## Merging to Main (After Task 1 Completion)

### 13. Switch to Main Branch
```bash
git checkout main
```

### 14. Merge task-1 into Main
```bash
git merge task-1
```

### 15. Push Main Branch
```bash
git push origin main
```

### 16. Delete Local task-1 Branch (Optional)
```bash
git branch -d task-1
```

### 17. Delete Remote task-1 Branch (Optional)
```bash
git push origin --delete task-1
```

## Useful Git Commands

### Check Status
```bash
git status
```

### View Commit History
```bash
git log --oneline --graph --all
```

### View Changes Before Committing
```bash
git diff
```

### Undo Uncommitted Changes
```bash
# Discard changes in working directory
git checkout -- <file>

# Unstage files
git reset HEAD <file>
```

### Amend Last Commit
```bash
git commit --amend -m "Updated commit message"
```

### View Remote URLs
```bash
git remote -v
```

### Pull Latest Changes
```bash
git pull origin task-1
```

## Creating Pull Request (via GitHub Web Interface)

1. Go to your GitHub repository
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select `base: main` and `compare: task-1`
5. Add title: "Task 1: Project Setup and Exploratory Data Analysis"
6. Add description with:
   - Summary of changes
   - Key findings
   - Checklist of completed items
7. Click "Create pull request"
8. Request review from team members
9. Merge after approval

## Quick Reference: Complete Task 1 Workflow

```bash
# 1. Create branch
git checkout -b task-1

# 2. Do your work (create files, run analysis)

# 3. Stage and commit
git add .
git commit -m "feat: complete Task 1 - EDA and project setup"

# 4. Push to GitHub
git push -u origin task-1

# 5. Create PR on GitHub (web interface)

# 6. After approval, merge to main
git checkout main
git merge task-1
git push origin main
```
