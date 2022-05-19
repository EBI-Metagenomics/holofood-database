[![Testing](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/test.yml/badge.svg)](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/test.yml)

# Holofood Database
The database and website to present [Holofood](https://www.holofood.eu) samples,
and unify the datasets stored in supporting services.

## Background
HoloFood is a consortium and project focussed on understanding the biomolecular 
and physiological processes  triggered by incorporating feed additives and novel
sustainable feeds in farmed animals.

This codebase is the public website and API for browsing the Samples and datasets
created by the project, which are stored in publicly-accessible data repositories. 

The website is built with Django.

Management commands are used to important a cache of Samples and their metadata
from ENA and Biosamples.

There is a normal Django Admin panel as well.

## Development
Install development tools (including pre-commit hooks to run Black code formatting).
```shell
pip install -r requirements-dev.txt
pre-commit install
```

### Code style
Use [Black](https://black.readthedocs.io/en/stable/).

## Testing
```shell
pytest
```

## Configuration
We use [Pydantic](https://pydantic-docs.helpmanual.io/) to formalise Config files.
Configuration is split between:
- `config/local.env` as a convenience for env vars.
- `config/data_config.json` contains what are expected to be somewhat change-able config options.
- `config/secrets.env` is needed during development, whilst some data are private.

## Use
```shell
source config/secrets.env
python manage.py migrate
python manage.py fetch_project_samples
python manage.py refresh_structureddata 
python manage.py runserver
```

## Deployment
TODO