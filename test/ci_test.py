import pytest
from jasmine.ci import CIRunner

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


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
    return OrderedDict({
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
    })


def test_process_results__status(suites, results):
    processed = CIRunner()._process_results(suites, results)

    # Python is going to reverse the order of the above OrderedDict
    assert processed[0]['status'] == "passed"
    assert processed[1]['status'] == "failed"


def test_process_results__stack(suites, results):
    processed = CIRunner()._process_results(suites, results)

    assert processed[0]['status'] == 'passed'
    assert processed[1]['status'] == 'failed'

    assert 'failedExpectations' not in processed[0]
    assert processed[1]['failedExpectations'][0]['stack'] == "Totally the one you want"


def test_process_results__fullName(suites, results):
    processed = CIRunner()._process_results(suites, results)

    assert processed[0]['fullName'] == "datepicker icon triggers the datepicker"
    assert processed[1]['fullName'] == "datepicker calls the datepicker constructor"
