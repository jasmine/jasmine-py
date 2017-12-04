import pytest

import urllib

from jasmine.url_builder import JasmineUrlBuilder
from test.helpers.fake_config import FakeConfig


@pytest.fixture
def jasmine_config():
    return FakeConfig(
        src_dir='src',
        spec_dir='spec',
    )


def test_defaults(jasmine_config):
    url = JasmineUrlBuilder(jasmine_config=jasmine_config).build_url(port=80)

    assert url == 'http://localhost:80?random=false'


def test_stop_spec_on_expectation_failure(jasmine_config):
    jasmine_config._stop_spec_on_expectation_failure = True
    url = JasmineUrlBuilder(jasmine_config=jasmine_config).build_url(port=80)

    assert url == 'http://localhost:80?random=false&throwFailures=True'


def test_random(jasmine_config):
    jasmine_config._random = True
    true_url = JasmineUrlBuilder(jasmine_config=jasmine_config).build_url(port=80)
    assert true_url == 'http://localhost:80?random=true'

    jasmine_config._random = False
    false_url = JasmineUrlBuilder(jasmine_config=jasmine_config).build_url(port=80)
    assert false_url == 'http://localhost:80?random=false'


def test_seed(jasmine_config):
    url = JasmineUrlBuilder(jasmine_config=jasmine_config).build_url(port=80, seed=1234)

    assert url == 'http://localhost:80?random=false&seed=1234'


def test_multiple_query_parameters(jasmine_config):
    jasmine_config._random = True
    jasmine_config._stop_spec_on_expectation_failure = True

    url = JasmineUrlBuilder(jasmine_config=jasmine_config).build_url(port=80, seed=1234)

    uri_tuple = urllib.parse.urlparse(url)
    assert uri_tuple[0] == 'http'
    assert uri_tuple[1] == 'localhost:80'
    assert urllib.parse.parse_qs(uri_tuple[4]) == {"random": ['true'], "throwFailures": ['True'], "seed": ['1234']}

