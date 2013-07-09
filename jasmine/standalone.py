import os
import re
import sys
import getopt

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

if __name__ == "__main__":
    port_arg = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:", ["port="])
    except getopt.GetoptError:
        sys.stdout.write('python jasmine/standalone.py -p <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-p', '--port']:
            try:
                port_arg = int(arg)
            except ValueError:
                pass
    port = port_arg if (port_arg and 8000 <= port_arg <= 8999) else 8888
    app.run(port=port, debug=True)
