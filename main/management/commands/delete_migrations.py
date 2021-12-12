from django.core.management import BaseCommand
import glob
import shutil


def delete_migrations():
    for migration_path in glob.glob('*/migrations'):
        shutil.rmtree(path=migration_path)


class Command(BaseCommand):
    help = "Deletes all migrations in the project"

    def handle(self, *args, **options):
        delete_migrations()