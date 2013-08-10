import os
import re
import pkg_resources

from flask import Flask, render_template_string, make_response, send_file

from jasmine_core import Core
from jasmine.config import Config

# instance_path set to work around: https://bitbucket.org/hpk42/pytest/issue/317
app = Flask(__name__, instance_path=os.getcwd())
app.debug = False


@app.before_first_request
def init():
    project_path = os.path.realpath(os.path.dirname(__name__))

    config_file = os.path.join(project_path, "spec/javascripts/support/jasmine.yml")

    if not os.path.exists(config_file):
        print("Could not find your config file at {0}".format(config_file))

    app.jasmine_config = Config(config_file, project_path=project_path)

    app.filetype_mapping = {
        'src': app.jasmine_config.src_dir,
        'spec': app.jasmine_config.spec_dir
    }


@app.route("/__<filetype>__/<path:filename>")
def serve(filetype, filename):
    if filetype == 'jasmine':
        contents = pkg_resources.resource_string('jasmine_core', filename)
    else:
        path = os.path.join(os.getcwd(), app.filetype_mapping[filetype](), filename)
        contents = open(path, 'r').read()

    response = make_response(contents)
    if re.match(r'^.*\.js$', filename):
        response.mimetype = 'application/javascript'
    elif re.match(r'^.*\.css$', filename):
        response.mimetype = 'text/css'
    else:
        response.mimetype = 'application/octet-stream'

    return response


@app.route("/")
def run():
    context = {
        'css_files': app.jasmine_config.stylesheet_urls(),
        'js_files': app.jasmine_config.script_urls()
    }

    template = pkg_resources.resource_string('jasmine.django.templates', 'runner.html')

    return render_template_string(template, **context)

@app.route('/jasmine_favicon.png')
def favicon():
    return send_file(pkg_resources.resource_stream('jasmine_core.images', 'jasmine_favicon.png'), mimetype='image/png')