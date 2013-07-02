import mockfs
import pytest
import os
import glob

from jasmine import Config


@pytest.fixture
def fs():
    mfs = mockfs.replace_builtins()

    os.path.lexists = mfs.exists
    glob.iglob = mfs.glob

    mfs.add_entries({
        "jasmine.yml": """
            src_files:
              - src/**/*.js
              - src/player.js
              - vendor/test.js
              - vendor/**/*.{js,coffee}
            """,
        "/helpers/spec_helper.js": '',
        "/lib/jams/jam_spec.js": '',
        "/src/player.js": '',
        "/src/mixer/mixer.js": '',
        "/src/tuner/fm/fm_tuner.js": '',
        "/spec/javascripts/player_spec.js": '',
        "/spec/javascripts/mixer/mixer_spec.js": '',
        "/spec/javascripts/tuner/fm/fm_tuner_spec.js": '',
        "/spec/javascripts/tuner/am/AMSpec.js": '',
        "/vendor/test.js": '',
        "/vendor/pants.coffee": '',
    })

    return mfs


@pytest.mark.usefixtures("fs")
def test_src_files():
    config = Config("jasmine.yml")

    assert config.src_files() == [
        '/src/player.js',
        '/src/mixer/mixer.js',
        '/src/tuner/fm/fm_tuner.js',
        '/vendor/test.js',
        '/vendor/pants.coffee'
    ]


@pytest.mark.usefixtures("fs")
def test_stylesheets_default():
    config = Config("jasmine.yml")

    assert config.stylesheets() == []


@pytest.mark.usefixtures("fs")
def test_helpers_default():
    config = Config("jasmine.yml")

    assert config.helpers() == ['/helpers/spec_helper.js']


@pytest.mark.usefixtures("fs")
def test_spec_files_default():
    config = Config("jasmine.yml")

    assert config.spec_files() == [
        '/spec/javascripts/player_spec.js',
        '/spec/javascripts/mixer/mixer_spec.js',
        '/spec/javascripts/tuner/am/AMSpec.js',
        '/spec/javascripts/tuner/fm/fm_tuner_spec.js',
    ]


def test_src_dir_spec_dir(fs):
    fs.add_entries({
        "jasmine.yml": """
            src_files:
              - "**/*.js"
              - player.js
              - vendor/test.js
              - vendor/**/*.{js,coffee}
            src_dir: src

            spec_dir: specs
            """,
        "/src/player.js": '',
        "/src/mixer/mixer.js": '',
        "/src/tuner/fm/fm_tuner.js": '',
        "/specs/player_spec.js": '',
        "/specs/mixer/mixer_spec.js": '',
        "/specs/tuner/fm/fm_tuner_spec.js": '',
        "/specs/tuner/am/AMSpec.js": '',
        "/vendor/test.js": '',
        "/vendor/pants.coffee": '',
        "/vendor/pantsSpec.js": '',
        "/helpers/spec_helper.js": ''
    })

    config = Config('jasmine.yml')

    assert config.src_files() == [
        '/src/player.js',
        '/src/mixer/mixer.js',
        '/src/tuner/fm/fm_tuner.js'
    ]

    assert config.spec_files() == [
        '/specs/player_spec.js',
        '/specs/mixer/mixer_spec.js',
        '/specs/tuner/am/AMSpec.js',
        '/specs/tuner/fm/fm_tuner_spec.js',
    ]