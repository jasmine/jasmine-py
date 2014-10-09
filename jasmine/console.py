import datetime
from collections import namedtuple
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from future_builtins import filter
except ImportError:
    pass


class Formatter(object):
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

    def __init__(self, results, **kwargs):
        self.colors = kwargs.get('colors', True)
        self.browser_logs = kwargs.get('browser_logs', [])
        self.suite_results = ResultList(kwargs.get('suite_results', []))
        self.results = ResultList(results)

    def colorize(self, color, text):
        if not self.colors:
            return text

        return self.COLORS[color] + text + self.COLORS['none']

    def format(self):
        return (
            self.JASMINE_HEADER +
            self.format_progress() + "\n\n" +
            self.format_summary() + "\n\n" +
            self.format_suite_failure() + "\n\n" +
            self.format_browser_logs() +
            self.format_failures() +
            self.format_pending()
        )

    def format_progress(self):
        output = ""

        for result in self.results:
            if result.status == "passed":
                output += self.colorize('green', '.')
            elif result.status == "failed":
                output += self.colorize('red', 'X')
            else:
                output += self.colorize('yellow', '*')

        return output

    def format_summary(self):
        output = "{0} specs, {1} failed".format(len(self.results), len(list(self.results.failed())))

        if self.results.pending():
            output += ", {0} pending".format(len(list(self.results.pending())))

        return output

    def format_suite_failure(self, colors=False):
        output = ""
        for result in self.suite_results:
            if(result.failedExpectations):
                output += self.colorize('red', '\nAfter All {0}'.format(result.failedExpectations[0]['message']))
        return output

    def format_browser_logs(self):
        output = ""
        if list(self.results.failed()):
            output = "Browser Session Logs:\n"
            for log in self.browser_logs:
                output += "  [{0} - {1}] {2}\n".format(
                    datetime.datetime.fromtimestamp(log['timestamp'] / 1000.0),
                    log['level'],
                    log['message']
                )
            output += "\n"
        return output

    def format_failures(self):
        output = ""
        for failure in self.results.failed():
            output += self.colorize('red', failure.fullName) + "\n" +\
                self.clean_stack(failure.failedExpectations[0]['stack']) + "\n"

        return output

    def clean_stack(self, stack):
        if not stack:
            return ""

        def dirty(stack_line):
            return "__jasmine__" in stack_line or "__boot__" in stack_line

        return "\n".join([stack_line for stack_line in stack.split("\n") if not dirty(stack_line)])

    def format_pending(self):
        output = ""

        for pending in self.results.pending():
            output += self.colorize('yellow', pending.fullName + "\n")
        return output


class ResultList(list):
    def passed(self):
        return self._filter_status('passed')

    def failed(self):
        return self._filter_status('failed')

    def pending(self):
        return self._filter_status('pending')

    def _filter_status(self, status):
        return filter(lambda x: x.status == status, self)


RESULT_FIELDS = ['status', 'fullName', 'failedExpectations', 'id', 'description']

class Parser(object):
    def parse(self, items):
        return ResultList([Result(**item) for item in self._filter_fields(items)])

    def _filter_fields(self, raw_items):
        filtered_items = []
        for item in raw_items:
            filtered_items.append(dict(((k,v) for k,v in item.items() if k in RESULT_FIELDS)))
        return filtered_items


class Result(namedtuple('Result', RESULT_FIELDS)):
    def __new__(cls, status=None, fullName=None, failedExpectations=[], id=None, description=None):
        # Constructor arguments correspond to RESULT_FIELDS
        return super(Result, cls).__new__(cls, status, fullName, failedExpectations, id, description)

