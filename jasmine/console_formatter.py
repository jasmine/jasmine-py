import datetime


class ConsoleFormatter(object):
    COLORS = {
        'red': "\033[0;31m",
        'green': "\033[0;32m",
        'yellow': "\033[0;33m",
        'none': "\033[0m"
    }

    JASMINE_HEADER = """
      _                     _
     | |                   (_)
     | | __ _ ___ _ __ ___  _ _ __   ___
 _   | |/ _` / __| '_ ` _ \| | '_ \ / _ \\
| |__| | (_| \__ \ | | | | | | | | |  __/
 \____/ \__,_|___/_| |_| |_|_|_| |_|\___|

"""

    def __init__(self, spec_results, suite_results, browser_logs, seed=None, colors=True):
        self.results = spec_results
        self.suite_results = suite_results
        self.browser_logs = browser_logs
        self.colors = colors
        self.seed = seed

    def format(self):
        return (
            self.JASMINE_HEADER +
            self.format_progress() + "\n\n" +
            self.format_summary() + "\n\n" +
            self.format_suite_failure() +
            self.format_browser_logs() +
            self.format_spec_failures() +
            self.format_pending() +
            self.format_deprecations()
        )

    def format_progress(self):
        output = ""

        for result in self.results:
            if result.status == "passed":
                output += self._colorize('green', '.')
            elif result.status == "failed":
                output += self._colorize('red', 'X')
            elif result.status == 'pending':
                output += self._colorize('yellow', '*')

        return output

    def format_summary(self):
        output = "{0} specs, {1} failed".format(
            self._enabled_spec_count(),
            len(self.results.failed())
        )

        if self.results.pending():
            output += ", {0} pending".format(len(self.results.pending()))

        if self.seed:
            output += "\nRandomized with seed {0} (jasmine-ci --seed {0})".format(self.seed)
        return output

    def _enabled_spec_count(self):
        return len(self.results.enabled())

    def format_suite_failure(self):
        output = ""
        for failed_suite in self.suite_results.failed():
            for expectation in failed_suite.failed_expectations:
                output += self._format_expectation_failure(expectation)
        if output:
            output = self._colorize('red', 'Suite Failures:\n') + output
        return output

    def format_spec_failures(self):
        output = ""
        for failed_spec in self.results.failed():
            output += self._colorize('red', failed_spec.full_name) + "\n"
            for expectation in failed_spec.failed_expectations:
                output += self._format_expectation_failure(expectation)
        return output

    def format_browser_logs(self):
        output = ""
        if self.results.failed() and self.browser_logs:
            output = "Browser Session Logs:\n"
            for log in self.browser_logs:
                output += "  [{0} - {1}] {2}\n".format(
                    datetime.datetime.fromtimestamp(log['timestamp'] / 1000.0),
                    log['level'],
                    log['message']
                )
            output += "\n"
        return output

    def clean_stack(self, stack):
        if not stack:
            return ""

        def _dirty(stack_line):
            return "__jasmine__" in stack_line or "__boot__" in stack_line

        return "\n".join([
            stack_line
            for stack_line in stack.split("\n")
            if not _dirty(stack_line)
        ])

    def format_pending(self):
        output = ""

        for pending in self.results.pending():
            output += self._colorize('yellow', pending.full_name + "\n")
            if pending.pending_reason:
                output += "  Reason: {0}\n".format(pending.pending_reason)

        return output

    def format_deprecations(self):
        output = ""
        spec_deprecations = [result for result in self.results if result.deprecation_warnings]
        for deprecation in spec_deprecations:
            output += self._colorize('yellow', deprecation.full_name + "\n")
            for warning in deprecation.deprecation_warnings:
                output += self._format_expectation_failure(warning)
        suite_deprecations = [result for result in self.suite_results if result.deprecation_warnings]
        for deprecation in suite_deprecations:
            output += self._colorize('yellow', deprecation.full_name + "\n")
            for warning in deprecation.deprecation_warnings:
                output += self._format_expectation_failure(warning)
        if output:
            output = 'Deprecations:\n' + output

        return output

    def _format_expectation_failure(self, expectation):
            output = "  " + expectation['message'] + "\n"
            if 'stack' in expectation:
                output += "  " + self.clean_stack(expectation['stack']) + "\n"
            return output

    def _colorize(self, color, text):
        if not self.colors:
            return text

        return self.COLORS[color] + text + self.COLORS['none']
