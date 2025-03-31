# PyVueBot Deployment Guide

This guide outlines the steps to publish PyVueBot to the Python Package Index (PyPI).

## Prerequisites

Before publishing, ensure you have the following:

1. A PyPI account - register at [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Poetry installed - [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)
3. All tests passing and code ready for release
4. Updated version number in both `pyproject.toml` and `pyvuebot/__init__.py`

## Preparation

### 1. Update Version Number

Before deployment, ensure the version number is updated in:

- `pyvuebot/__init__.py`: Update `__version__ = "x.y.z"`
- `pyproject.toml`: Update `version = "x.y.z"`

Example:

```python
# pyvuebot/__init__.py
__version__ = "0.2.0"
```

```toml
# pyproject.toml
[tool.poetry]
name = "pyvuebot"
version = "0.2.0"
# ...
```

### 2. Update CHANGELOG (Recommended)

It's good practice to maintain a CHANGELOG.md file documenting what has changed in each version.

### 3. Ensure README is Up-to-Date

The README.md file is what users will see on PyPI. Make sure it's current and provides all necessary information.

## Building and Publishing

### Using Poetry (Recommended)

Poetry simplifies the package building and publishing process. Follow these steps:

1. **Build the package**:

```bash
poetry build
```

This creates both source distribution (.tar.gz) and wheel (.whl) files in the `dist/` directory.

2. **Publish to TestPyPI first (optional but recommended)**:

Configure Poetry to use TestPyPI:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi <your-testpypi-token>
```

Then publish:

```bash
poetry publish --repository testpypi
```

3. **Publish to PyPI**:

Configure your PyPI token:

```bash
poetry config pypi-token.pypi <your-pypi-token>
```

Then publish:

```bash
poetry publish
```

Or build and publish in one step:

```bash
poetry publish --build
```

### Using Twine (Alternative)

If you prefer using twine instead of Poetry:

1. **Install build and twine**:

```bash
pip install build twine
```

2. **Build the package**:

```bash
python -m build
```

3. **Upload to TestPyPI (optional)**:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

4. **Upload to PyPI**:

```bash
twine upload dist/*
```

## Post-Deployment

### Verify Installation

After publishing, verify that your package can be installed:

```bash
pip install --upgrade pyvuebot
```

### Create a Release Tag

Tag the release in Git:

```bash
git tag -a v0.2.0 -m "Version 0.2.0"
git push origin v0.2.0
```

### Creating a GitHub Release

1. Go to your repository on GitHub
2. Click on "Releases"
3. Click "Draft a new release"
4. Select the tag you just pushed
5. Add release notes
6. Publish the release

## Troubleshooting

### Common Issues

1. **Version already exists**: You cannot upload a package with the same version twice to PyPI. Always increment the version number.
2. **README not rendering properly**: Ensure your README.md is valid Markdown.
3. **Missing dependencies**: Check that all dependencies are correctly listed in `pyproject.toml`.

### Getting Help

If you encounter problems during the deployment process, refer to:

- [Poetry Documentation](https://python-poetry.org/docs/cli/#publish)
- [PyPI Help](https://pypi.org/help/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)

## Release Checklist

Before each release, go through this checklist:

- [ ] Update version number in `pyvuebot/__init__.py` and `pyproject.toml`
- [ ] Update CHANGELOG.md
- [ ] Ensure README.md is up-to-date
- [ ] Run tests to make sure everything works
- [ ] Build and test the package locally
- [ ] Publish to TestPyPI and verify installation
- [ ] Publish to PyPI
- [ ] Create Git tag
- [ ] Create GitHub release
- [ ] Announce the release on relevant channels
