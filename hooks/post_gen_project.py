#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return output if successful."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_github_username(fallback):
    """Detect the actual GitHub username from the system."""
    # 1. Try GitHub CLI (The most reliable way)
    gh_user = run_command("gh api user --jq .login")
    if gh_user:
        return gh_user

    # 2. Try git config (Commonly used by some tools)
    git_user = run_command("git config --get github.user")
    if git_user:
        return git_user

    # 3. Fallback to the cookiecutter variable
    return fallback


def create_jupyter_kernel(project_slug):
    """Create a Jupyter kernel from the uv virtual environment."""
    print("\n📓 Setting up Jupyter kernel...")

    # Ensure ipykernel is installed in the venv
    if run_command("uv run python -m ipykernel --version", check=False) is None:
        print("  Installing ipykernel...")
        run_command("uv add ipykernel")

    # Register the kernel using the project slug as the kernel name
    kernel_cmd = (
        f"uv run python -m ipykernel install "
        f"--user "
        f"--name {project_slug} "
        f"--display-name 'Python ({project_slug})'"
    )

    if run_command(kernel_cmd, check=False) is not None:
        print(f"  ✅ Jupyter kernel 'Python ({project_slug})' created successfully!")
    else:
        print("  ⚠️  Kernel creation failed. Run manually:")
        print(
            f"      uv run python -m ipykernel install --user --name {project_slug} --display-name 'Python ({project_slug})'"
        )


def main():
    project_dir = Path.cwd()

    # Templated variables
    full_name = "{{ cookiecutter.full_name }}"
    email = "{{ cookiecutter.email }}"
    project_slug = "{{ cookiecutter.project_slug }}"

    # DETECT REAL USERNAME
    raw_github_username = "{{ cookiecutter.github_username }}"
    github_username = get_github_username(raw_github_username)

    print(f"\n{'=' * 60}")
    print(f"🚀 Detected GitHub User: {github_username}")
    print(f"📁 Project directory: {project_dir}")
    print(f"{'=' * 60}")

    # 1. Init
    run_command("git init", check=False)

    # 2. Config
    run_command(f'git config user.name "{full_name}"')
    run_command(f'git config user.email "{email}"')
    run_command("git config init.defaultBranch main")

    # 3. Commit
    run_command("git add .")
    run_command('git commit -m "Initial commit from template"')

    # 4. Remote & Push
    remote_url = f"git@github.com:{github_username}/{project_slug}.git"
    print(f"🔗 Setting remote to: {remote_url}")

    # Add remote (ignore error if already exists)
    subprocess.run(
        f'git remote add origin "{remote_url}"', shell=True, capture_output=True
    )

    if run_command("git push -u origin main", check=False) is not None:
        print("✅ Successfully pushed to GitHub!")
    else:
        print("⚠️  Push failed. Check if the repo exists and your SSH keys are set.")

    # 5. Jupyter kernel
    create_jupyter_kernel(project_slug)

    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
