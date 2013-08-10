from mockfs import replace_builtins, restore_builtins
import pkg_resources
import pytest
from jasmine.config import Config

import jasmine.standalone

@pytest.fixture
def app():
    try:
        reload(jasmine.standalone)
    except NameError:
        import imp
        imp.reload(jasmine.standalone)

    from jasmine.standalone import app
    app.testing = True
    return app


@pytest.fixture
def template():
    return pkg_resources.resource_string('jasmine.django.templates', 'runner.html')


@pytest.fixture
def mockfs(request):
    mfs = replace_builtins()
    mfs.add_entries({
        "/spec/javascripts/support/jasmine.yml": """
        src_dir: src
        spec_dir: spec
        """
    })
    request.addfinalizer(lambda: restore_builtins())
    return mfs


def test__favicon(mockfs, monkeypatch, app):
    monkeypatch.setattr(pkg_resources, 'resource_stream', lambda package, filename: [])

    with app.test_client() as client:
        rv = client.get("/jasmine_favicon.png")

        assert rv.status_code == 200


def test__before_first_request(mockfs, monkeypatch, app):
    monkeypatch.setattr(pkg_resources, 'resource_stream', lambda package, filename: [])

    assert not hasattr(app, 'jasmine_config')

    with app.test_client() as client:
        rv = client.get("/jasmine_favicon.png")
        assert rv.status_code == 200

    assert app.jasmine_config is not None


def test__serve(mockfs, monkeypatch, app):
    mockfs.add_entries({
        "/src/main.css": "CSS",
        "/src/main.js": "JS",
        "/src/main.png": "PNG"
    })

    with app.test_client() as client:
        rv = client.get("/__src__/main.css")

        assert rv.status_code == 200
        assert rv.headers['Content-Type'] == 'text/css; charset=utf-8'

        rv = client.get("/__src__/main.js")

        assert rv.status_code == 200
        assert rv.headers['Content-Type'] == 'application/javascript'

        rv = client.get("/__src__/main.png")

        assert rv.status_code == 200
        assert rv.headers['Content-Type'] == 'application/octet-stream'


def test__run(template, mockfs, monkeypatch, app):
    monkeypatch.setattr(pkg_resources, 'resource_listdir', lambda package, dir: ['jasmine.js', 'boot.js'])
    monkeypatch.setattr(pkg_resources, 'resource_string', lambda package, filename: str(template))

    monkeypatch.setattr(Config, 'src_files', lambda self: ['main.js', 'main_spec.js'])
    monkeypatch.setattr(Config, 'stylesheets', lambda self: ['main.css'])

    with app.test_client() as client:
        rv = client.get("/")

        assert rv.status_code == 200

        html = rv.get_data(as_text=True)

        assert """<script src="__jasmine__/jasmine.js" type="text/javascript"></script>""" in html
        assert """<script src="__jasmine__/boot.js" type="text/javascript"></script>""" in html
        assert """<script src="__src__/main.js" type="text/javascript"></script>""" in html
        assert """<script src="__src__/main_spec.js" type="text/javascript"></script>""" in html
        assert """<link rel="stylesheet" href="__src__/main.css" type="text/css" media="screen"/>""" in html