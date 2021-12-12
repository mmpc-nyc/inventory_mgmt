from django.core.management import call_command, BaseCommand


class Command(BaseCommand):
    help = 'Loads data from fixtures/db created by the autodump command'

    def handle(self, **kwargs):
        call_command('loaddata', 'fixtures/db')