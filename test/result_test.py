from jasmine.js_api_parser import Result


def test_result():
    status = 'status'
    full_name = 'fullName'
    failed_expectations = 'failedExpectations'
    id = 'id'
    description = 'description'
    pending_reason = 'pendingReason'

    result = Result(
        status=status,
        fullName=full_name,
        failedExpectations=failed_expectations,
        id=id,
        description=description,
        pendingReason=pending_reason
    )

    assert result.status == status
    assert result.fullName == full_name
    assert result.failedExpectations == failed_expectations
    assert result.id == id
    assert result.description == description
    assert result.pendingReason == pending_reason