#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
This script runs after the project is generated and:
1. Configures git for the repository
2. Initializes git repository
3. Makes initial commit
4. Sets up remote origin
5. Attempts to push to GitHub (if repository exists)

Cookiecutter will template this file, replacing {{cookiecutter.*}} variables.
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a shell command and return success status."""
    print(f"\n{description}...")
    try:
        # Use shell=True for cross-platform compatibility
        # On Windows, this uses cmd.exe; on Unix, it uses /bin/sh
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(f"Error: {e.stderr}", file=sys.stderr)
        return False


def main():
    """Main post-generation hook."""
    # Get the project directory (where cookiecutter runs the hook)
    project_dir = Path.cwd()
    
    # These variables are templated by cookiecutter before the script runs
    full_name = "{{cookiecutter.full_name}}"
    email = "{{cookiecutter.email}}"
    github_username = "{{cookiecutter.github_username}}"
    project_slug = "{{cookiecutter.project_slug}}"
    
    print(f"\n{'='*60}")
    print("Running post-generation hook...")
    print(f"Project directory: {project_dir}")
    print(f"{'='*60}")
    
    # Configure git for this repository only (local config, not global)
    print("\nConfiguring git...")
    run_command(
        f'git config user.name "{full_name}"',
        "Setting git user.name",
        check=False
    )
    run_command(
        f'git config user.email "{email}"',
        "Setting git user.email",
        check=False
    )
    run_command(
        "git config init.defaultBranch main",
        "Setting default branch to main",
        check=False
    )
    
    # Initialize git repository
    print(f"\nInitializing git repository in: {project_dir}")
    if not run_command("git init", "Initializing git repository", check=False):
        print("Warning: Could not initialize git repository")
        return
    
    # Add all files
    if not run_command("git add .", "Adding files to git", check=False):
        print("Warning: Could not add files to git")
        return
    
    # Make initial commit
    commit_message = "Initial commit: Generated from ml-project-template"
    if not run_command(
        f'git commit -m "{commit_message}"',
        "Making initial commit",
        check=False
    ):
        print("Warning: Could not make initial commit (repository might already be initialized)")
    
    # Set up remote origin
    remote_url = f"git@github.com:{github_username}/{project_slug}.git"
    
    print(f"\nSetting remote origin to: {remote_url}")
    run_command(
        f'git remote add origin "{remote_url}"',
        "Adding remote origin",
        check=False
    )
    
    # Attempt to push, but don't fail if it doesn't work
    print("\nAttempting to push to remote...")
    if run_command("git push -u origin main", "Pushing to remote", check=False):
        print("✅ Successfully pushed to remote repository")
    else:
        print("\n⚠️  Warning: Could not push to remote. This is normal if:")
        print("  - The repository doesn't exist yet on GitHub")
        print("  - SSH keys are not configured")
        print("  - You don't have push access")
        print(f"\nYou can push manually later with: git push -u origin main")
    
    print(f"\n{'='*60}")
    print("Post-generation hook completed!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
