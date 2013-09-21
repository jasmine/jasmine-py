import datetime
import time
import sys
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from mock import MagicMock, Mock
import pytest

from jasmine.ci import CIRunner, TestServerThread

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


def test_possible_ports():
    ports = TestServerThread().possible_ports("localhost:80,8000-8002")
    assert ports == [80, 8000, 8001, 8002]

@pytest.fixture
def sysexit(monkeypatch):
    mock_exit = MagicMock()
    monkeypatch.setattr(sys, 'exit', mock_exit)
    return mock_exit

@pytest.fixture
def test_server(monkeypatch):
    import jasmine.ci
    server = MagicMock()
    server.port = 80
    monkeypatch.setattr(jasmine.ci, 'TestServerThread', server)
    return server

@pytest.fixture
def firefox_driver(monkeypatch):
    import selenium.webdriver.firefox.webdriver
    driver = MagicMock()
    driver_class = lambda: driver
    monkeypatch.setattr(selenium.webdriver.firefox.webdriver, 'WebDriver', driver_class)
    return driver

@pytest.fixture
def suites():
    return [
        {
            "id": 0,
            "name": "datepicker",
            "type": "suite",
            "children": [
                {
                    "id": 0,
                    "name": "calls the datepicker constructor",
                    "type": "spec",
                    "children": []
                },
                {
                    "id": 1,
                    "name": "icon triggers the datepicker",
                    "type": "spec",
                    "children": []
                }
            ]
        }
    ]


@pytest.fixture
def results():
    return {
        "0": {
            "messages": [
                {
                    "type": "expect",
                    "matcherName": "toHaveBeenCalledWith",
                    "passed_": False,
                    "expected": {
                        "format": "yyy-mm-dd"
                    },
                    "message": "Expected spy datepicker to have been called with [ { format : 'yyy-mm-dd' } ] but actual calls were [ { format : 'yyyy-mm-dd' } ]",
                    "stack": "Totally the one you want",
                    "trace": {
                        "stack": "Stack would be here"
                    }
                }
            ],
            "result": "failed"
        },
        "1": {
            "messages": [
                {
                    "type": "expect",
                    "matcherName": "toHaveBeenCalled",
                    "passed_": True,
                    "message": "Passed.",
                    "trace": ""
                }
            ],
            "result": "passed"
        }
    }


def test_process_results__status(suites, results):
    processed = CIRunner()._process_results(suites, results)

    # Python is going to reverse the order of the above OrderedDict
    assert processed[0]['status'] == "failed"
    assert processed[1]['status'] == "passed"


def test_process_results__stack(suites, results):
    processed = CIRunner()._process_results(suites, results)

    assert processed[0]['status'] == 'failed'
    assert processed[1]['status'] == 'passed'

    assert processed[0]['failedExpectations'][0]['stack'] == "Totally the one you want"
    assert 'failedExpectations' not in processed[1]


def test_process_results__fullName(suites, results):
    processed = CIRunner()._process_results(suites, results)

    assert processed[0]['fullName'] == "datepicker calls the datepicker constructor"
    assert processed[1]['fullName'] == "datepicker icon triggers the datepicker"

def test_run_exits_with_zero_on_success(suites, results, capsys, sysexit, firefox_driver, test_server):
    results['0'] = results['1']
    del results['1']
    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.results()' in js:
            return results
        if 'jsApiReporter.suites()' in js:
            return suites
        return None

    def get_log(type):
        return [dict(timestamp=0, level='INFO', message='hello')]

    firefox_driver.execute_script = execute_script
    firefox_driver.get_log = get_log

    CIRunner().run()
    stdout, _stderr = capsys.readouterr()

    assert not sysexit.called
    stdout, _stderr = capsys.readouterr()

    dt = datetime.datetime.fromtimestamp(0)
    assert '[{0} - INFO] hello\n'.format(dt) not in stdout

def test_run_exits_with_nonzero_on_failure(suites, results, capsys, sysexit, firefox_driver, test_server):
    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.results()' in js:
            return results
        if 'jsApiReporter.suites()' in js:
            return suites
        return None

    timestamp = time.time() * 1000
    def get_log(type):
        assert type == 'browser'
        return [
            dict(timestamp=timestamp, level='INFO', message='hello'),
            dict(timestamp=timestamp + 1, level='WARNING', message='world'),
        ]

    firefox_driver.execute_script = execute_script
    firefox_driver.get_log = get_log

    CIRunner().run()

    sysexit.assert_called_with(1)
    stdout, _stderr = capsys.readouterr()

    dt = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    assert '[{0} - INFO] hello\n'.format(dt) in stdout

    dt = datetime.datetime.fromtimestamp((timestamp + 1) / 1000.0)
    assert '[{0} - WARNING] world\n'.format(dt) in stdout
