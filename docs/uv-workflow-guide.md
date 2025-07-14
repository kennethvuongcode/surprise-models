# UV Python Package Manager Guide

This guide explains how to work with `uv`, a fast Python package manager and project manager. UV is significantly faster than pip and provides better dependency resolution and project management capabilities.

## What is UV?

UV is a modern Python package manager that:
- Installs packages 10-100x faster than pip
- Provides better dependency resolution
- Manages Python versions and virtual environments
- Handles project dependencies with lock files
- Replaces pip, pip-tools, pipx, poetry, and more

## Installation

### Install UV

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip (if you have Python already)
pip install uv

# Via Homebrew (macOS)
brew install uv
```

### Verify Installation

```bash
uv --version
```

## Project Setup

### Initialize a New Project

```bash
# Create a new project
uv init my-project
cd my-project

# Or initialize in existing directory
uv init
```

This creates:
- `pyproject.toml` - Project configuration and dependencies
- `README.md` - Project documentation
- `src/` - Source code directory
- `.python-version` - Python version specification

### Understanding Project Structure

```
my-project/
├── pyproject.toml      # Project config and dependencies
├── uv.lock            # Lock file (auto-generated)
├── .python-version    # Python version
├── README.md
└── src/
    └── my_project/
        └── __init__.py
```

## Managing Dependencies

### Adding Packages

```bash
# Add a package to dependencies
uv add requests

# Add a specific version
uv add "requests>=2.28.0"

# Add a development dependency
uv add --dev pytest

# Add multiple packages
uv add requests pandas numpy

# Add with extras
uv add "fastapi[all]"

# Add from git repository
uv add git+https://github.com/user/repo.git

# Add from local path
uv add --editable ./local-package
```

### Removing Packages

```bash
# Remove a package
uv remove requests

# Remove a dev dependency
uv remove --dev pytest

# Remove multiple packages
uv remove requests pandas numpy
```

### Upgrading Packages

```bash
# Upgrade a specific package
uv add --upgrade requests

# Upgrade all packages
uv lock --upgrade

# Upgrade and sync
uv sync --upgrade
```

## Working with Virtual Environments

### Automatic Environment Management

UV automatically manages virtual environments for your projects:

```bash
# UV automatically creates and uses a virtual environment
uv add requests  # Creates .venv if it doesn't exist

# Check current environment
uv pip list
```

### Manual Environment Management

```bash
# Create a virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Create in custom location
uv venv .venv-custom

# Activate environment (optional, uv handles this automatically)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

## Installing Dependencies

### Sync Dependencies

```bash
# Install all dependencies from pyproject.toml
uv sync

# Install only production dependencies (skip dev)
uv sync --no-dev

# Install with specific extras
uv sync --extra dev --extra test
```

### Install from Requirements Files

```bash
# Install from requirements.txt
uv pip install -r requirements.txt

# Install from multiple files
uv pip install -r requirements.txt -r dev-requirements.txt
```

## Running Commands

### Running Python Scripts

```bash
# Run a Python script
uv run python script.py

# Run a module
uv run python -m my_module

# Run with arguments
uv run python script.py --arg1 value1
```

### Running Installed Tools

```bash
# Run a tool (like pytest)
uv run pytest

# Run with arguments
uv run pytest tests/ -v

# Run a script defined in pyproject.toml
uv run my-script
```

### Running One-off Commands

```bash
# Run a command with temporary dependencies
uv run --with requests python -c "import requests; print(requests.get('https://httpbin.org/json').json())"

# Run a tool without installing it globally
uv run --with black black --check .
```

## Python Version Management

### Setting Python Version

```bash
# Set Python version for project
uv python pin 3.11

# Use specific Python version
uv python pin 3.11.5

# Install a Python version
uv python install 3.11
```

### Checking Python Versions

```bash
# List available Python versions
uv python list

# Show current Python version
uv python find
```

## Common Workflows

### Starting a New Project

```bash
# 1. Create and navigate to project
mkdir my-project && cd my-project

# 2. Initialize UV project
uv init

# 3. Set Python version
uv python pin 3.11

# 4. Add dependencies
uv add requests pandas

# 5. Add development dependencies
uv add --dev pytest black ruff

# 6. Create your code
mkdir src/my_project
echo "print('Hello, World!')" > src/my_project/main.py

# 7. Run your code
uv run python src/my_project/main.py
```

### Working on an Existing Project

```bash
# 1. Clone the repository
git clone https://github.com/user/repo.git
cd repo

# 2. Install dependencies
uv sync

# 3. Run tests
uv run pytest

# 4. Start development
uv run python src/main.py
```

### Adding a New Feature

```bash
# 1. Add any new dependencies
uv add new-package

# 2. Write your code
# ... make changes ...

# 3. Test your changes
uv run pytest

# 4. Format code
uv run black .
uv run ruff check .
```

## Configuration

### pyproject.toml Example

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
dependencies = [
    "requests>=2.28.0",
    "pandas>=1.5.0",
]
requires-python = ">=3.11"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "ruff>=0.1.0",
]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[project.scripts]
my-script = "my_project.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=22.0.0",
]
```

## Creating CLI Entry Points

Entry points allow you to create command-line utilities that can be run from anywhere after installing your package. This is perfect for creating tools and utilities that your team can use.

### What are Entry Points?

Entry points create executable commands that:
- Are available system-wide after package installation
- Point to specific functions in your code
- Can be run from any directory
- Are automatically added to the system PATH

### Defining Entry Points in pyproject.toml

```toml
[project.scripts]
my-tool = "my_package.cli:main"
data-processor = "my_package.tools.processor:process_data"
model-trainer = "my_package.training:train_model"
```

### Creating CLI Functions

#### Basic CLI Function

```python
# src/my_package/cli.py
import argparse
import sys

def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(description="My awesome CLI tool")
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Processing {args.input} -> {args.output}")
    
    # Your actual logic here
    process_file(args.input, args.output)
    
    if args.verbose:
        print("Processing complete!")

def process_file(input_path, output_path):
    """Process the input file and save to output."""
    # Your processing logic here
    pass

if __name__ == "__main__":
    main()
```

#### Advanced CLI with Click

First, add Click as a dependency:
```bash
uv add click
```

Then create a more sophisticated CLI:

```python
# src/my_package/cli.py
import click
from pathlib import Path

@click.group()
@click.version_option()
def cli():
    """My Package CLI - A tool for awesome things."""
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option("--format", "-f", default="json", help="Output format")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def process(input_file, output_file, format, verbose):
    """Process input file and save to output file."""
    if verbose:
        click.echo(f"Processing {input_file} -> {output_file}")
    
    # Your processing logic
    result = process_data(input_file, format)
    
    with open(output_file, "w") as f:
        f.write(result)
    
    if verbose:
        click.echo("✅ Processing complete!")

@cli.command()
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file")
def train(config):
    """Train a model with optional config file."""
    click.echo("Starting training...")
    # Your training logic
    click.echo("Training complete!")

def process_data(input_file, format):
    """Process data and return formatted result."""
    # Your actual processing logic
    return f"Processed data in {format} format"

if __name__ == "__main__":
    cli()
```

### Complete Example Setup

#### 1. Project Structure
```
my-package/
├── pyproject.toml
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── cli.py          # CLI entry points
│       ├── core.py         # Core functionality
│       └── utils.py        # Utility functions
```

#### 2. pyproject.toml Configuration
```toml
[project]
name = "my-package"
version = "0.1.0"
description = "My awesome package with CLI tools"
dependencies = [
    "click>=8.0.0",
    "requests>=2.28.0",
]

[project.scripts]
my-tool = "my_package.cli:cli"
quick-process = "my_package.cli:process"
train-model = "my_package.cli:train"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
]
```

#### 3. Install and Use
```bash
# Install your package in development mode
uv pip install -e .

# Now you can use your CLI tools from anywhere
my-tool --help
my-tool process input.txt output.txt --verbose
quick-process data.csv results.json --format json
train-model --config config.yaml
```

### Best Practices for CLI Tools

#### 1. Use Clear Command Names
```toml
[project.scripts]
# Good: descriptive and specific
data-validator = "my_package.validation:validate"
model-trainer = "my_package.training:train"
results-analyzer = "my_package.analysis:analyze"

# Avoid: too generic
tool = "my_package.cli:main"
run = "my_package.cli:run"
```

#### 2. Provide Help and Documentation
```python
import click

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", help="Output file path")
@click.option("--format", "-f", default="json", 
              help="Output format (json, csv, txt)")
def process(input_file, output, format):
    """
    Process input file and generate output.
    
    INPUT_FILE: Path to the input data file
    
    Examples:
        my-tool process data.csv --output results.json
        my-tool process data.csv -o results.txt -f txt
    """
    pass
```

#### 3. Handle Errors Gracefully
```python
import sys
import click

def main():
    try:
        # Your logic here
        result = process_data()
        click.echo("✅ Success!")
        return 0
    except FileNotFoundError as e:
        click.echo(f"❌ Error: File not found - {e}", err=True)
        return 1
    except ValueError as e:
        click.echo(f"❌ Error: Invalid input - {e}", err=True)
        return 1
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

#### 4. Use Configuration Files
```python
import click
import json
from pathlib import Path

@click.command()
@click.option("--config", "-c", type=click.Path(exists=True), 
              help="Configuration file path")
def run(config):
    """Run with configuration file."""
    if config:
        with open(config) as f:
            config_data = json.load(f)
    else:
        # Use default config
        config_data = get_default_config()
    
    # Use config_data in your logic
    process_with_config(config_data)
```

### Testing CLI Tools

```python
# tests/test_cli.py
import pytest
from click.testing import CliRunner
from my_package.cli import cli

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "My Package CLI" in result.output

def test_process_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create test input file
        with open("input.txt", "w") as f:
            f.write("test data")
        
        # Run command
        result = runner.invoke(cli, ["process", "input.txt", "output.txt"])
        assert result.exit_code == 0
        
        # Check output file exists
        assert Path("output.txt").exists()
```

### Common CLI Patterns

#### File Processing Tool
```python
@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--output-dir", "-o", type=click.Path(), default="./output")
def batch_process(files, output_dir):
    """Process multiple files."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for file_path in files:
        process_single_file(file_path, output_path)
```

#### Configuration Management
```python
@click.group()
def config():
    """Manage configuration."""
    pass

@config.command()
@click.argument("key")
@click.argument("value")
def set(key, value):
    """Set configuration value."""
    # Save to config file
    pass

@config.command()
@click.argument("key")
def get(key):
    """Get configuration value."""
    # Read from config file
    pass
```

### Integration with UV

```bash
# After adding entry points to pyproject.toml
uv sync  # Install dependencies

# Install your package in development mode
uv pip install -e .

# Run your CLI tools
my-tool --help
uv run my-tool process input.txt output.txt

# Or install from your package
uv add ./my-package
my-tool --version
```

## Best Practices

### 1. Version Pinning

```bash
# Pin exact versions for reproducibility
uv add "requests==2.31.0"

# Use version ranges for flexibility
uv add "requests>=2.28.0,<3.0.0"

# Pin Python version
uv python pin 3.11
```

### 2. Dependency Organization

```bash
# Separate production and development dependencies
uv add requests pandas          # Production
uv add --dev pytest black ruff  # Development

# Use extras for optional features
uv add --extra dev fastapi
```

### 3. Lock Files

```bash
# Always commit uv.lock to version control
git add uv.lock
git commit -m "Update dependencies"

# Regenerate lock file when needed
uv lock --upgrade
```

### 4. Environment Isolation

```bash
# Let UV manage environments automatically
uv sync  # Creates .venv if needed

# Use project-specific environments
# Don't activate manually - let uv handle it
```

## Troubleshooting

### Common Issues

#### Dependencies Not Found
```bash
# Sync dependencies
uv sync

# Check if package is installed
uv pip list | grep package-name
```

#### Python Version Issues
```bash
# Install required Python version
uv python install 3.11

# Set project Python version
uv python pin 3.11
```

#### Lock File Conflicts
```bash
# Regenerate lock file
rm uv.lock
uv lock

# Force sync
uv sync --reinstall
```

#### Virtual Environment Issues
```bash
# Remove and recreate environment
rm -rf .venv
uv sync
```

## Command Reference

### Package Management
```bash
uv add <package>              # Add package
uv remove <package>           # Remove package
uv sync                       # Install dependencies
uv lock                       # Generate lock file
uv pip list                   # List installed packages
```

### Environment Management
```bash
uv venv                       # Create virtual environment
uv python pin <version>       # Set Python version
uv python install <version>   # Install Python version
uv python list                # List Python versions
```

### Running Commands
```bash
uv run <command>              # Run command in environment
uv run python <script>        # Run Python script
uv run --with <pkg> <cmd>     # Run with temporary dependency
```

### Project Management
```bash
uv init                       # Initialize new project
uv build                      # Build project
uv publish                    # Publish to PyPI
```

## Migration from Other Tools

### From pip + requirements.txt

```bash
# Convert requirements.txt to pyproject.toml
uv add $(cat requirements.txt | xargs)

# Or import directly
uv pip install -r requirements.txt
```

### From Poetry

```bash
# UV can read poetry.lock files
uv sync  # Reads existing poetry.lock

# Or migrate manually
uv add $(poetry show --no-dev | cut -d' ' -f1 | xargs)
```

### From Pipenv

```bash
# Convert Pipfile to pyproject.toml
uv add $(pipenv requirements | xargs)
```

## Tips for Success

1. **Always use `uv sync`** after pulling changes
2. **Commit `uv.lock`** to version control
3. **Use `uv run`** instead of activating environments manually
4. **Pin Python versions** for consistency across team
5. **Separate dev and production dependencies**
6. **Use `--dev` flag** for development-only packages
7. **Check `uv.lock`** when dependencies don't match expectations

Remember: UV is designed to be fast and reliable. When in doubt, `uv sync` will usually fix dependency issues! 