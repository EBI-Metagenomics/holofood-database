from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates an 'Authors' user group and assigns permissions for them to create Annotation documents."

    def handle(self, *args, **options):
        authors_group, created = Group.objects.get_or_create(name="authors")
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Authors group"))

        for perm_codename in [
            "view_sample",
            "view_project",
            "add_sampleannotation",
            "view_sampleannotation",
            "change_sampleannotation",
        ]:
            try:
                perm = Permission.objects.get(codename=perm_codename)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"No permission exists called {perm_codename}. Have you migrated?"
                    )
                )
                raise CommandError()

            authors_group.permissions.add(perm)
            self.stdout.write(
                self.style.SUCCESS(f"Granted Authors group perm to {perm_codename}")
            )
