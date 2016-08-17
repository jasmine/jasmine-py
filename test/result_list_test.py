from mock import Mock
import pytest

from jasmine.result_list import ResultList


@pytest.fixture
def result_list():
    return ResultList([
        Mock(status='passed', id='pass'),
        Mock(status='failed', id='fail'),
        Mock(status='pending', id='pend'),
        Mock(status='disabled', id='disable'),
    ])


def test_result_list_passed(result_list):
    passed = result_list.passed()
    assert len(passed) == 1
    assert passed[0].id == 'pass'


def test_result_list_failed(result_list):
    failed = result_list.failed()
    assert len(failed) == 1
    assert failed[0].id == 'fail'


def test_result_list_pending(result_list):
    pending = result_list.pending()
    assert len(pending) == 1
    assert pending[0].id == 'pend'


def test_result_list_enabled(result_list):
    enabled = result_list.enabled()
    assert len(enabled) == 3
    assert enabled[0].id == 'pass'
    assert enabled[1].id == 'fail'
    assert enabled[2].id == 'pend'


def test_result_list_concatination(result_list):
    concatinated = result_list + result_list
    assert len(concatinated.passed()) == 2
