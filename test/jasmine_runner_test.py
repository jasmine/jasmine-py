from jasmine_core import Core
import pytest

class DummyConfig(object):
    src_dir = "src"
    spec_dir = "specs"

    lists = {
        "src_files": ["/src/file1.js", "/src/file2.js"],
        "spec_files": ["/specs/file1_spec.js", "/specs/file2_spec.js"],
        "helpers": ['/specs/helpers/spec_helper.js'],
        "stylesheets": ['/src/css/user.css']
    }

    def __getattr__(self, name):
        def _missing():
            return self.lists.get(name, [])
        return _missing


@pytest.fixture
def config():
    return DummyConfig()


@pytest.fixture
def response(rf, config):
    from jasmine.views import JasmineRunner

    request = rf.get("")

    return JasmineRunner.as_view(template_name="runner.html", config=config)(request)


def test_js_files(config, response):
    core_js_files = ["core/{}".format(f) for f in Core.js_files()]
    boot_js_files = ["boot/{}".format(f) for f in Core.boot_files()]

    user_files = config.lists['src_files'] + config.lists['helpers'] + config.lists['spec_files']

    assert response.context_data['js_files'] == core_js_files + boot_js_files + [f[1:] for f in user_files]


def test_css_files(config, response):
    core_css_files = ["core/{}".format(css) for css in Core.css_files()]
    user_css_files = config.lists['stylesheets']

    assert response.context_data['css_files'] == core_css_files + [f[1:] for f in user_css_files]