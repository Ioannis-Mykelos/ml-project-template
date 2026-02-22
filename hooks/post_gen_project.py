#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
1. Initializes git repository
2. Configures git locally (user.name, user.email)
3. Makes initial commit
4. Sets up remote origin
5. Attempts to push to GitHub
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a shell command and return success status."""
    print(f"\n{description}...")
    try:
        # shell=True is used for cross-platform compatibility (Windows/Mac/Linux)
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(f"Error: {e.stderr.strip()}", file=sys.stderr)
        return False

def main():
    """Main post-generation hook."""
    project_dir = Path.cwd()
    
    # Templated variables from cookiecutter.json
    full_name = "{{ cookiecutter.full_name }}"
    email = "{{ cookiecutter.email }}"
    github_username = "{{ cookiecutter.github_username }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    
    print(f"\n{'='*60}")
    print("🚀 Running post-generation hook...")
    print(f"Project directory: {project_dir}")
    print(f"{'='*60}")

    # 1. Initialize git repository FIRST
    # This creates the .git folder so that local config has a place to live
    if not run_command("git init", "Initializing git repository", check=False):
        print("❌ Error: Could not initialize git repository. Is git installed?")
        return

    # 2. Configure git for this repository only
    # Using local config prevents overwriting your laptop's global settings
    run_command(f'git config user.name "{full_name}"', "Setting local git user.name", check=False)
    run_command(f'git config user.email "{email}"', "Setting local git user.email", check=False)
    run_command("git config init.defaultBranch main", "Setting default branch to main", check=False)

    # 3. Add all files
    run_command("git add .", "Staging files", check=False)

    # 4. Make initial commit
    commit_message = "Initial commit: Generated from ml-project-template"
    run_command(f'git commit -m "{commit_message}"', "Making initial commit", check=False)

    # 5. Set up remote origin
    remote_url = f"git@github.com:{github_username}/{project_slug}.git"
    print(f"\nTarget remote: {remote_url}")
    run_command(f'git remote add origin "{remote_url}"', "Adding remote origin", check=False)

    # 6. Attempt to push
    print("\nAttempting to push to GitHub...")
    if run_command("git push -u origin main", "Pushing to remote", check=False):
        print("\n✅ Successfully pushed to remote repository!")
    else:
        print("\n⚠️  Notice: Automatic push did not succeed.")
        print("This is normal if:")
        print("  - The repository hasn't been created on GitHub yet.")
        print("  - Your SSH keys are not configured on this machine.")
        print(f"\nTo push later, use: git push -u origin main")

    print(f"\n{'='*60}")
    print("Done! Your project is ready.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()