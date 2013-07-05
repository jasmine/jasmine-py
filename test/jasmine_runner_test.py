from jasmine_core import Core
import pytest
from mock import Mock


@pytest.fixture
def config():
    from jasmine import Config

    mock_config = Mock(spec=Config, autospec=True)

    mock_config.lists = {
        "src_files": ["file1.js", "file2.js"],
        "spec_files": ["file1_spec.js", "file2_spec.js"],
        "helpers": ['helpers/spec1_helpers/spec_helper.js'],
        "stylesheets": ['css/user.css']
    }

    mock_config.src_files.return_value = ["src/file1.js", "src/file2.js"]
    mock_config.spec_files.return_value = ["specs/file1_spec.js", "specs/file2_spec.js"]
    mock_config.helpers.return_value = ["specs/helpers/spec_helper.js"]
    mock_config.stylesheets.return_value = ["src/css/user.css"]
    mock_config.src_dir.return_value = "src"
    mock_config.spec_dir.return_value = "specs"
    mock_config.script_urls.return_value = ["__jasmine__/jasmine.js",
                                            "__jasmine__/jasmine-html.js",
                                            "__jasmine__/json2.js",
                                            "__boot__/boot.js",
                                            "__src__/file1.js",
                                            "__src__/file2.js",
                                            "__spec__/file1_spec.js",
                                            "__spec__/file2_spec.js",
                                            "__spec__/helpers/spec1_helpers/spec_helper.js",
                                            ]
    mock_config.stylesheet_urls.return_value = ["__jasmine__/jasmine.css",
                                                "__src__/css/user.css",
                                                ]
    return mock_config


@pytest.fixture
def response(rf, config):
    from jasmine.views import JasmineRunner

    request = rf.get("")

    return JasmineRunner.as_view(template_name="runner.html", config=config)(request)


def test_js_files(config, response):
    core_js_files = ["__jasmine__/{0}".format(f) for f in Core.js_files()]
    boot_js_files = ["__boot__/{0}".format(f) for f in Core.boot_files()]

    user_files = ["__src__/{0}".format(f) for f in config.lists['src_files']] +\
                 ["__spec__/{0}".format(f) for f in config.lists['spec_files']] +\
                 ["__spec__/{0}".format(f) for f in config.lists['helpers']]

    assert response.context_data['js_files'] == core_js_files + boot_js_files + user_files


def test_css_files(config, response):
    core_css_files = ["__jasmine__/{0}".format(css) for css in Core.css_files()]
    user_css_files = ["__src__/{0}".format(f) for f in config.lists['stylesheets']]

    assert response.context_data['css_files'] == core_css_files + user_css_files


def test_reload_on_each_request(config, response):
    config.reload.assert_called_once_with()