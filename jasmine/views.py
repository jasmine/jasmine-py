from django.views.generic.base import TemplateView
from django.conf import settings

import os

from jasmine_core import Core


class JasmineRunner(TemplateView):
    config = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        project_src_dir = os.path.join(settings.PROJECT_PATH, self.config.src_dir)
        project_spec_dir = os.path.join(settings.PROJECT_PATH, self.config.spec_dir)

        js_files = \
            ["core/{}".format(core_js) for core_js in Core.js_files()] +\
            ["boot/{}".format(boot_file) for boot_file in Core.boot_files()] +\
            ["src/{}".format(os.path.relpath(src_file, project_src_dir)) for src_file in self.config.src_files()] +\
            ["specs/{}".format(os.path.relpath(helper, project_spec_dir)) for helper in self.config.helpers()] +\
            ["specs/{}".format(os.path.relpath(spec_file, project_spec_dir)) for spec_file in self.config.spec_files()]

        css_files = \
            ["core/{}".format(core_css) for core_css in Core.css_files()] +\
            ["src/{}".format(os.path.relpath(css_file, project_src_dir)) for css_file in self.config.stylesheets()]

        context.update({
            'css_files': css_files,
            'js_files': js_files
        })

        return self.render_to_response(context)