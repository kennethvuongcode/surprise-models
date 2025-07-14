# Git Fork Workflow Guide

This guide explains how to work with git forks when contributing to the `eduardo-escoto/surprise-modeling` repository. Following this workflow will help maintain a clean project history and make collaboration smooth.

## Overview

When working with forks, you'll have:
- **Upstream repository**: `eduardo-escoto/surprise-modeling` (the original repo)
- **Your fork**: `your-username/surprise-modeling` (your personal copy)
- **Local repository**: Your local clone of your fork

## Initial Setup

### 1. Fork the Repository

1. Go to https://github.com/eduardo-escoto/surprise-modeling
2. Click the "Fork" button in the top-right corner
3. Select your GitHub account as the destination
4. Wait for GitHub to create your fork

### 2. Clone Your Fork

```bash
git clone https://github.com/your-username/surprise-modeling.git
cd surprise-modeling
```

### 3. Add Upstream Remote

Add the original repository as an "upstream" remote:

```bash
git remote add upstream https://github.com/eduardo-escoto/surprise-modeling.git
```

Verify your remotes:
```bash
git remote -v
```

You should see:
```
origin    https://github.com/your-username/surprise-modeling.git (fetch)
origin    https://github.com/your-username/surprise-modeling.git (push)
upstream  https://github.com/eduardo-escoto/surprise-modeling.git (fetch)
upstream  https://github.com/eduardo-escoto/surprise-modeling.git (push)
```

## Daily Workflow

### Before Starting New Work

Always sync your main branch with upstream before creating new branches:

```bash
# Switch to main branch
git checkout main

# Fetch latest changes from upstream
git fetch upstream

# Merge upstream changes into your main
git merge upstream/main

# Push updated main to your fork
git push origin main
```

### Working on Features

#### 1. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or use the newer syntax
git switch -c feature/your-feature-name
```

**Branch naming conventions:**
- `feature/add-new-model` - for new features
- `fix/resolve-data-loading` - for bug fixes
- `docs/update-readme` - for documentation updates
- `refactor/cleanup-utils` - for code refactoring

#### 2. Make Your Changes

Work on your feature, making commits as you go:

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add data preprocessing pipeline for user feedback"
```

**Good commit message practices:**
- Use present tense ("Add feature" not "Added feature")
- Be specific and descriptive
- Keep the first line under 50 characters
- Add more details in the body if needed

#### 3. Push Your Branch

```bash
git push origin feature/your-feature-name
```

#### 4. Create a Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request" (appears after pushing)
3. Ensure the base repository is `eduardo-escoto/surprise-modeling` and base branch is `main`
4. Write a clear title and description
5. Click "Create pull request"

## Keeping Your Fork Updated

### Option 1: Using GitHub's Interface

1. Go to your fork on GitHub
2. Click "Sync fork" button
3. Click "Update branch"

### Option 2: Using Command Line (Recommended)

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### If Your Feature Branch Gets Behind

If upstream has been updated while you're working on a feature:

```bash
# Switch to your feature branch
git checkout feature/your-feature-name

# Fetch latest upstream changes
git fetch upstream

# Rebase your branch onto the latest main
git rebase upstream/main

# Force push (be careful with this!)
git push origin feature/your-feature-name --force-with-lease
```

## Best Practices

### 1. Keep Your Main Clean
- **Never** work directly on your main branch
- **Always** create feature branches for new work
- Keep your main branch in sync with upstream

### 2. Small, Focused Changes
- Make small, focused commits
- One feature per branch
- Break large features into smaller, reviewable chunks

### 3. Regular Updates
- Sync with upstream regularly (daily or before starting new work)
- Don't let your fork get too far behind

### 4. Code Review Ready
- Test your changes locally before pushing
- Write clear commit messages
- Include relevant documentation updates

## Common Commands Reference

```bash
# Check current branch and status
git status

# See all branches
git branch -a

# Switch branches
git checkout branch-name
# or
git switch branch-name

# Delete a local branch (after merge)
git branch -d feature/branch-name

# Delete a remote branch
git push origin --delete feature/branch-name

# See commit history
git log --oneline

# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Stash changes temporarily
git stash
git stash pop
```

## Troubleshooting

### My Fork is Behind
```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### I Made Changes on Main by Mistake
```bash
# Create a new branch from current main
git checkout -b feature/my-changes

# Reset main to upstream
git checkout main
git reset --hard upstream/main
git push origin main --force-with-lease
```

### Merge Conflicts
```bash
# After a failed merge/rebase
git status  # shows conflicted files
# Edit files to resolve conflicts
git add .
git commit  # or git rebase --continue
```

## Questions?

If you run into issues:
1. Check this guide first
2. Search for the error message online
3. Ask a team member for help
4. Include the exact error message and what you were trying to do

Remember: It's better to ask for help than to mess up the repository! 