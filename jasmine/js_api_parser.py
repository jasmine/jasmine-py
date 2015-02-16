from collections import namedtuple

from jasmine.result_list import ResultList


RESULT_FIELDS = [
    'status',
    'fullName',
    'failedExpectations',
    'id',
    'description',
    'pendingReason'
]


class Parser(object):
    def parse(self, items):
        return ResultList([
            Result(**item)
            for item in self._filter_fields(items)
        ])

    def _filter_fields(self, raw_items):
        filtered_items = []
        for item in raw_items:
            filtered_items.append(dict((
                (k, v)
                for k, v in item.items()
                if k in RESULT_FIELDS
            )))
        return filtered_items


class Result(namedtuple('Result', RESULT_FIELDS)):
    def __new__(cls, status=None, fullName=None, failedExpectations={},
                id=None, description=None, pendingReason=None):
        # Constructor arguments correspond to RESULT_FIELDS
        return super(Result, cls).__new__(cls, status, fullName,
                                          failedExpectations, id,
                                          description, pendingReason)
