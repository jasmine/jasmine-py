from jasmine.js_api_parser import Parser

def test_parser_should_return_a_correct_results_list():
    parser = Parser()

    results = parser.parse([
        {u'status': u'failed',
         u'fullName': u'Globals refer to the most holy.',
         u'failedExpectations': [{u'actual': u'Batman',
                                  u'matcherName': u'toEqual',
                                  u'passed': False,
                                  u'expected': u'PANTS',
                                  u'message': u"Expected 'Batman' to equal 'PANTS'.",
                                  u'stack': u"stack\n    stack\n    stack"}],

         u'passedExpectations': [{u'matcherName': u'toBeTruthy',
                                  u'expected': [],
                                  u'actual': True,
                                  u'message': u'Passed.',
                                  u'stack': u'',
                                  u'passed': True}],
         u'id': 0,
         u'description': u'refer to the most holy',
         u'pendingReason': u'pending reason'}
    ])

    assert len(results) == 1
    assert results[0].status == 'failed'
    assert results[0].fullName == 'Globals refer to the most holy.'
    assert len(results[0].failedExpectations) == 1
    assert results[0].failedExpectations[0]['stack'] == "stack\n    stack\n    stack"
    assert results[0].failedExpectations[0]['message'] == "Expected 'Batman' to equal 'PANTS'."
    assert results[0].pendingReason == u'pending reason'


