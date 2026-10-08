from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set up local development environment"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-sample-data",
            action="store_true",
            help="Skip creating the starter pages (home, services, contact)",
        )

    def handle(self, *args, **options):
        self.stdout.write("Running migrations...")
        call_command("migrate")

        self.stdout.write("Creating cache table...")
        call_command("createcachetable")

        if options["no_sample_data"]:
            self.stdout.write(self.style.WARNING("Skipping starter pages."))
        else:
            self.stdout.write("Creating starter pages...")
            call_command("load_initial_data")

        self.stdout.write("Collecting static files...")
        call_command("collectstatic", interactive=False)

        self.stdout.write(self.style.SUCCESS("Local setup complete."))
        self.stdout.write(
            "Create your administrator account with:\npython manage.py createsuperuser"
        )
