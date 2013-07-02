import os
from django.views.generic.base import TemplateView
from jasmine import Config
from jasmine_core import Core

from django.conf import settings

class JasmineRunner(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        config = Config(os.path.join(settings.PROJECT_PATH, 'spec/javascripts/support/jasmine.yml'))
        project_src_dir = os.path.join(settings.PROJECT_PATH, config.src_dir)
        project_spec_dir = os.path.join(settings.PROJECT_PATH, config.spec_dir)

        js_files = []
        css_files = []

        for core_css in Core.css_files():
            css_files.append("core/{}".format(core_css))

        for core_js in Core.js_files():
            js_files.append("core/{}".format(core_js))

        for boot_file in Core.boot_files():
            js_files.append("boot/{}".format(boot_file))


        for src_file in config.src_files():
            js_files.append("src/{}".format(os.path.relpath(src_file, project_src_dir)))

        for helper_file in config.helpers():
            js_files.append("specs/{}".format(os.path.relpath(helper_file, project_spec_dir)))

        for spec_file in config.spec_files():
            js_files.append("specs/{}".format(os.path.relpath(spec_file, project_spec_dir)))

        for css_file in config.stylesheets():
            css_file.append("src/{}".format(os.path.relpath(css_file, project_src_dir)))

        context.update({
            'css_files': css_files,
            'js_files': js_files
        })

        return self.render_to_response(context)