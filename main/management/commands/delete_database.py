from django.core.management import BaseCommand
from django.conf import settings
import os
from django.db import DEFAULT_DB_ALIAS


def delete_database(database: str):
    db_path = settings.DATABASES[database]['NAME']
    if os.path.exists(db_path):
        os.remove(db_path)


class Command(BaseCommand):
    help = """Deletes provided database"""

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='database', nargs='*',
                            help='Restricts deletion to database', )

    def handle(self, *databases, **options):
        databases = databases if databases else [DEFAULT_DB_ALIAS]

        for database in databases:
            delete_database(database)
