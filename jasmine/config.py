from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from .utils import iglob
import os


class Config(object):
    def __init__(self, yaml_file, project_path=os.getcwd()):
        self.yaml_file = yaml_file
        self.project_path = project_path
        self._load()

    def _uniq(self, items):
        return list(OrderedDict.fromkeys(items))

    def _glob_paths(self, paths):
        files = []

        for src_glob in paths:
            files.extend([os.path.abspath(x) for x in iglob(src_glob)])

        return self._uniq(files)

    def _load(self):
        with open(self.yaml_file, 'rU') as f:
            self.yaml = load(f, Loader=Loader) or {}

    def reload(self):
        self._load()

    def src_files(self):
        src_paths = self.yaml.get('src_files') or []
        src_paths = [os.path.join(self.src_dir(), src_path) for src_path in src_paths]

        return self._glob_paths(src_paths)

    def stylesheets(self):
        return self._glob_paths(self.yaml.get('stylesheets') or [])

    def helpers(self):
        helpers_paths = self.yaml.get('helpers') or ['helpers/**/*.js']
        helpers_paths = [os.path.join(self.spec_dir(), helpers_path) for helpers_path in helpers_paths]

        return self._glob_paths(helpers_paths)

    def spec_files(self):
        spec_paths = self.yaml.get('spec_files') or ["**/*[sS]pec.js"]
        spec_paths = [os.path.join(self.spec_dir(), spec_path) for spec_path in spec_paths]

        return self._glob_paths(spec_paths)

    def src_dir(self):
        return self.yaml.get("src_dir") or self.project_path

    def spec_dir(self):
        return self.yaml.get("spec_dir") or 'spec/javascripts'