[![Testing](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/test.yml/badge.svg)](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/EBI-Metagenomics/holofood-database/branch/main/graph/badge.svg?token=27IVW899W8)](https://codecov.io/gh/EBI-Metagenomics/holofood-database)

# Holofood Data Portal / Database
The database, website, and API to present [Holofood](https://www.holofood.eu) samples,
and unify the datasets stored in supporting services.

## Background
HoloFood is a consortium and project focussed on understanding the biomolecular 
and physiological processes  triggered by incorporating feed additives and novel
sustainable feeds in farmed animals.

This codebase is the public website and API for browsing the Samples and datasets
created by the project, which are stored in publicly-accessible data repositories. 

The website is built with Django.

Management commands are used to import a cache of Samples and their metadata
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
pip install -r requirements-dev.txt
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
python manage.py create_authors_user_group   
python manage.py runserver
```

## Adding users
Superusers can do everything in the admin panel, including managing other users.
```shell
python manage.py createsuperuser
```
Superusers can go to e.g. http://localhost:8000/admin and create other users there.

"Staff" users can access the admin panel, but won't by default have permissions to do anything there.
Add them to the "authors" user group to give them permissions to author "Annotation" documents via the admin panel.
Note that this relies on having run `python manage.py create_authors_user_group` to create such a permissioned group.


## Deployment
TODO

## Documentation
There is an [mkdocs](https://www.mkdocs.org/) based documentation pack in the `docs/` folder
configured by `mkdocs.yml`.
This is suitable for serving on [ReadTheDocs](https://readthedocs.org/).

To develop documentation:
```shell
pip install -r requirements-docs.txt
mkdocs serve
```
and edit the Markdown files in `docs/*.md`.

If you add a new file (page), add it to the navigation by editing the `nav` field of `mkdocs.yml`.