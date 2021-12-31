import os

from yaml import load, Loader
from jasmine_core import Core

from jasmine.utils import iglob


class Config(object):
    def __init__(self, yaml_file, project_path=None):
        self.yaml_file = yaml_file
        self.project_path = project_path or os.getcwd()
        self._load()

    def script_urls(self):
        core_js_files = Core.js_files()
        if 'node_boot.js' in core_js_files:
            core_js_files.remove('node_boot.js')
        return [
                   "/__jasmine__/{0}".format(core_js) for core_js in core_js_files
               ] + [
                   self._prefix_src_underscored(src_file) for src_file in self.src_files()
               ] + [
                   "/__spec__/{0}".format(helper) for helper in self.helpers()
               ] + [
                   "/__spec__/{0}".format(spec_file) for spec_file in self.spec_files()
               ]

    def stylesheet_urls(self):
        return [
                   "/__jasmine__/{0}".format(core_css) for core_css in Core.css_files()
               ] + [
                   "/__src__/{0}".format(css_file) for css_file in self.stylesheets()
               ]

    def reload(self):
        self._load()

    def src_files(self):
        return self._glob_filelist('src_files', self.src_dir())

    def stylesheets(self):
        return self._glob_filelist('stylesheets', self.src_dir())

    def helpers(self):
        default_helpers = os.path.join(self.project_path, self.spec_dir(),
                                       'helpers/**/*.js')

        return self._glob_filelist('helpers', self.spec_dir(),
                                   default=[default_helpers])

    def spec_files(self):
        default_spec = os.path.join(self.project_path, self.spec_dir(),
                                    "**/*[sS]pec.js")

        return self._glob_filelist('spec_files', self.spec_dir(),
                                   default=[default_spec])

    def src_dir(self):
        return self._yaml.get("src_dir") or self.project_path

    def spec_dir(self):
        return self._yaml.get("spec_dir") or 'spec/javascripts'

    def stop_spec_on_expectation_failure(self):
        return self._yaml.get("stop_spec_on_expectation_failure") is True

    def stop_on_spec_failure(self):
        return self._yaml.get("stop_on_spec_failure") is True

    def random(self):
        return self._yaml.get("random", True) is not False

    def _prefix_src_underscored(self, path):
        return (
            path if path.startswith('http') else "/__src__/{0}".format(path)
        )

    def _uniq(self, items, idfun=None):
        # order preserving

        if idfun is None:
            def idfun(x):
                return x
        seen = {}
        result = []
        for item in items:
            marker = idfun(item)
            # in old Python versions:
            # if seen.has_key(marker)
            # but in new ones:
            if marker in seen:
                continue

            seen[marker] = 1
            result.append(item)
        return result

    def _glob_filelist(self, filelist, relative_to, default=None):
        default = default or []
        paths = self._yaml.get(filelist) or default

        paths = [self._make_absolute(path, relative_to) for path in paths]
        paths = [self._expland_globs(path) for path in paths]
        paths = sum(paths, [])
        relpaths = [self._make_relative(path, relative_to) for path in paths]

        # fix py26 relpath from root bug http://bugs.python.org/issue5117
        return [
            relpath[3:] if relpath.startswith("../") else relpath
            for relpath in relpaths
        ]

    def _make_absolute(self, path, relative_to):
        return (
            path if path.startswith('http')
            else os.path.abspath(
                os.path.join(self.project_path, relative_to, path)
            )
        )

    def _expland_globs(self, path):
        return (
            [path] if path.startswith('http')
            else self._glob_paths([path])
        )

    def _make_relative(self, path, relative_to):
        return (
            path if path.startswith('http')
            else os.path.relpath(path, relative_to)
        )

    def _glob_paths(self, paths):
        files = []

        for src_glob in paths:
            files.extend([os.path.abspath(x) for x in iglob(src_glob)])

        return list(self._uniq(files))

    def _extract_urls(self, filelist):
        local_files = [x for x in filelist if 'http' not in x]
        urls = [x for x in filelist if 'http' in x]

        return local_files, urls

    def _load(self):
        with open(self.yaml_file, 'rU') as f:
            self._yaml = load(f, Loader=Loader) or {}
