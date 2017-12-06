import os
import sys
import tempfile

from mock import Mock, MagicMock
import pytest
from yaml import load
from contextlib import contextmanager

import builtins
from jasmine.entry_points import (
    continuous_integration,
    query,
    standalone,
    mkdir_p,
    install
)
from jasmine.ci import CIRunner
import jasmine.standalone


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


class FakeApp(object):
    def __init__(self, jasmine_config=None):
        FakeApp.app = self
        self.run = MagicMock(name='run')

    def run(self, host=None, port=None, blocking=False):
        pass


def write_config(path="spec/javascripts/support/jasmine.yml"):
    mkdir_p(os.path.dirname(path))
    with open(path, "w") as f:
        f.write("""
            src_dir: src
            spec_dir: spec
            """)


@pytest.fixture
def mock_CI_run(request):
    CIRunner.run = MagicMock(name='run')


def test_ci_config_check(monkeypatch, mock_CI_run):
    with in_temp_dir():
        monkeypatch.setattr(sys, 'argv', ['test.py'])

        continuous_integration()
        assert not CIRunner.run.called


def test_continuous_integration__set_browser(monkeypatch, mock_CI_run):
    with in_temp_dir():
        write_config()
        monkeypatch.setattr(sys, 'argv', ["test.py", "--browser", "firefox"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        continuous_integration()

        CIRunner.run.assert_called_once_with(browser='firefox', show_logs=False, seed=None, app=FakeApp.app)


def test_continuous_integration__browser_default(monkeypatch, mock_CI_run):
    with in_temp_dir():
        write_config()
        monkeypatch.setattr(sys, 'argv', ["test.py"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        continuous_integration()

        CIRunner.run.assert_called_once_with(browser=None, show_logs=False, seed=None, app=FakeApp.app)


def test_continuous_integration__show_logs(monkeypatch, mock_CI_run):
    with in_temp_dir():
        write_config()
        monkeypatch.setattr(sys, 'argv', ["test.py", "--logs"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        continuous_integration()

        CIRunner.run.assert_called_once_with(show_logs=True, browser=None, seed=None, app=FakeApp.app)


def test_continuous_integration__set_seed(monkeypatch, mock_CI_run):
    with in_temp_dir():
        write_config()
        monkeypatch.setattr(sys, 'argv', ["test.py", "--seed", "1234"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        continuous_integration()

        CIRunner.run.assert_called_once_with(seed="1234", show_logs=False, browser=None, app=FakeApp.app)

def test_continuous_integration__custom_config__from_argv(monkeypatch):
    with in_temp_dir():
        write_config("custom/path/to/jasmine.yml")
        monkeypatch.setattr(sys, 'argv', ["test.py", "-c", "custom/path/to/jasmine.yml"])
        fake_standalone = Mock()
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', fake_standalone)

        continuous_integration()

        fake_standalone.assert_called_once()
        standalone_construction_kwargs = fake_standalone.call_args[1]
        called_with_config = standalone_construction_kwargs['jasmine_config'].yaml_file
        assert called_with_config.endswith("custom/path/to/jasmine.yml")


def test_standalone__set_host(monkeypatch):
    with in_temp_dir():
        write_config()
        monkeypatch.setattr(sys, 'argv', ["test.py", "-o", "127.0.0.2"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        standalone()

        FakeApp.app.run.assert_called_once_with(host="127.0.0.2", port=8888, blocking=True)


def test_standalone__set_port(monkeypatch):
    with in_temp_dir():
        write_config()
        monkeypatch.setattr(sys, 'argv', ["test.py", "-p", "1337"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        standalone()

        FakeApp.app.run.assert_called_once_with(host="127.0.0.1", port=1337, blocking=True)


def test_standalone__port_default(monkeypatch):
    with in_temp_dir():
        write_config()
        monkeypatch.setattr(sys, 'argv', ["test.py"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        standalone()

        FakeApp.app.run.assert_called_once_with(host="127.0.0.1", port=8888, blocking=True)


def test_standalone__port_invalid(monkeypatch):
    with in_temp_dir():
        write_config()
        FakeApp.app = None
        monkeypatch.setattr(sys, 'argv', ["test.py", "-p", "pants"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        with pytest.raises(SystemExit):
            standalone()

        assert "invalid int value: 'pants'"
        assert FakeApp.app == None

def test_standalone__missing_config(monkeypatch):
    with in_temp_dir():
        FakeApp.app = None
        monkeypatch.setattr(sys, 'argv', ["test.py"])
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', FakeApp)

        standalone()

        assert FakeApp.app == None

def test_standalone__custom_config__from_argv(monkeypatch):
    with in_temp_dir():
        write_config("custom/path/to/jasmine.yml")
        monkeypatch.setattr(sys, 'argv', ["test.py", "-c", "custom/path/to/jasmine.yml"])
        fake_standalone = Mock()
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', fake_standalone)

        standalone()

        fake_standalone.assert_called_once()
        standalone_construction_kwargs = fake_standalone.call_args[1]
        called_with_config = standalone_construction_kwargs['jasmine_config'].yaml_file
        assert called_with_config.endswith("custom/path/to/jasmine.yml")

def test_standalone__custom_config__when_environment_variable_set(monkeypatch):
    with in_temp_dir():
        write_config("custom/path/to/jasmine.yml")
        monkeypatch.setattr(sys, 'argv', ["test.py"])
        env_vars = {'JASMINE_CONFIG_PATH': "custom/path/to/jasmine.yml"}
        monkeypatch.setattr(os, 'environ', env_vars)
        fake_standalone = Mock()
        monkeypatch.setattr(jasmine.entry_points, 'JasmineApp', fake_standalone)

        standalone()

        fake_standalone.assert_called_once()
        standalone_construction_kwargs = fake_standalone.call_args[1]
        called_with_config = standalone_construction_kwargs['jasmine_config'].yaml_file
        assert called_with_config.endswith("custom/path/to/jasmine.yml")


def test__query__yes(capsys, monkeypatch):
    input_string(monkeypatch, "Y")

    choice = query("Would you like to play a game?")

    out, err = capsys.readouterr()

    assert out == "Would you like to play a game? [Y/n] "
    assert True == choice


def test__query__no(capsys, monkeypatch):
    input_string(monkeypatch, "N")

    choice = query("Would you like to hear some cat facts?")

    out, err = capsys.readouterr()

    assert out == "Would you like to hear some cat facts? [Y/n] "
    assert False == choice


def test__query__default(capsys, monkeypatch):
    input_string(monkeypatch, "")

    choice = query("Would you like to blindly accept my defaults?")

    out, err = capsys.readouterr()

    assert out == "Would you like to blindly accept my defaults? [Y/n] "
    assert True == choice


def test__mkdir_p():
    with in_temp_dir():
        mkdir_p("pants/a/b/c")
    
        assert os.path.isdir("pants")
        assert os.path.isdir("pants/a")
        assert os.path.isdir("pants/a/b")
        assert os.path.isdir("pants/a/b/c")


def input_string(monkeypatch, string=""):
    try:
        monkeypatch.setattr(builtins, 'raw_input', lambda: string)
    except AttributeError:
        monkeypatch.setattr(builtins, 'input', lambda: string)


def test_install__yes(monkeypatch):
    # Should create spec/javascripts/support
    # Should create a spec/javascripts/support/jasmine.yml
    spec_dir = "spec/javascripts/support"
    yaml_file = os.path.join(spec_dir, "jasmine.yml")

    input_string(monkeypatch, "Y")

    install()

    assert os.path.isdir(spec_dir)
    assert os.path.isfile(yaml_file)

    yaml = load(open(yaml_file))

    assert yaml['spec_files'] == ["**/*[Ss]pec.js"]


def test_install__yes__existing_yaml(monkeypatch):
    with in_temp_dir():
        mkdir_p("spec/javascripts/support")
        with open("spec/javascripts/support/jasmine.yml", "w") as f:
            f.write("""
                spec_files:
                    - "**/pants.*"
                """)
        # Should NOT overwrite spec/javascripts/support/jasmine.yml
        spec_dir = "spec/javascripts/support"
        yaml_file = os.path.join(spec_dir, "jasmine.yml")
    
        input_string(monkeypatch, "Y")
    
        install()
    
        assert os.path.isdir(spec_dir)
        assert os.path.isfile(yaml_file)
    
        yaml = load(open(yaml_file))
    
        assert yaml['spec_files'] == ["**/pants.*"]


def test_install__no(monkeypatch):
    with in_temp_dir():
        # Should NOT create spec/javascripts/support
        # Should NOT create a spec/javascripts/support/jasmine.yml
        spec_dir = "spec/javascripts/support"
        yaml_file = os.path.join(spec_dir, "jasmine.yml")
    
        input_string(monkeypatch, "N")
    
        install()
    
        assert not os.path.isdir(spec_dir)
        assert not os.path.isfile(yaml_file)
