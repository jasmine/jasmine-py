from mockfs import replace_builtins, restore_builtins
import pkg_resources
import pytest

from jasmine.standalone import JasmineApp
from test.helpers.fake_config import FakeConfig


@pytest.fixture
def jasmine_config():
    script_urls = ['__src__/main.js', '__spec__/main_spec.js']
    stylesheet_urls = ['__src__/main.css']

    return FakeConfig(
        src_dir='src',
        spec_dir='spec',
        script_urls=script_urls,
        stylesheet_urls=stylesheet_urls
    )

@pytest.fixture
def app(jasmine_config):
    jasmine_app = JasmineApp(jasmine_config=jasmine_config)

    jasmine_app.app.testing = True
    return jasmine_app.app


@pytest.fixture
def template():
    return pkg_resources.resource_string('jasmine.django.templates', 'runner.html')


@pytest.fixture
def mockfs(request):
    mfs = replace_builtins()
    request.addfinalizer(lambda: restore_builtins())
    return mfs


@pytest.mark.usefixtures('mockfs')
def test__favicon(monkeypatch, app):
    monkeypatch.setattr(pkg_resources, 'resource_stream', lambda package, filename: [])

    with app.test_client() as client:
        response = client.get("/jasmine_favicon.png")

        assert response.status_code == 200


def test__serve(mockfs, app):
    mockfs.add_entries({
        "/src/main.css": "CSS",
        "/src/main.js": "JS",
        "/src/main.png": "PNG"
    })

    with app.test_client() as client:
        response = client.get("/__src__/main.css")

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/css; charset=utf-8'

        response = client.get("/__src__/main.js")

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/javascript'

        response = client.get("/__src__/main.png")

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'image/png'


def test__serve_jasmine_files(mockfs, app, monkeypatch):
    monkeypatch.setattr(
        pkg_resources,
        'resource_string',
        lambda package, filename: "file content"
    )

    with app.test_client() as client:
        response = client.get("/__jasmine__/jasmine-source.js")

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/javascript'
        assert response.data.decode('ascii') == 'file content'

def test__run(template, mockfs, monkeypatch, app, jasmine_config):
    monkeypatch.setattr(
        pkg_resources,
        'resource_listdir',
        lambda package, dir: [
            'jasmine.js',
            'boot.js',
            'node_boot.js'
        ]
    )
    monkeypatch.setattr(
        pkg_resources,
        'resource_string',
        lambda package, filename: template
    )

    with app.test_client() as client:
        response = client.get("/")

        assert jasmine_config.reload_call_count == 1
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        assert """<script src="__src__/main.js" type="text/javascript"></script>""" in html
        assert """<script src="__spec__/main_spec.js" type="text/javascript"></script>""" in html
        assert """<link rel="stylesheet" href="__src__/main.css" type="text/css" media="screen"/>""" in html
