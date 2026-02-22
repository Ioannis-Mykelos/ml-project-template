#!/bin/bash
#echo "# {{ cookiecutter.project_slug }}" >> README.md
git config --global user.name "{{cookiecutter.full_name}}"
git config --global user.email {{cookiecutter.email}}
git config --global init.defaultBranch main
git config --global --add --bool push.autoSetupRemote true


# Get the absolute path of the directory where the script is currently running
PROJECT_DIR=$(pwd)

echo "Setting safe directory for: $PROJECT_DIR"
git config --global --add safe.directory "$PROJECT_DIR"
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
git push -u origin main
