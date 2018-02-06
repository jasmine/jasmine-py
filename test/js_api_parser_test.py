from jasmine.js_api_parser import Parser


def test_parser_should_return_a_correct_results_list():
    parser = Parser()

    results = parser.parse([
        {
            u'status': u'failed',
            u'fullName': u'Globals refer to the most holy.',
            u'failedExpectations': [
                {
                    u'actual': u'Batman',
                    u'matcherName': u'toEqual',
                    u'passed': False,
                    u'expected': u'PANTS',
                    u'message': u"Expected 'Batman' to equal 'PANTS'.",
                    u'stack': u"stack\n    stack\n    stack"
                }
            ],

            u'passedExpectations': [
                {
                    u'matcherName': u'toBeTruthy',
                    u'expected': [],
                    u'actual': True,
                    u'message': u'Passed.',
                    u'stack': u'',
                    u'passed': True
                }
            ],
            u'deprecationWarnings': [
                {
                    u'message': u'old and busted',
                    u'stack': u'snacky stack'
                }
            ],
            u'id': 0,
            u'description': u'refer to the most holy',
            u'pendingReason': u'pending reason'
        }
    ])

    assert len(results) == 1
    assert results[0].status == 'failed'
    assert results[0].full_name == 'Globals refer to the most holy.'
    assert len(results[0].failed_expectations) == 1
    assert results[0].failed_expectations[0]['stack'] == "stack\n    stack\n    stack"
    assert results[0].failed_expectations[0]['message'] == "Expected 'Batman' to equal 'PANTS'."
    assert results[0].pending_reason == u'pending reason'
    assert len(results[0].deprecation_warnings) == 1
    assert results[0].deprecation_warnings[0]['message'] == "old and busted"
    assert results[0].deprecation_warnings[0]['stack'] == "snacky stack"


def test_parser_returns_an_empty_results_list_with_no_runnables():
    parser = Parser()
    results = parser.parse([])

    assert len(results) == 0


def test_parser_returns_all_failed_expectations():
    parser = Parser()

    results = parser.parse([
        {
            u'failedExpectations': [
                {u'actual': u'Expectation1'},
                {u'actual': u'Expectation2'},
                {u'actual': u'Expectation3'},
                {u'actual': u'Expectation4'},
            ],
        }
    ])

    assert len(results) == 1
    assert len(results[0].failed_expectations) == 4
    assert results[0].failed_expectations[0][u'actual'] == u'Expectation1'
    assert results[0].failed_expectations[1][u'actual'] == u'Expectation2'
    assert results[0].failed_expectations[2][u'actual'] == u'Expectation3'
    assert results[0].failed_expectations[3][u'actual'] == u'Expectation4'