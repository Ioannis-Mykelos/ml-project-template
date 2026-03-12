# ML Project Template

A cookiecutter template for creating standardized machine learning projects with best practices, pre-configured tooling, and a clean project structure.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Setup](#project-setup)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Additional Resources](#additional-resources)

## Prerequisites

### Install Cookiecutter

Cookiecutter is required to generate projects from this template. Install it using one of the following methods:

**Using pip:**
```bash
pip install cookiecutter
```

**Using Homebrew (macOS):**
```bash
brew install cookiecutter
```

**Using Conda:**
```bash
conda install cookiecutter
```

For more installation options, see the [official documentation](https://cookiecutter.readthedocs.io/en/1.7.2/installation.html).

## Installation

### Option 1: Use from GitHub (Recommended)

Generate a project directly from the GitHub repository:

```bash
cookiecutter git@github.com:Ioannis-Mykelos/ml-project-template.git
```

To use a specific branch:

```bash
cookiecutter git@github.com:Ioannis-Mykelos/ml-project-template.git --checkout dev
```

### Option 2: Use Local Clone

If you prefer to work with a local copy of the template:

```bash
git clone https://github.com/Ioannis-Mykelos/ml-project-template.git
# or using SSH:
git clone git@github.com:Ioannis-Mykelos/ml-project-template.git
```

Then generate a project from the local template:

```bash
cookiecutter ml-project-template
```

> **Note:** If you want the project to be automatically pushed to a repository, create an empty repository with the same name as your project before generating.

## Usage

### Step 1: Navigate to Your Desired Directory

```bash
cd /path/to/your/projects/directory
```

### Step 2: Generate the Project

Run cookiecutter with the template URL or local path (see [Installation](#installation) above).

### Step 3: Configure Project Parameters

When prompted, provide the following information:

| Parameter | Description | Notes |
|-----------|-------------|-------|
| `full_name` | Your full name | Default value shown in brackets `[]` |
| `email` | Your email address | Default value shown in brackets `[]` |
| `short_name` | Short name/identifier | Auto-generated from email by default |
| `github_username` | GitHub username | Press Enter for default organization repo |
| `project_name` | Project name | **Must match** your empty repository name if pushing to a repo |
| `project_slug` | URL-friendly project identifier | Auto-generated from `project_name` (press Enter to accept) |
| `project_short_description` | Brief project description | Optional |
| `version` | Project version | Optional (default: 1.0.0) |

**Important Notes:**
- Values in brackets `[]` are defaults - press Enter to accept them
- If you plan to push to a repository, ensure `project_name` matches the repository name
- The `project_slug` is automatically generated from `project_name` (lowercase, spaces/hyphens converted)

**Example:**
```
full_name [John Doe]: Jane Smith
email [johndoe@gmail.com]: jane@example.com
short_name [jane]:
github_username [nuuday]:
project_name [My Project]: ml-sentiment-analysis
project_slug [my-project]:
project_short_description [Amazing stuff going on]: Sentiment analysis model
version [1.0.0]:
```

## Project Setup

After generating your project:

1. **Post-generation hook runs automatically:**
   - The template includes a post-generation hook that automatically:
     - Configures git with your name and email
     - Initializes a git repository
     - Creates an initial commit
     - Sets up the remote origin (if GitHub username and project slug are provided)
     - Attempts to push to GitHub (will fail gracefully if the repo doesn't exist yet)
   - **Windows users:** The Python hook (`post_gen_project.py`) will run automatically if Python is installed
   - **Unix/Linux/macOS users:** The bash hook (`post_gen_project.sh`) will run automatically

2. **Navigate into the project directory:**
   ```bash
   cd your-project-name
   ```

3. **Install dependencies using UV:**
   For more information on using `UV`, see [README_uv.md](README_uv.md).

4. **Set up pre-commit hooks** (see [Pre-commit Hooks](#pre-commit-hooks) below)

## Pre-commit Hooks

This template includes pre-configured pre-commit hooks for code quality and consistency.

### Installation

1. **Install pre-commit:**
   ```bash
   pip install pre-commit
   ```
   Or if using uv:
   ```bash
   uv add pre-commit --group dev
   ```

2. **Install the hooks:**
   ```bash
   pre-commit install
   ```

### What's Included

The pre-commit configuration includes:
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **Pre-commit hooks** - File checks (YAML, JSON, trailing whitespace, etc.)

### Usage

Pre-commit hooks run automatically on every `git commit`. No need to re-install if you modify `.pre-commit-config.yaml` - changes are automatically applied.

To manually run hooks on all files:
```bash
pre-commit run --all-files
```

### Adding to Existing Projects

To add these pre-commit hooks to an existing project:

1. Copy `.pre-commit-config.yaml` to your project root
2. Run `pre-commit install` as described above

## Additional Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/getting-started/)
- [Pre-commit Documentation](https://pre-commit.com/)
