class Result():
    def __init__(
            self,
            status=None,
            fullName=None,
            failedExpectations=None,
            id=None,
            description=None,
            pendingReason=None
    ):
        if failedExpectations is None:
            failedExpectations = {}

        self._status = status
        self._full_name = fullName
        self._failed_expectations = failedExpectations
        self._id = id
        self._description = description
        self._pending_reason = pendingReason

    @property
    def status(self):
        return self._status

    @property
    def fullName(self):
        return self._full_name

    @property
    def failedExpectations(self):
        return self._failed_expectations

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def pendingReason(self):
        return self._pending_reason