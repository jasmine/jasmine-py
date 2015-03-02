from jasmine.result import Result


def test_result():
    status = 'status'
    full_name = 'fullName'
    failed_expectations = 'failedExpectations'
    runnable_id = 'id'
    description = 'description'
    pending_reason = 'pendingReason'

    result = Result(
        status=status,
        full_name=full_name,
        failed_expectations=failed_expectations,
        runnable_id=runnable_id,
        description=description,
        pending_reason=pending_reason
    )

    assert result.status == status
    assert result.full_name == full_name
    assert result.failed_expectations == failed_expectations
    assert result.runnable_id == runnable_id
    assert result.description == description
    assert result.pending_reason == pending_reason