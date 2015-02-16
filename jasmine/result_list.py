try:
    from future_builtins import filter
except ImportError:
    pass


class ResultList(list):
    def passed(self):
        return self._filter_status('passed')

    def failed(self):
        return self._filter_status('failed')

    def pending(self):
        return self._filter_status('pending')

    def _filter_status(self, status):
        return filter(lambda x: x.status == status, self)

