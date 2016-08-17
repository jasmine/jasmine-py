import itertools
import os
import socket
import sys
import threading

from six.moves import range
from cherrypy import wsgiserver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait

from jasmine.console_formatter import ConsoleFormatter
from jasmine.js_api_parser import Parser
from jasmine.url_builder import JasmineUrlBuilder


class TestServerThread(threading.Thread):

    def __init__(self, app=None, *args, **kwargs):
        super(TestServerThread, self).__init__(*args, **kwargs)
        self.server = None
        self.port = None
        self.app = app

    def run(self):
        ports = self._possible_ports()

        for port in ports:
            try:
                self._attempt_server_start(port)
                break
            except socket.error:
                continue

    def join(self, timeout=None):
        self.server.stop()

    def _attempt_server_start(self, port):
        self.server = wsgiserver.CherryPyWSGIServer(
            ('localhost', port),
            self.app,
            request_queue_size=2048
        )
        self.port = port
        self.server.start()

    def _possible_ports(self):
        return itertools.chain(range(80, 81, 1), range(8889, 10000))


class CIRunner(object):

    def __init__(self, jasmine_config=None):
        self.jasmine_config = jasmine_config

    def run(self, browser=None, show_logs=False, app=None, seed=None):
        try:
            test_server = self._start_test_server(app, browser)

            url_builder = JasmineUrlBuilder(jasmine_config=self.jasmine_config)
            jasmine_url = url_builder.build_url(test_server.port, seed)
            self.browser.get(jasmine_url)

            WebDriverWait(self.browser, 100).until(
                lambda driver:
                driver.execute_script("return jsApiReporter.finished;")
            )

            parser = Parser()
            spec_results = self._get_spec_results(parser)
            top_suite_results = self._get_top_suite_results(parser)
            suite_results = self._get_suite_results(parser) + top_suite_results
            show_logs = self._get_browser_logs(show_logs=show_logs)
            actual_seed = self._get_seed()

            formatter = ConsoleFormatter(
                spec_results=spec_results,
                suite_results=suite_results,
                browser_logs=show_logs,
                seed=actual_seed
            )
            sys.stdout.write(formatter.format())
            if len(spec_results.failed()) or len(suite_results.failed()):
                sys.exit(1)
        finally:
            if hasattr(self, 'browser'):
                self.browser.close()
            if hasattr(self, 'test_server'):
                self.test_server.join()

    def _start_test_server(self, app, browser):
        test_server = TestServerThread(app=app)
        test_server.start()
        driver = browser if browser \
            else os.environ.get('JASMINE_BROWSER', 'firefox')
        try:
            webdriver = __import__(
                "selenium.webdriver.{0}.webdriver".format(driver),
                globals(), locals(), ['object'], 0
            )

            self.browser = webdriver.WebDriver()
        except ImportError as e:
            print("Browser {0} not found".format(driver))
        return test_server

    def _get_spec_results(self, parser):
        spec_results = []
        index = 0
        batch_size = 50
        while True:
            results = self.browser.execute_script(
                "return jsApiReporter.specResults({0}, {1})".format(
                    index,
                    batch_size
                )
            )
            spec_results.extend(results)
            index += len(results)

            if not len(results) == batch_size:
                break

        return parser.parse(spec_results)

    def _get_suite_results(self, parser):
        suite_results = []
        index = 0
        batch_size = 50
        while True:
            results = self.browser.execute_script(
                "return jsApiReporter.suiteResults({0}, {1})".format(
                    index,
                    batch_size
                )
            )

            suite_results.extend(results)
            index += len(results)

            if not len(results) == batch_size:
                break

        return parser.parse(suite_results)

    def _get_top_suite_results(self, parser):
        failed_expectations = self.browser.execute_script("return jsApiReporter.runDetails").get('failedExpectations')

        top_suite_result = {
            "failedExpectations": failed_expectations,
            "status": "failed" if len(failed_expectations) else "passed"
        }

        return parser.parse([top_suite_result])

    def _get_seed(self):
        order = self._get_order()
        is_random = order.get('random')
        seed = order.get('seed') if is_random else None
        return seed

    def _get_order(self):
        return self.browser.execute_script("return jsApiReporter.runDetails").get('order')

    def _get_browser_logs(self, show_logs):
        log = []
        if show_logs:
            try:
                log = self.browser.get_log('browser')
            except WebDriverException:
                pass
        return log
