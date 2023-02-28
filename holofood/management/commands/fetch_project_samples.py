import logging
from itertools import groupby

from django.core.management.base import BaseCommand, CommandError

# from holofood.external_apis.ena.portal_api import get_holofood_readruns
# from holofood.models import Sample, Project


class Command(BaseCommand):
    help = (
        "(Re)fetches the list of Holofood samples from the ENA API."
        "Technically fetches `read_run`s from ENA rather than `sample`s."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--projects",
            type=str,
            help="Project accessions, if only some should be updated",
            nargs="+",
            metavar="ACCESSION",
        )

    @staticmethod
    def _sample_for_run(run):
        return run["sample_accession"]

    def handle(self, *args, **options):
        # TODO
        pass
        # if options["projects"]:
        #     projects_runs = get_holofood_readruns(options["projects"])
        # else:
        #     projects_runs = get_holofood_readruns()
        # samples_added = 0
        # samples_updated = 0
        # for project_accession, runs in projects_runs.items():
        #     if type(runs) is list and runs:
        #         project_title = runs[0]["project_name"]
        #     else:
        #         project_title = ""
        #     project, project_created = Project.objects.update_or_create(
        #         accession=project_accession, defaults={"title": project_title}
        #     )
        #     if project_created:
        #         logging.info(f"Created Project {project_accession}")
        #
        #     project_samples_fetched = 0
        #     for sample_accession, sample_runs_iter in groupby(
        #         sorted(runs, key=self._sample_for_run), key=self._sample_for_run
        #     ):
        #         sample_runs = list(sample_runs_iter)
        #         sample = sample_runs[0]
        #         run_accessions = map(lambda run: run["run_accession"], sample_runs)
        #         _, created = Sample.objects.update_or_create(
        #             accession=sample.get("sample_accession"),
        #             defaults={
        #                 "project": project,
        #                 "title": sample.get("sample_title"),
        #                 "ena_run_accessions": list(run_accessions),
        #             },
        #         )
        #         if created:
        #             samples_added += 1
        #         else:
        #             samples_updated += 1
        #         project_samples_fetched += 1
        #
        #     if not project_created:
        #         # Sanity check whether samples count has changed
        #         project.refresh_from_db()
        #         project_samples_total = project.sample_set.count()
        #
        #         if project_samples_total != project_samples_fetched:
        #             self.stdout.write(
        #                 self.style.WARNING(
        #                     f"Project has {project_samples_total} samples, which differs "
        #                     f"from this fetch ({project_samples_fetched} samples)"
        #                 )
        #             )
        #
        # self.stdout.write(self.style.SUCCESS(f"Added {samples_added} samples."))
        # self.stdout.write(
        #     self.style.SUCCESS(f"Touched/updated {samples_updated} samples.")
        # )
