from django.conf import settings


def pytest_configure():
    settings.configure(
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        TEMPLATE_DIRS=('/templates',),
        PROJECT_PATH="/",
        INSTALLED_APPS=('jasmine',),
        JASMINE_YAML='jasmine.yml'
    )