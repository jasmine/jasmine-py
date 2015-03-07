class Result():
    def __init__(
            self,
            status=None,
            full_name=None,
            failed_expectations=None,
            runnable_id=None,
            description=None,
            pending_reason=None
    ):
        if failed_expectations is None:
            failed_expectations = {}

        self._status = status
        self._full_name = full_name
        self._failed_expectations = failed_expectations
        self._runnable_id = runnable_id
        self._description = description
        self._pending_reason = pending_reason

    @property
    def status(self):
        return self._status

    @property
    def full_name(self):
        return self._full_name

    @property
    def failed_expectations(self):
        return self._failed_expectations

    @property
    def runnable_id(self):
        return self._runnable_id

    @property
    def description(self):
        return self._description

    @property
    def pending_reason(self):
        return self._pending_reason
