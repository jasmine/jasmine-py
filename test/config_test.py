import os
import glob

import mockfs
import pytest


@pytest.fixture
def fs(request):
    mfs = mockfs.replace_builtins()

    os.path.lexists = mfs.exists
    glob.iglob = mfs.glob

    mfs.add_entries({
        "jasmine.yml": """
            src_files:
              - src/player.js
              - src/**/*.js
              - vendor/test.js
              - vendor/**/*.{js,coffee}
            """,
        "/spec/javascripts/helpers/spec_helper.js": '',
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
        "/vendor_spec/pantsSpec.js": '',
    })

    request.addfinalizer(lambda: mockfs.restore_builtins())

    return mfs


@pytest.fixture
def config(fs):
    from jasmine import Config

    return Config("jasmine.yml", project_path="/")


@pytest.mark.usefixtures("fs")
def test_src_files(config):
    assert config.src_files() == [
        'src/player.js',
        'src/mixer/mixer.js',
        'src/tuner/fm/fm_tuner.js',
        'vendor/test.js',
        'vendor/pants.coffee',
    ]


@pytest.mark.usefixtures("fs")
def test_stylesheets_default(config):
    assert config.stylesheets() == []


@pytest.mark.usefixtures("fs")
def test_helpers_default(config):
    assert config.helpers() == ['helpers/spec_helper.js']


@pytest.mark.usefixtures("fs")
def test_spec_files_default(config):
    assert config.spec_files() == [
        'player_spec.js',
        'mixer/mixer_spec.js',
        'tuner/am/AMSpec.js',
        'tuner/fm/fm_tuner_spec.js',
    ]


@pytest.mark.usefixtures("fs")
def test_src_dir_spec_dir(config):
    config.yaml['src_dir'] = 'src'
    config.yaml['spec_dir'] = 'spec'
    config.yaml['src_files'] = ['**/*.js', 'player.js', 'vendor/test.js', 'vendor/**/*.{js,coffee}']

    assert config.src_files() == [
        'player.js',
        'mixer/mixer.js',
        'tuner/fm/fm_tuner.js',
    ]

    assert config.spec_files() == [
        "javascripts/player_spec.js",
        "javascripts/mixer/mixer_spec.js",
        "javascripts/tuner/am/AMSpec.js",
        "javascripts/tuner/fm/fm_tuner_spec.js",
    ]


def test_reload(fs, config):
    fs.add_entries({
        "jasmine.yml": """
            src_files:
              - pants
            """
     })

    config.reload()

    assert config.yaml['src_files'] == ['pants']