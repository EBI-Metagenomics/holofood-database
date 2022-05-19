import logging

from django.core.management.base import BaseCommand, CommandError

from holofood.external_apis.ena.portal_api import get_holofood_samples
from holofood.models import Sample, Project


class Command(BaseCommand):
    help = "(Re)fetches the list of Holofood samples from the ENA API"

    def handle(self, *args, **options):
        projects_samples = get_holofood_samples()
        samples_added = 0
        for project_accession, samples in projects_samples.items():
            logging.info(project_accession)
            logging.info(samples)
            if type(samples) is list and samples:
                project_title = samples[0]["project_name"]
            else:
                project_title = ""
            project, created = Project.objects.update_or_create(
                accession=project_accession, defaults={"title": project_title}
            )
            if created:
                logging.info(f"Created Project {project_accession}")
            for sample in samples:
                _, created = Sample.objects.update_or_create(
                    accession=sample.get("sample_accession"),
                    defaults={"project": project, "title": sample.get("sample_title")},
                )
                if created:
                    samples_added += 1

        self.stdout.write(self.style.SUCCESS(f"Added {samples_added} samples."))
