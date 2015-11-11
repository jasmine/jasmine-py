import mimetypes
import os

import chardet
import pkg_resources
from flask import Flask, render_template_string, make_response, send_file


class JasmineApp(object):

    def __init__(self, jasmine_config=None):
        self.jasmine_config = jasmine_config

        self.filetype_mapping = {
            'src': self.jasmine_config.src_dir(),
            'spec': self.jasmine_config.spec_dir()
        }

        # instance_path set to work around:
        # https://bitbucket.org/hpk42/pytest/issue/317
        self.app = Flask(__name__, instance_path=os.getcwd())
        self.app.debug = True

        self.app.add_url_rule("/__<filetype>__/<path:filename>", 'serve', self.serve)
        self.app.add_url_rule("/", 'run', self.run)
        self.app.add_url_rule('/jasmine_favicon.png', 'favicon', self.favicon)

    def serve(self, filetype, filename):
        if filetype == 'jasmine':
            contents = pkg_resources.resource_string('jasmine_core', filename)
        else:
            path = os.path.join(
                os.getcwd(),
                self.filetype_mapping[filetype],
                filename
            )
            raw_contents = open(path, 'rb').read()
            contents = self._decode_raw(raw_contents)

        response = make_response(contents)
        response.mimetype = mimetypes.guess_type(filename)[0]

        return response

    def run(self):
        self.jasmine_config.reload()
        context = {
            'css_files': self.jasmine_config.stylesheet_urls(),
            'js_files': self.jasmine_config.script_urls()
        }

        template = pkg_resources.resource_string(
            'jasmine.templates',
            'runner.html'
        )

        return render_template_string(template.decode(), **context)

    def favicon(self):
        return send_file(
            pkg_resources.resource_stream(
                'jasmine_core.images',
                'jasmine_favicon.png'
            ),
            mimetype='image/png'
        )

    def _decode_raw(self, raw_contents):
        encoding = chardet.detect(raw_contents)['encoding']
        contents = raw_contents.decode(encoding)
        return contents
