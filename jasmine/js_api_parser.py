from jasmine.result import Result
from jasmine.result_list import ResultList


class Parser(object):
    RESULT_FIELDS = [
        'status',
        'fullName',
        'failedExpectations',
        'id',
        'description',
        'pendingReason'
    ]

    def parse(self, items):
        result_list = ResultList()
        for item in self._filter_fields(items):
            result_list.add_result(item)
        return result_list

    def _filter_fields(self, raw_items):
        filtered_items = []
        for item in raw_items:
            filtered_items.append(dict((
                (k, v)
                for k, v in item.items()
                if k in self.RESULT_FIELDS
            )))
        return filtered_items


