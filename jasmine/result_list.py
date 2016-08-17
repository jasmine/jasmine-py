from jasmine.result import Result


class ResultList(list):

    def add_result(self, result):
        self.append(Result(**result))

    def passed(self):
        return self._filter_status('passed')

    def failed(self):
        return self._filter_status('failed')

    def pending(self):
        return self._filter_status('pending')

    def enabled(self):
        return [result for result in self if result.status != 'disabled']

    def _filter_status(self, status):
        return [result for result in self if result.status == status]

    def __add__(self, other):
        return ResultList(list.__add__(self, other))
