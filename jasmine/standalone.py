import mimetypes
import os
import cherrypy
from jinja2 import Environment
import pkg_resources


class JasmineApp(object):

    def __init__(self, jasmine_config=None):
        self.jasmine_config = jasmine_config
        self.jinja_env = Environment()
        self.jasmine_file = JasmineFile()

    @cherrypy.expose
    def index(self, **kwargs):
        self.jasmine_config.reload()
        context = {
            'css_files': self.jasmine_config.stylesheet_urls(),
            'js_files': self.jasmine_config.script_urls()
        }

        template = self.jinja_env.from_string(pkg_resources.resource_string(
            'jasmine.templates',
            'runner.html'
        ).decode())

        return template.render(**context)

    def _cp_dispatch(self, vpath):
        if vpath[0] == '__jasmine__':
            vpath.pop(0)
            if len(vpath) == 1 and vpath[0] == 'jasmine_favicon.png':
                vpath.pop()
                cherrypy.request.params['path'] = 'jasmine_favicon'
            else:
                cherrypy.request.params['path'] = "/".join(vpath)
                vpath[:] = []
            return self.jasmine_file

        return vpath

    def run(self, host='127.0.0.1', port=8888, blocking=False):
        cherrypy.config.update({
            'server.socket_host': host,
            'server.socket_port': port
        })
        cherrypy.tree.mount(self, '/', {
                '/__src__':
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.abspath(self.jasmine_config.src_dir())
                },
                '/__spec__':
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.path.abspath(self.jasmine_config.spec_dir())
                }
            }
        )
        cherrypy.engine.signals.subscribe
        cherrypy.engine.start()
        if blocking:
            cherrypy.engine.block()

    def stop(self):
        cherrypy.engine.stop()


class JasmineFile(object):
    @cherrypy.expose
    def index(self, path):
        if path == 'jasmine_favicon':
            return cherrypy.lib.static.serve_fileobj(
                pkg_resources.resource_stream(
                    'jasmine_core.images',
                    'jasmine_favicon.png'
                ),
                content_type='image/png'
            )
        mime_type, _ = mimetypes.guess_type(path)
        return cherrypy.lib.static.serve_fileobj(
            pkg_resources.resource_stream('jasmine_core', path),
            content_type=mime_type
        )
