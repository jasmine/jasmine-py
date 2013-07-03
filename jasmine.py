import os
import re

from flask import Flask
from flask import render_template, make_response

from jasmine_core import Core
from jasmine import Config

app = Flask(__name__, template_folder='jasmine/templates')

project_path = os.path.realpath(os.path.dirname(__name__))

config_file = os.path.join(project_path, "spec/javascripts/support/jasmine.yml")
config = Config(config_file, project_path=project_path)

filetype_mapping = {
    'core': Core.path,
    'boot': Core.boot_dir,
    'src': config.src_dir,
    'specs': config.spec_dir
}


@app.route("/<filetype>/<path:filename>")
def serve(filetype, filename):
    path = os.path.join(os.getcwd(), filetype_mapping[filetype](), filename)

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
    project_src_dir = os.path.join(project_path, config.src_dir())
    project_spec_dir = os.path.join(project_path, config.spec_dir())

    context = {}

    js_files = \
        ["core/{0}".format(core_js) for core_js in Core.js_files()] +\
        ["boot/{0}".format(boot_file) for boot_file in Core.boot_files()] +\
        ["src/{0}".format(os.path.relpath(src_file, project_src_dir)) for src_file in config.src_files()] +\
        ["specs/{0}".format(os.path.relpath(helper, project_spec_dir)) for helper in config.helpers()] +\
        ["specs/{0}".format(os.path.relpath(spec_file, project_spec_dir)) for spec_file in config.spec_files()]

    css_files = \
        ["core/{0}".format(core_css) for core_css in Core.css_files()] +\
        ["src/{0}".format(os.path.relpath(css_file, project_src_dir)) for css_file in config.stylesheets()]

    context.update({
        'css_files': css_files,
        'js_files': js_files
    })

    return render_template('runner.html', **context)

if __name__ == "__main__":
    app.run(port=8888, debug=True)
