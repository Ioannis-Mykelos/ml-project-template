#!/bin/bash
set -e  # Exit on error

# Configure git for this repository only (local config, not global)
git config user.name "{{cookiecutter.full_name}}"
git config user.email "{{cookiecutter.email}}"
git config init.defaultBranch main

# Get the absolute path of the directory where the script is currently running
PROJECT_DIR=$(pwd)

echo "Initializing git repository in: $PROJECT_DIR"
git init
git add .
git commit -m "Initial commit: Generated from ml-project-template"

# Only set up remote and push if repository URL is provided and valid
REMOTE_URL="git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git"
echo "Setting remote origin to: $REMOTE_URL"
git remote add origin "$REMOTE_URL" || echo "Warning: Remote may already exist"

# Attempt to push, but don't fail if it doesn't work (repo might not exist yet)
echo "Attempting to push to remote..."
if git push -u origin main 2>/dev/null; then
    echo "Successfully pushed to remote repository"
else
    echo "Warning: Could not push to remote. This is normal if:"
    echo "  - The repository doesn't exist yet on GitHub"
    echo "  - SSH keys are not configured"
    echo "  - You don't have push access"
    echo "You can push manually later with: git push -u origin main"
fi
