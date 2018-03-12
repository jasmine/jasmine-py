import datetime

import pytest

from jasmine.console_formatter import ConsoleFormatter
from jasmine.js_api_parser import Parser
from jasmine.result_list import ResultList


@pytest.fixture
def results():
    parser = Parser()
    return parser.parse([
        {u'status': u'passed'},
        {u'status': u'failed'},
        {u'status': u'passed'},
        {u'status': u'pending', u'fullName': u'Context is this test is pending'},
        {u'status': u'disabled'},
    ])


@pytest.fixture
def passing_results():
    parser = Parser()
    return parser.parse([
        {u'status': u'passed'},
        {u'status': u'passed'},
        {u'status': u'pending', u'fullName': u'Context is this test is pending'},
    ])


@pytest.fixture
def browser_logs():
    return [
        {u'timestamp': 0, 'level': 'INFO', 'message': 'hi'},
        {u'timestamp': 1000, 'level': 'WARNING', 'message': 'lo'},
        {u'timestamp': 2000, 'level': 'INFO', 'message': 'bye'},
    ]


def _create_console_formatter(spec_results=None, suite_results=None, browser_logs=None, seed=None, colors=False):
    spec_results = spec_results or ResultList([])
    suite_results = suite_results or ResultList([])
    browser_logs = browser_logs or []

    return ConsoleFormatter(
        spec_results=spec_results,
        suite_results=suite_results,
        browser_logs=browser_logs,
        seed=seed,
        colors=colors,
    )


def test_format_progress(results):
    formatter = _create_console_formatter(spec_results=results, colors=False)

    assert formatter.format_progress() == ".X.*"


def test_format_summary(results):
    formatter = _create_console_formatter(spec_results=results, colors=False)

    assert formatter.format_summary() == "4 specs, 1 failed, 1 pending"


def test_format_summary_with_seed(results):
    formatter = _create_console_formatter(spec_results=results, seed=1234, colors=False)

    assert formatter.format_summary() == "4 specs, 1 failed, 1 pending\nRandomized with seed 1234 (jasmine-ci --seed 1234)"


def test_format_suite_errors_empty():
    formatter = _create_console_formatter(suite_results=ResultList([]))
    assert formatter.format_suite_failure() == ""


def test_format_suite_errors():
    parser = Parser()
    suite_results = parser.parse([
        {
            u'status': u'failed',
            u'failedExpectations': [
                {"message": "ahhh", "stack": "stack1"},
                {"message": "oh no!", "stack": "stack2"}
            ]
        },
        {
            u'status': u'failed',
            u'failedExpectations': [
                {"message": "boom", "stack": "stack3"},
            ]
        },
        {
            u'status': u'failed',
            u'failedExpectations': [
                {"message": "nope"},
            ]
        }
    ])

    formatter = _create_console_formatter(suite_results=suite_results)
    assert formatter.format_suite_failure() == \
           "Suite Failures:\n" \
           + "  ahhh\n" \
           + "  stack1\n" \
           + "  oh no!\n" \
           + "  stack2\n" \
           + "  boom\n" \
           + "  stack3\n" \
           + "  nope\n"


def test_format_browser_logs(results, browser_logs):
    formatter = _create_console_formatter(spec_results=results, colors=False, browser_logs=browser_logs)

    dt1, dt2, dt3 = map(datetime.datetime.fromtimestamp, range(3))
    assert formatter.format_browser_logs() == (
        "Browser Session Logs:\n" +
        "  [{0} - INFO] hi\n".format(dt1) +
        "  [{0} - WARNING] lo\n".format(dt2) +
        "  [{0} - INFO] bye\n".format(dt3) +
        "\n"
    )


def test_format_browser_logs_with_no_failures(passing_results, browser_logs):
    formatter = _create_console_formatter(spec_results=passing_results, colors=False, browser_logs=browser_logs)

    assert formatter.format_browser_logs() == ""


def test_format_failures():
    parser = Parser()

    stack1 = u"""Error: Expected 'Batman' to equal 'PANTS'.
        at stack (http://localhost:8888/__jasmine__/jasmine.js:1110)
        at http://localhost:8888/__spec__/global_spec.js:3"""

    stack2 = u"""Error: Expected 'Batman' to equal 'Superman'.
        at stack (http://localhost:8888/__jasmine__/jasmine.js:1110)
        at http://localhost:8888/__spec__/global_spec.js:6"""

    stack3 = u"""Error: Expected 'Justice' to equal 'Served'.
        at stack (http://localhost:8888/__jasmine__/jasmine.js:1110)
        at http://localhost:8888/__spec__/global_spec.js:9"""

    results = parser.parse([
        {u'status': u'passed', u'fullName': u'Context is this test passes'},
        {u'status': u'failed', u'fullName': u'Context is this test fails',
         u'failedExpectations': [{u'stack': stack1, u'message': 'Message1'}]},
        {u'status': u'failed', u'fullName': u'Context is this test also fails',
         u'failedExpectations': [{u'stack': stack2, u'message': 'Message2'},
                                 {u'stack': stack3, u'message': 'Message3'}]},
    ])

    formatter = _create_console_formatter(spec_results=results, colors=False)

    assert formatter.format_spec_failures() == \
           "Context is this test fails\n" + \
           "  Message1\n" + \
           "  Error: Expected 'Batman' to equal 'PANTS'.\n" + \
           "        at http://localhost:8888/__spec__/global_spec.js:3\n" + \
           "Context is this test also fails\n" + \
           "  Message2\n" + \
           "  Error: Expected 'Batman' to equal 'Superman'.\n" + \
           "        at http://localhost:8888/__spec__/global_spec.js:6\n" + \
           "  Message3\n" + \
           "  Error: Expected 'Justice' to equal 'Served'.\n" + \
           "        at http://localhost:8888/__spec__/global_spec.js:9\n"


def test_clean_stack(results):
    formatter = _create_console_formatter(spec_results=results, colors=False)

    dirty_stack = u"""Error: Expected 'Batman' to equal 'PANTS'.
        at stack (http://localhost:8888/__jasmine__/jasmine.js:1110)
        at http://localhost:8888/__spec__/global_spec.js:3"""

    assert formatter.clean_stack(dirty_stack) == """Error: Expected 'Batman' to equal 'PANTS'.
        at http://localhost:8888/__spec__/global_spec.js:3"""


def test_pending_stack(results):
    formatter = _create_console_formatter(spec_results=results, colors=False)

    assert formatter.format_pending() == "Context is this test is pending\n"


def test_pending_with_message():
    parser = Parser()

    results = parser.parse(
        [
            {
                u'status': u'pending',
                u'fullName': u'pending',
                u'pendingReason': 'the reason'
            }
        ]
    )

    formatter = _create_console_formatter(spec_results=results, colors=False)
    assert formatter.format_pending() == "pending\n  Reason: the reason\n"

def test_deprecation_warning():
    parser = Parser()

    specs = parser.parse(
        [
            {
                u'status': u'passed',
                u'fullName': u'Speccy',
                u'deprecationWarnings': [
                    {
                        u'message': u'spec deprecated',
                        u'stack': None
                    }
                ]
            }
        ]
    )

    suites = parser.parse(
        [
            {
                u'status': u'passed',
                u'fullName': u'Sweet',
                u'deprecationWarnings': [
                    {
                        u'message': u'suite deprecated',
                        u'stack': None
                    }
                ]
            }
        ]
    )

    formatter = _create_console_formatter(spec_results=specs, suite_results=suites, colors=False)
    assert formatter.format_deprecations() == \
            "Deprecations:\n" + \
            "Speccy\n" + \
            "  spec deprecated\n" + \
            "  \n" + \
            "Sweet\n" + \
            "  suite deprecated\n" +\
            "  \n"

