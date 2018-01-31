import os
import tempfile
import pkg_resources
from contextlib import contextmanager

from jasmine.config import Config

default_jasmine_yml = """
    src_files:
      - src/player.js
      - src/**/*.js
      - http://cdn.jquery.com/jquery.js
      - vendor/test.js
      - vendor/**/*.{js,coffee}
    """

def create_files(jasmine_yml=default_jasmine_yml):
    files = {
        "jasmine.yml": jasmine_yml,
        "spec/javascripts/helpers/spec_helper.js": '',
        "lib/jams/jam_spec.js": '',
        "src/player.js": '',
        "src/mixer/mixer.js": '',
        "src/tuner/fm/fm_tuner.js": '',
        "spec/javascripts/player_spec.js": '',
        "spec/javascripts/mixer/mixer_spec.js": '',
        "spec/javascripts/tuner/fm/fm_tuner_spec.js": '',
        "spec/javascripts/tuner/am/AMSpec.js": '',
        "vendor/test.js": '',
        "vendor/pants.coffee": '',
        "vendor_spec/pantsSpec.js": '',
        "main.css": '',
    }
    for k in files:
        parent = os.path.dirname(k)
        if parent and not os.path.exists(parent):
            os.makedirs(parent)
        with open(k, 'w') as f:
            f.write(files[k])

@contextmanager
def pushd(dest):
    src = os.getcwd()
    os.chdir(dest)
    try:
        yield
    finally:
        os.chdir(src)

@contextmanager
def in_temp_dir():
    with tempfile.TemporaryDirectory() as root:
        with pushd(root):
            yield

def test_src_files():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        src_files = config.src_files()
    
        assert src_files[0] == "src/player.js"
        assert src_files.index("vendor/test.js") < src_files.index("vendor/pants.coffee")
    
        assert 'http://cdn.jquery.com/jquery.js' in src_files
        assert 'src/mixer/mixer.js' in src_files
        assert 'src/tuner/fm/fm_tuner.js' in src_files
        assert 'vendor/pants.coffee' in src_files


def test_stylesheets_default():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        assert config.stylesheets() == []


def test_helpers_default():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        assert config.helpers() == ['helpers/spec_helper.js']


def test_spec_files_default():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        # sort because all of the specified paths are globs, order does not matter
        assert sorted(config.spec_files()) == [
            'mixer/mixer_spec.js',
            'player_spec.js',
            'tuner/am/AMSpec.js',
            'tuner/fm/fm_tuner_spec.js',
        ]


def test_src_dir_spec_dir():
    with in_temp_dir():
        create_files("""
            src_dir: src
            spec_dir: spec
            src_files:
                - ./**/*.js
                - player.js
                - vendor/test.js
                - vendor/**/*.{js,coffee}
            """)
        config = Config("jasmine.yml")
        src_files = config.src_files()
    
        assert 'player.js' in src_files
        assert 'mixer/mixer.js' in src_files
        assert 'tuner/fm/fm_tuner.js' in src_files
    
        # noinspection PySetFunctionToLiteral
        assert set(config.spec_files()) == set([
            "javascripts/player_spec.js",
            "javascripts/mixer/mixer_spec.js",
            "javascripts/tuner/am/AMSpec.js",
            "javascripts/tuner/fm/fm_tuner_spec.js",
        ])


def test_script_urls(monkeypatch):
    monkeypatch.setattr(
        pkg_resources,
        'resource_listdir',
        lambda package, directory: [
            'json2.js',
            'jasmine.js',
            'boot.js',
            'node_boot.js',
            'jasmine-html.js',
            'jasmine.css'
        ]
    )

    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        script_urls = config.script_urls()

        assert script_urls[:5] == [
            "/__jasmine__/jasmine.js",
            "/__jasmine__/jasmine-html.js",
            "/__jasmine__/json2.js",
            "/__jasmine__/boot.js",
            "/__src__/src/player.js"
        ]
    
        assert 'http://cdn.jquery.com/jquery.js' in script_urls
        assert '/__src__/src/mixer/mixer.js' in script_urls
        assert '/__src__/src/tuner/fm/fm_tuner.js' in script_urls
        assert '/__src__/vendor/pants.coffee' in script_urls


def test_stylesheet_urls():
    with in_temp_dir():
        create_files("""
            stylesheets:
              - ./**/*.css
            """)
        with open("main.css", "r"):
            pass
        config = Config("jasmine.yml")

        stylesheet_urls = config.stylesheet_urls()
    
        assert stylesheet_urls == [
            "/__jasmine__/jasmine.css",
            "/__src__/main.css"
        ]

def test_stop_spec_on_expectation_failure_default():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        assert config.stop_spec_on_expectation_failure() is False


def test_stop_spec_on_expectation_failure_invalid():
    with in_temp_dir():
        create_files("""
                stop_spec_on_expectation_failure: pants
            """)
        config = Config("jasmine.yml")
        assert config.stop_spec_on_expectation_failure() is False


def test_stop_spec_on_expectation_failure_set():
    with in_temp_dir():
        create_files("""
                stop_spec_on_expectation_failure: true
            """)
        config = Config("jasmine.yml")
        assert config.stop_spec_on_expectation_failure() is True


def test_stop_on_spec_failure_default():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        assert config.stop_on_spec_failure() is False


def test_stop_on_spec_failure_invalid():
    with in_temp_dir():
        create_files("""
                stop_on_spec_failure: pants
            """)
        config = Config("jasmine.yml")
        assert config.stop_on_spec_failure() is False


def test_stop_on_spec_failure_set():
    with in_temp_dir():
        create_files("""
                stop_on_spec_failure: true
            """)
        config = Config("jasmine.yml")
        assert config.stop_on_spec_failure() is True

def test_random_default():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
    assert config.random() is True


def test_random_invalid():
    with in_temp_dir():
        create_files("""
            random: pants
            """)
        config = Config("jasmine.yml")
        assert config.random() is True


def test_random_set_false():
    with in_temp_dir():
        create_files("""
            random: false
            """)
        config = Config("jasmine.yml")
        assert config.random() is False

def test_reload():
    with in_temp_dir():
        create_files()
        config = Config("jasmine.yml")
        assert config.src_files() != ['pants.txt']

        with open("jasmine.yml", "w") as f:
            f.write("""
                src_files:
                  - pants.txt
                """)

        with open("pants.txt", "w"):
            pass

        config.reload()
        assert config.src_files() == ['pants.txt']
