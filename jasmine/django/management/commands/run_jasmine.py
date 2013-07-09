from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from jasmine.ci import CIRunner

        CIRunner().run()