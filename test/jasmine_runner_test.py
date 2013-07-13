import pytest
from mock import Mock


@pytest.fixture
def config():
    from jasmine.config import Config

    mock_config = Mock(spec=Config, autospec=True)
    mock_config.script_urls.return_value = ["__jasmine__/jasmine.js", "__boot__/boot.js"]
    mock_config.stylesheet_urls.return_value = ["__jasmine__/jasmine.css", "__src__/css/user.css"]

    return mock_config


@pytest.fixture
def response(rf, config):
    from jasmine.django.views import JasmineRunner

    request = rf.get("")

    return JasmineRunner.as_view(template_name="runner.html", config=config)(request)


def test_js_files(config, response):
    assert response.context_data['js_files'] == config.script_urls()
    assert response.context_data['css_files'] == config.stylesheet_urls()


def test_reload_on_each_request(config, response):
    config.reload.assert_called_once_with()