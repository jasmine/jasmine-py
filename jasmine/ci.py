import os
import threading
import sys

from selenium.webdriver.support.wait import WebDriverWait

from cherrypy import wsgiserver

from jasmine.standalone import app as App
from jasmine.console import Parser, Formatter

import socket

class TestServerThread(threading.Thread):
    def run(self):
        ports = self.possible_ports("localhost:80,8889-9999")

        for index, port in enumerate(ports):
            try:
                self.server = wsgiserver.CherryPyWSGIServer(('localhost', port), App, request_queue_size=2048)
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
            raise 'Invalid address ("{}") for live server.'.format(specified_address)

        return possible_ports


class CIRunner(object):
    def _buildFullNames(self, leadin, children):
        fullNames = {}

        for child in children:
            name = " ".join([leadin, child['name']])

            if child['type'] == "spec":
                fullNames[child['id']] = name
            else:
                fullNames.update(self._buildFullNames(name, child['children']))

        return fullNames

    def _process_results(self, suites, results):
        processed = []

        fullNames = {}

        for suite in suites:
            fullNames.update(self._buildFullNames(suite['name'], suite['children']))

        for spec_id in sorted(results.keys(), key=lambda x: int(x)):
            result = results[spec_id]

            pr = {
                'status': result['result'],
                'fullName': fullNames[int(spec_id)]
            }

            failed_expectations = []
            for message in result['messages']:
                if 'stack' in message:
                    failed_expectations.append({'stack': message['stack']})

            if failed_expectations:
                pr.update(failedExpectations=failed_expectations)

            processed.append(pr)

        return processed

    def run(self, browser=None):
        try:
            test_server = TestServerThread()
            test_server.start()

            driver = browser if browser else os.environ.get('JASMINE_BROWSER', 'firefox')

            try:
                webdriver = __import__("selenium.webdriver.{0}.webdriver".format(driver), globals(), locals(), ['object'], 0)

                self.browser = webdriver.WebDriver()
            except ImportError as e:
                print("Browser {0} not found".format(driver))

            self.browser.get("http://localhost:{0}/".format(test_server.port))

            WebDriverWait(self.browser, 100).until(
                lambda driver: driver.execute_script("return window.jsApiReporter.finished;")
            )

            spec_results = []
            index = 0
            batch_size = 50

            while True:
                results = self.browser.execute_script("return window.jsApiReporter.specResults({0}, {1})".format(index, batch_size))
                spec_results.extend(results)
                index = len(results)

                if not index == batch_size:
                    break

            formatter = Formatter(spec_results)

            sys.stdout.write(formatter.format())
            if formatter.failed:
                sys.exit(1)
        finally:
            if hasattr(self, 'browser'):
                self.browser.close()
            if hasattr(self, 'test_server'):
                self.test_server.join()
