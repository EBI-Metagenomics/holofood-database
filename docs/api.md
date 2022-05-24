# API for programmatic access

APIs (Application Programming Interfaces) allow programmatic access to data resources.
If you need to fetch and analyse metadata for many Samples, 
you can write a script to fetch data in this way.

The [HoloFood Data Portal API]() 
gives programmatic access to the HoloFood Samples and their metadata,
as well as URLs for where datasets are stored in public archives.

## Canonical URLs
Throughout the API, `canonical_url`s are returned which point to the canonical database entry, 
i.e. the authoritative source,  for each data object.

These are:
- The [European Nucleotide Archive Browser](https://www.ebi.ac.uk/ena/browser/home) for Samples and Projects.
- [MGnify](https://www.ebi.ac.uk/metagenomics) for metagenomic-derived analyses and MAGs (metagenome assembled genomes)
- [MetaboLights](https://www.ebi.ac.uk/metabolights/) for metabolomic analyses
- The websites of various partner institutions and registries where an [IRI](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier) has been supplied with a metadata entry.
- The HoloFood Data Portal itself for "Annotations", which are documents hosted only by this website.

## API Endpoints and Playground
TODO

