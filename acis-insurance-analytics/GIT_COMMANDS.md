# Git Commands for ACIS Insurance Analytics

## 📋 Quick Reference Guide

This document contains all the Git commands you need to set up and manage the ACIS Insurance Analytics repository.

---

## 🚀 Initial Repository Setup

### Step 1: Initialize Local Repository

```bash
# Navigate to project directory
cd c:\Users\yoga\code\10_Academy\week_3\acis-insurance-analytics

# Initialize Git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "chore: initial project setup with folder structure and documentation"
```

### Step 2: Create GitHub Repository

**Option A: Using GitHub CLI (Recommended)**
```bash
# Install GitHub CLI if not already installed
# Download from: https://cli.github.com/

# Authenticate with GitHub
gh auth login

# Create repository on GitHub
gh repo create acis-insurance-analytics --public --source=. --remote=origin --push

# Or for private repository
gh repo create acis-insurance-analytics --private --source=. --remote=origin --push
```

**Option B: Manual Setup via GitHub Website**
1. Go to https://github.com/new
2. Repository name: `acis-insurance-analytics`
3. Choose Public or Private
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

Then connect your local repo:
```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/acis-insurance-analytics.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🌿 Task 1 Branch Workflow

### Create and Switch to task-1 Branch

```bash
# Ensure you're on main branch
git checkout main

# Create and switch to task-1 branch
git checkout -b task-1

# Verify you're on the correct branch
git branch
```

### Alternative: Create develop branch first (Git Flow)

```bash
# Create develop branch from main
git checkout main
git checkout -b develop
git push -u origin develop

# Now create task-1 from develop
git checkout develop
git checkout -b task-1
```

---

## 💾 Working on Task 1

### Making Changes and Committing

```bash
# Check status of your changes
git status

# Add specific files
git add scripts/eda/data_summary.py
git add notebooks/eda/01_data_overview.ipynb

# Or add all changes
git add .

# Commit with descriptive message
git commit -m "feat: implement data loading and summary statistics"

# More commit examples:
git commit -m "feat: add univariate analysis for numerical features"
git commit -m "feat: create missing data visualization"
git commit -m "docs: update EDA documentation in README"
git commit -m "fix: resolve pandas dtype warning in data loader"
```

### Viewing Your Work

```bash
# View commit history
git log --oneline --graph --all

# View changes before staging
git diff

# View staged changes
git diff --cached

# View changes in specific file
git diff scripts/eda/data_summary.py
```

---

## 🔄 Pushing to GitHub

### Push task-1 Branch

```bash
# First time pushing task-1 branch
git push -u origin task-1

# Subsequent pushes
git push
```

### Verify Push

```bash
# Check remote branches
git branch -r

# Check all branches (local and remote)
git branch -a
```

---

## 🔀 Creating Pull Request

### Option A: Using GitHub CLI

```bash
# Create PR from task-1 to develop (or main)
gh pr create --base develop --head task-1 --title "Task 1: Exploratory Data Analysis" --body "## Summary
- Implemented data loading module
- Created univariate and bivariate analysis
- Generated visualizations for missing data
- Documented findings in notebooks

## Checklist
- [x] Code follows style guidelines
- [x] Tests pass
- [x] Documentation updated
- [x] Notebooks executed successfully"

# Or use interactive mode
gh pr create
```

### Option B: Via GitHub Website

1. Go to your repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Base: `develop` (or `main`) ← Compare: `task-1`
4. Click "Create pull request"
5. Fill in title and description
6. Click "Create pull request"

---

## 🔄 Merging and Cleanup

### After PR is Approved

```bash
# Switch to develop (or main)
git checkout develop

# Pull latest changes
git pull origin develop

# Merge task-1 (if not merged via GitHub)
git merge task-1 --no-ff

# Push merged changes
git push origin develop

# Delete local task-1 branch
git branch -d task-1

# Delete remote task-1 branch
git push origin --delete task-1
```

---

## 🛠️ Useful Git Commands

### Branch Management

```bash
# List all branches
git branch -a

# Switch to existing branch
git checkout branch-name

# Create new branch
git checkout -b new-branch-name

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Rename current branch
git branch -m new-name
```

### Syncing with Remote

```bash
# Fetch changes from remote
git fetch origin

# Pull changes (fetch + merge)
git pull origin main

# Pull with rebase
git pull --rebase origin main

# Push all branches
git push --all origin
```

### Undoing Changes

```bash
# Discard changes in working directory
git checkout -- filename

# Unstage file (keep changes)
git reset HEAD filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert commit-hash
```

### Stashing Changes

```bash
# Save changes temporarily
git stash

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove stash
git stash pop

# Drop stash
git stash drop
```

### Viewing History

```bash
# Detailed log
git log

# Compact log
git log --oneline

# Graph view
git log --oneline --graph --all

# Show specific commit
git show commit-hash

# Show changes in last commit
git show HEAD
```

---

## 📝 Commit Message Best Practices

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Formatting, missing semicolons, etc.
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance, dependencies

### Examples

```bash
# Simple commit
git commit -m "feat: add data validation function"

# Detailed commit
git commit -m "feat: implement advanced statistical analysis

- Add correlation matrix calculation
- Implement hypothesis testing
- Create visualization functions
- Update documentation

Closes #123"
```

---

## 🔥 Emergency Commands

### Accidentally Committed to Wrong Branch

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Switch to correct branch
git checkout correct-branch

# Commit changes
git add .
git commit -m "your message"
```

### Merge Conflicts

```bash
# When merge conflict occurs
git status  # See conflicted files

# Edit files to resolve conflicts
# Look for <<<<<<< HEAD markers

# After resolving
git add resolved-file
git commit -m "fix: resolve merge conflicts"
```

### Reset to Remote State

```bash
# Discard all local changes
git fetch origin
git reset --hard origin/main
```

---

## 🎯 Complete Task 1 Workflow Example

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create task-1 branch
git checkout -b task-1

# 3. Do your work...
# Create files, write code, run analysis

# 4. Stage and commit changes
git add .
git commit -m "feat: complete exploratory data analysis for Task 1"

# 5. Push to GitHub
git push -u origin task-1

# 6. Create Pull Request
gh pr create --base main --head task-1 --title "Task 1: EDA Complete"

# 7. After PR approval and merge, cleanup
git checkout main
git pull origin main
git branch -d task-1
git push origin --delete task-1

# 8. Ready for Task 2
git checkout -b task-2
```

---

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow Workflow](https://nvie.com/posts/a-successful-git-branching-model/)

---

**Pro Tip**: Create a `.gitconfig` alias for common commands:

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --all"
```

Now you can use: `git st`, `git co`, `git br`, etc.
