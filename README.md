[![Testing](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/test.yml/badge.svg)](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/EBI-Metagenomics/holofood-database/branch/main/graph/badge.svg?token=27IVW899W8)](https://codecov.io/gh/EBI-Metagenomics/holofood-database)
[![Build & Publish Docs](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/docs.yml/badge.svg)](https://github.com/EBI-Metagenomics/holofood-database/actions/workflows/docs.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)
[![DOI](https://zenodo.org/badge/475986161.svg)](https://zenodo.org/badge/latestdoi/475986161)


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
Use [djLint](https://djlint.com/).
These are both configured if you install the pre-commit tools as above.

To manually run them:
`black .` and `djlint . --extension=html --lint` (or `--reformat`).

### Fake data
Once a database is created and migrated (see below), there is a management command to fill the database
with some minimal fake data for development ease. 
```shell
python manage.py generate_dev_data
```

## Testing
```shell
# You most likely need (see below):
#   brew install chromedriver
pip install -r requirements-dev.txt
pytest
```

### Chrome Driver for web interface tests
The web interface tests need the Chrome browser and `chromedriver` to communicate with the browser.
To install `chromedriver` on a Mac or Linux machine, [use the Homebrew formula](https://formulae.brew.sh/cask/chromedriver)
or any other sensible installation method. On GitHub Actions, a "Setup Chromedriver" action step exists for this.
On a Mac, you’ll probably get Gate Keeper permissions problems running `chromedriver`; so:
```shell
which chromedriver  # probably: /usr/local/bin/chromedriver
spctl --add /usr/local/bin/chromedriver
```
If this doesn't work, `open /usr/local/bin`, then find `chromedriver` in Finder, right click, Open.

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
python manage.py refresh_external_data
python manage.py runserver
```
TODO: update README once importer supports hierarchical samples

### Refreshing external data
`refresh_external_data` has several options, for fetching data for some or all samples/projects, 
and for fetching data from some or all supporting APIs.

To (re)fetch sample metadata from ENA and Biosamples only, for a specific sample:

`python manage.py refresh_external_data --samples SAMEA7687881 --types METADATA`

or to refresh metagenomic data for all sample in a project:

`python manage.py refresh_external_data --projects PRJEB39110 --types METAGENOMIC`

(Note that it is **much** more efficient to fetch metagenomics data on a per-project basis than a per-sample basis
– this is because it uses many fewer API calls and the MGnify API has strict rate-limits.)

Or to (re)fetch sample metadata and metagenomic existence data from ENA, Biosamples, and MGnify, 
for samples with accessions in a certain range:

`python manage.py refresh_external_data --sample_filters accession__gt=SAMEA7687880 accession__lt=SAMEA7687900 --types METADATA METAGENOMIC`

`--sample_filters...` is expected to be useful in cases where refreshing a large number of samples fails, 
and you therefore need to retry from a certain accession onwards.
(Because samples are iterated through in ascending order of accession.) 

### Import catalogues
MAG and Viral catalogues can be imported using management commands.
Each MAG catalogue needs to relate to a single public MAG catalogue on MGnify; 
in that the species representative of each MAG must exist on MGnify.
Each Viral Catalogue must relate (biome-wise) to a single MAG catalogue on the portal.
In other words, the order of data insertion needs to be:

- public MAG catalogue into MGnify
- MAG catalogue into this data portal
- Viral catalogue into this data portal

The uploaders expect TSV files (and a folder of GFFs in the case of viral catalogue).
For the format / column naming, inspect the files in `holofood/tests/static_fixtures`.

Run `python manage.py import_mag_catalogue` or `import_viral_catalogue` for help, but essentially:

```shell
python manage.py import_mag_catalogue hf-salmon-mags-v1 ./salmon.tsv "HoloFood Salmon V1" mgnify-salmon-v1-0 "Some:Biome:String" salmon
python manage.py import_viral_catalogue hf-salmon-vir-v1 './salmon_viral_cat.tsv' './salmon_viral_annotations.gff' --title="HoloFood Salmon Viruses V1" --related_mag_catalogue_id=hf-salmon-mags-v1
```
The `import_viral_catalogue` command can be run multiple times to populate the catalogue with several TSV/GFF combinations if needed –
fragments are appended to the existing catalogue if it already exists.

### Adding users
Superusers can do everything in the admin panel, including managing other users.
```shell
python manage.py createsuperuser
```
Superusers can go to e.g. http://localhost:8000/admin and create other users there.

"Staff" users can access the admin panel, but won't by default have permissions to do anything there.
Add them to the "authors" user group to give them permissions to author "Analysis Summary" documents via the admin panel.


## Deployment
### AWS Elastic Beanstalk
The Django application can be deployed to AWS Cloud via [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/),
a scalable web app deployment service.

There is an Elastic Beanstalk configuration in `.ebextensions/django.config`.
This config will migrate the db on deployment, as well as compile scss styles and collect static files.

Run `pip install -r requirements-aws.txt` to install the CLI tool for EB.

Create an 
[Elastic Beanstalk environment](https://eu-west-1.console.aws.amazon.com/elasticbeanstalk/home?region=eu-west-1#/environments).
You need a `Python 3.8 on Amazon Linux 2` platform, and an RDS Postgres database (a `db.t4g.micro` instance is fine).

Run `eb use <whatever-the-name-of-your-elastic-beanstalk-environment-is>`, e.g.
`eb use holofood-data-portal-dev-env`.

Deploy the latest git commit with `eb deploy`

To log into the lead instance e.g. to run management commands: 
```shell
eb ssh
cd /var/app/current
source ../venv/*/bin/activate
export $(/opt/elasticbeanstalk/bin/get-config --output YAML environment |  sed -r 's/: /=/' | xargs)
# ^ this sources the env vars
python manage.py ...
```

Secret environment variables can be configured in the 
[AWS EB Console](https://eu-west-1.console.aws.amazon.com/elasticbeanstalk/home?region=eu-west-1#/environments).

#### EBI-specific info
If using the EBI AWS cloud, via an SSO login.
Refer to 
[the Confluence page on AWS SSO](https://www.ebi.ac.uk/seqdb/confluence/display/CCT/AWS+SSO+Authentication+and+Authorisation)
for the SSO parameters. Use `aws configure sso --profile eb-cli` to sign in.
Occasionally you’ll need `aws sso login --profile eb-cli` to get a new token.

### Kubernetes
#### Local
- Use [`minikube`](https://minikube.sigs.k8s.io/docs/start/) or [`kind`](https://kind.sigs.k8s.io).
- Make a secrets .env file at `k8s/secrets-k8s.env` with e.g. `DJANGO_SECRET_KEY`.
- `kubectl create secret generic holofood-secret --from-env-file=k8s/secrets-k8s.env`
- `minikube image build -t holofood -f k8s/Dockerfile .`
- `kubectl apply -f k8s`
- `kubectl get pods -A` and find the pod ID for `holofood-app-...`
- `kubectl exec --stdin --tty holofood-app-......... -- /bin/bash`
- `python manage.py migrate` will make the `/app/data/db.sqlite3`
- `minikube service holofood`

#### EBI WebProd k8s
- EBI operates a two-clusters-per-service policy (primary in "HL" data centre a.k.a. "HH" in some places, fallback in "HX"). The app needs to be deployed to both. There are stub configs in `k8s-hl` and `k8s-hx` for these.
- K8s cluster configurations are provided as YML files by EBI's webprod team. You need these to deploy.
- Build the image (with some customisation for EBI's NFS filesystem): `docker build -f k8s-hl/Dockerfile -t quay.io/microbiome-informatics/holofood-data-portal:ebi-k8s-hl .`
- `docker push quay.io/microbiome-informatics/holofood-data-portal:ebi-k8s-hl` (you need appropriate Quay credentials for this).
- Make a secrets .env file at `k8s-hl/secrets-k8s.env` with e.g. `DJANGO_SECRET_KEY=....`.
	- Push it with e.g.: `kubectl --kubeconfig ~/webprod-configs/mgnify-k8s-team-admin-hh.conf --namespace holofood-hl-prod create secret generic holofood-secret --from-env-file=k8s-hl/secrets-k8s.env`
- Get authentication credentials for quay.io (the built image is private). You can get a Kubernetes secrets yaml file from your Quay.io user settings, in the "CLI Password" section.
	- Download the secrets yaml and name the secret `name: quay-pull-secret` in the metadata section. Put this into the `k8s-hl` folder.
- Deploy: `kubectl --kubeconfig ~/webprod-configs/mgnify-k8s-team-admin-hh.conf apply -f k8s-hl`. If the namespace doesn't exist, you might need to apply twice.

## Documentation
There is an [Quarto](https://www.quarto.org/) based documentation pack in the `docs/` folder,
configured by `docs/_quarto.yml`.

This uses a mixture of [Markdown](https://quarto.org/docs/authoring/markdown-basics.html) 
and rendered [Jupyter Notebooks](https://jupyter.org/).
(This choice allows a code-based tutorial to be included in the docs as well as run by users.)

To develop documentation:

### To make some small text changes
Just edit the `.qmd` (essentially just Markdown) files, and commit to GitHub.
GitHub Actions will render your changes to the 
[GitHub Pages site](https://ebi-metagenomics.github.io/holofood-database/).
(Because there is a `.github/workflows/docs.yml` action to do this.)

### To preview changes, or change a Jupyter Notebook
[Install Quarto](https://quarto.org/docs/get-started/) on your system.

```shell
pip install -r requirements-docs.txt
jupyter lab
```
and edit the `.qmd` or `.ipynb` files in `docs/`.

Run
```shell
quarto preview docs
```
to open a live-preview of the documentation site that updates as you save changes.

If you add a new file (page), add it to the navigation by editing the 
`website.sidebar.contents` list in `docs/_quarto.yml`.

**Note**: any Jupyter Notebooks will be rendered to the documentation site _exactly_ as you leave them.
This is because 
[Quarto defaults to not executing Jupyter Notebooks during rendering](https://quarto.org/docs/projects/code-execution.html#notebooks)
which is a good thing.
If you've added any executable Quarto docs other than Jupyter Notebooks (like an R script...) run `quarto render docs`
and commit the `docs/_freeze/` dir.
