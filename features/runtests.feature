Feature: Running tests

  Scenario: Plain project
    Given I have a project
    And I install the jasmine distribution
    When I run the jasmine command
    Then I should see my tests run