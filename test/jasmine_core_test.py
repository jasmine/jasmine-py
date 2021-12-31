import os

import pytest
from jasmine_core import Core
import pkg_resources

notwin32 = pytest.mark.skipif("sys.platform == 'win32'")


@notwin32
def test_js_files():
    files = [
        'jasmine.js',
        'jasmine-html.js',
        'json2.js',
        'node_boot.js',
        'boot0.js',
        'boot1.js',
    ]

    assert Core.js_files() == files


def test_css_files():
    """ Should return a list of css files that are relative to Core.path() """
    assert ['jasmine.css'] == Core.css_files()


def test_favicon():
    assert os.path.isfile(pkg_resources.resource_filename('jasmine_core.images', 'jasmine_favicon.png'))
