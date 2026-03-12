# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Pipelines](#pipelines)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Versioning](#versioning)
- [Authors](#authors)
- [Contact](#contact)

## Overview

This project is a machine learning pipeline template designed for production-ready ML workflows. It includes pre-configured pipelines for data preprocessing, model training, scoring, and monitoring.

## Project Structure

```
{{cookiecutter.project_slug}}/
├── .venv/                             # The virtual environment folder
├── .github/workflows/
│   └── pylint-precommit-pytest.yaml   # GitHub Actions CI/CD workflows
├── data/                              # Data files for exploration
├── notebooks/                         # Jupyter notebooks for exploration
├── src/
│   └── pipelines/
│       ├── preprocessing.py           # Data preprocessing pipeline
│       ├── training.py                # Model training pipeline
│       ├── scoring.py                 # Model scoring pipeline
│       ├── production.py              # Production pipeline
│       ├── postprocessing.py          # Post-processing pipeline
│       └── monitoring.py              # Model monitoring pipeline
├── test/
│   ├── conftest.py                    # Pytest configuration and fixtures
│   └── test_one.py                    # Example test cases
├── .env                               # Environment variables file (.gitignored)
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
├── .pre-commit-config.yaml            # Pre-commit hooks configuration
├── pyproject.toml                     # UV dependencies and project config
├── README.md                          # This file
└── uv.lock                            # The uv lock file
```

## Prerequisites

- **Python**: >= 3.12
- **UV**: For dependency management ([Installation Guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Git**: For version control

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}.git
cd {{cookiecutter.project_slug}}
```

### 2. Install Dependencies

Using UV (recommended):

```bash
uv venv
uv lock
uv sync
```

This will install all project dependencies including development tools.

### 3. Activate the Virtual Environment

- Navigate to your project file
```bash
cd YourProjectFile
```

- For Windows OS:
```bash
source .venv\Scripts\activate
```

- For MacOS:
```bash
source .venv/bin/activate
```

### 4. Set Up Pre-commit Hooks

```bash
pre-commit install
```

Pre-commit hooks will automatically run on every commit to ensure code quality.

## Configuration

### Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your specific configuration values. **Important**: Never commit `.env` to version control (it's already in `.gitignore`).

### Project Configuration

Key configuration files:

- **`pyproject.toml`**: Project metadata, dependencies, and tool configurations (flake8, mypy, pylint, pytest)
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration

## Usage

### Running Pipelines

Each pipeline module can be run independently:

#### Preprocessing Pipeline

```bash
poetry run python src/pipelines/preprocessing.py \
    --input_data <path_to_input> \
    --output_data <path_to_output> \
    --filename <data_filename>
```

#### Training Pipeline

```bash
poetry run python src/pipelines/training.py \
    --input_data <path_to_input> \
    --output_data <path_to_output> \
    --filename <data_filename>
```

#### Scoring Pipeline

```bash
poetry run python src/pipelines/scoring.py \
    --input_data <path_to_input> \
    --output_data <path_to_output> \
    --filename <data_filename>
```

#### Production Pipeline

```bash
poetry run python src/pipelines/production.py \
    --output_data <path_to_output> \
    --outfile_format_string <format_string>
```

### Using Pipeline Functions

You can also import and use pipeline functions in your own scripts:

```python
from src.pipelines.preprocessing import preprocessing_pipeline
from src.pipelines.training import training_pipeline
import pandas as pd

# Load your data
data = pd.read_csv("your_data.csv")

# Run preprocessing
preprocessed_data = preprocessing_pipeline(data)

# Run training
trained_model = training_pipeline(preprocessed_data)
```

## Development

### Code Quality Tools

This project uses several tools to maintain code quality:

- **Black**: Code formatting (line length: 110)
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pylint**: Additional linting

### Running Code Quality Checks

```bash
# Format code
uv run black src/ test/

# Sort imports
uv run isort src/ test/

# Run linters
uv run flake8 src/ test/
uv run pylint src/

# Type checking
uv run mypy src/
```

### Pre-commit Hooks

Pre-commit hooks run automatically on commit. To run manually:

```bash
uv run pre-commit run --all-files
```

## Testing

### Running Tests

Run all tests:

```bash
uv run pytest
```

Run with verbose output:

```bash
uv run pytest -v
```

Run specific test file:

```bash
uv run pytest test/test_one.py
```

Run with coverage:

```bash
uv run pytest --cov=src --cov-report=html
```

### Writing Tests

- Place test files in the `test/` directory
- Test files should start with `test_` or end with `_test.py`
- Use pytest fixtures defined in `conftest.py`
- Follow the existing test structure in `test_one.py`

## Pipelines

### Available Pipelines

1. **Preprocessing** (`preprocessing.py`): Data cleaning, transformation, and feature engineering
2. **Training** (`training.py`): Model training and validation
3. **Scoring** (`scoring.py`): Model inference and prediction
4. **Production** (`production.py`): Production-ready pipeline orchestration
5. **Postprocessing** (`postprocessing.py`): Post-prediction processing and formatting
6. **Monitoring** (`monitoring.py`): Model performance monitoring and logging

### Pipeline Architecture

Each pipeline follows a consistent structure:

- **Pipeline function**: Core logic (e.g., `preprocessing_pipeline()`)
- **Argument parser**: Command-line interface configuration
- **Main block**: Execution logic with Azure ML integration support

### Customizing Pipelines

1. Modify the pipeline function to implement your specific logic
2. Update argument parsers if you need additional parameters
3. Adjust input/output handling as needed
4. Add logging and error handling

## Deployment

### CI/CD

This project includes GitHub Actions workflows (`.github/workflows/`) for:

- Running tests
- Code quality checks (pylint, pre-commit hooks)
- Automated testing on pull requests

### Production Deployment

For production deployment:

1. Ensure all environment variables are properly configured
2. Run tests: `uv run pytest`
3. Check code quality: `uv run pre-commit run --all-files`
4. Build and deploy according to your deployment strategy

### Azure ML Integration

The pipelines are designed to work with Azure Machine Learning. To use Azure ML:

1. Configure Azure ML workspace credentials
2. Update pipeline scripts to use Azure ML datasets
3. Deploy using Azure ML pipelines or endpoints

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Ensure tests pass: `uv run pytest`
4. Run pre-commit hooks: `uv run pre-commit run --all-files`
5. Commit your changes: `git commit -m "Add your feature"`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Versioning

Current version: **{{cookiecutter.version}}**

This project follows [Semantic Versioning](https://semver.org/).

## Authors

**{{cookiecutter.full_name}}**

## Contact

For questions or support, please contact:

- **{{cookiecutter.full_name}}**: {{cookiecutter.email}}

