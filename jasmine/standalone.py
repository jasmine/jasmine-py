import os
import re

from flask import Flask
from flask import render_template, make_response, send_file

from jasmine_core import Core
from jasmine import Config

app = Flask(__name__, template_folder='django/templates')


@app.before_first_request
def init():
    project_path = os.path.realpath(os.path.dirname(__name__))

    config_file = os.path.join(project_path, "spec/javascripts/support/jasmine.yml")

    app.jasmine_config = Config(config_file, project_path=project_path)

    app.filetype_mapping = {
        'jasmine': Core.path,
        'boot': Core.boot_dir,
        'src': app.jasmine_config.src_dir,
        'spec': app.jasmine_config.spec_dir
    }


@app.route("/__<filetype>__/<path:filename>")
def serve(filetype, filename):
    path = os.path.join(os.getcwd(), app.filetype_mapping[filetype](), filename)

    response = make_response(open(path, 'r').read())
    if re.match(r'^.*\.js$', path):
        response.mimetype = 'application/javascript'
    elif re.match(r'^.*\.css$', path):
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

    return render_template('runner.html', **context)

@app.route('/favicon.ico')
def favicon():
    return send_file(Core.favicon_path(), mimetype='image/vnd.microsoft.icon')