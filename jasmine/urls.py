import os

from django.conf import settings
from django.conf.urls import patterns, url
from jasmine_core import Core

from jasmine import Config
from .views import JasmineRunner


config = Config(os.path.join(settings.PROJECT_PATH, 'spec/javascripts/support/jasmine.yml'))
spec_dir = os.path.abspath(os.path.join(settings.PROJECT_PATH, config.spec_dir))
src_dir = os.path.abspath(os.path.join(settings.PROJECT_PATH, config.src_dir))

print spec_dir

urlpatterns = patterns(
    '',
    url(r'^specs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': spec_dir, }, name='jasmine_specs'),
    url(r'^src/(?P<path>.*)$', 'django.views.static.serve', {'document_root': src_dir, }, name='jasmine_src'),
    url(r'^boot/(?P<path>.*)$', 'django.views.static.serve', {'document_root': Core.boot_dir(), }, name='jasmine_boot'),
    url(r'^core/(?P<path>.*)$', 'django.views.static.serve', {'document_root': Core.path(), }, name='jasmine_core'),
    url(r'^$', JasmineRunner.as_view(template_name="runner.html")),
)
