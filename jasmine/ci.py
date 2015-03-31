import os
import threading
import sys
import socket

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from cherrypy import wsgiserver

from jasmine.console_formatter import ConsoleFormatter
from jasmine.js_api_parser import Parser


class TestServerThread(threading.Thread):

    def __init__(self, app=None, *args, **kwargs):
        super(TestServerThread, self).__init__(*args, **kwargs)
        self.server = None
        self.port = None
        self.app = app

    def run(self):
        ports = self.possible_ports("localhost:80,8889-9999")

        for index, port in enumerate(ports):
            try:
                self.server = wsgiserver.CherryPyWSGIServer(
                    ('localhost', port),
                    self.app,
                    request_queue_size=2048
                )
                self.port = port
                self.server.start()
                break
            except socket.error:
                continue

    def join(self, timeout=None):
        self.server.stop()

    def possible_ports(self, specified_address):
        possible_ports = []

        try:
            host, port_ranges = specified_address.split(':')
            for port_range in port_ranges.split(','):
                # A port range can be of either form: '8000' or '8000-8010'.
                extremes = list(map(int, port_range.split('-')))
                assert len(extremes) in [1, 2]
                if len(extremes) == 1:
                    # Port range of the form '8000'
                    possible_ports.append(extremes[0])
                else:
                    # Port range of the form '8000-8010'
                    for port in range(extremes[0], extremes[1] + 1):
                        possible_ports.append(port)
        except Exception:
            raise 'Invalid address ("{}") for live server.'.format(
                specified_address
            )

        return possible_ports


class CIRunner(object):

    def __init__(self, jasmine_config=None):
        self.jasmine_config = jasmine_config

    def run(self, browser=None, show_logs=False, app=None):
        try:
            test_server = self._start_test_server(app, browser)

            jasmine_url = "http://localhost:{0}/".format(test_server.port)
            if self.jasmine_config.stop_spec_on_expectation_failure():
                jasmine_url += "?throwFailures=true"
            self.browser.get(jasmine_url)

            WebDriverWait(self.browser, 100).until(
                lambda driver:
                driver.execute_script("return jsApiReporter.finished;")
            )

            parser = Parser()
            spec_results = self._get_spec_results(parser)
            suite_results = self._get_suite_results(parser)
            show_logs = self._get_browser_logs(show_logs=show_logs)

            formatter = ConsoleFormatter(
                spec_results=spec_results,
                suite_results=suite_results,
                browser_logs=show_logs
            )
            sys.stdout.write(formatter.format())
            if (len(list(formatter.results.failed())) or
                    len(list(formatter.suite_results.failed()))):
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

    def _get_browser_logs(self, show_logs):
        log = []
        if show_logs:
            try:
                log = self.browser.get_log('browser')
            except WebDriverException:
                pass
        return log
