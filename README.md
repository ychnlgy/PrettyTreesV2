# PrettyTreesV2
Upgrading from PyGame to Pyglet for shaders!


### Installation
Install **Python 3.11.4** and `pip >= 24.3.1`, then install the development requirements.

```bash
python -m venv ./venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pre-commit install --hook-type pre-commit --hook-type pre-push
```

### Quickstart
```bash
source venv/bin/activate
python -m pretty_trees.main
```

### Testing
```bash
pytest --cov
```

### Config files
 - `.coveragerc`: omits non-essential code for coverage analysis.
 - `.pre-commit-config.yaml`: sets hooks to run during commits and pushes.
 - `.pylintrc`: ignores certain linting rules.
 - `mypy.ini`: ignores certain folders for type checks.
 - `pytest.ini`: ignores certain folders for running tests.
 - `setup.py`: pip installation setup.
 - `MANIFEST.in`: include non-code files.