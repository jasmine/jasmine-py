from jasmine.result_list import ResultList


class Parser(object):
    RESULT_FIELDS = {
        'status': 'status',
        'fullName': 'full_name',
        'failedExpectations': 'failed_expectations',
        'deprecationWarnings': 'deprecation_warnings',
        'id': 'runnable_id',
        'description': 'description',
        'pendingReason': 'pending_reason'
    }

    def parse(self, items):
        result_list = ResultList()
        for item in self._filter_fields(items):
            result_list.add_result(item)
        return result_list

    def _filter_fields(self, raw_items):
        filtered_items = []
        for item in raw_items:
            filtered_items.append(dict((
                (self._to_snake_case(k), v)
                for k, v in item.items()
                if k in self.RESULT_FIELDS.keys()
            )))
        return filtered_items

    def _to_snake_case(self, key):
        return self.RESULT_FIELDS[key]
