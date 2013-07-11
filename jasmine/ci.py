import threading
import sys

from selenium.webdriver.support.wait import WebDriverWait
from splinter import Browser

from cherrypy import wsgiserver

from jasmine import App
from jasmine.console import Parser, Formatter

import socket


class CIRunner(object):
    class TestServerThread(threading.Thread):
        def run(self):
            ports = self.possible_ports("localhost:80,8889-9999")

            for index, port in enumerate(ports):
                try:
                    self.server = wsgiserver.CherryPyWSGIServer(('localhost', port), App)
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

        for index, result in results.iteritems():
            pr = {
                'status': result['result'],
                'fullName': fullNames[int(index)]
            }

            failed_expectations = []
            for message in result['messages']:
                if 'stack' in message:
                    failed_expectations.append({'stack': message['stack']})

            if failed_expectations:
                pr.update(failedExpectations=failed_expectations)

            processed.append(pr)

        return processed

    def run(self):
        try:
            test_server = self.TestServerThread()
            test_server.start()

            browser = Browser('firefox')
            browser.visit("http://localhost:{}/".format(test_server.port))



            WebDriverWait(browser.driver, 100).until(
                lambda driver: driver.execute_script("return window.jsApiReporter.finished;")
            )

            browser.execute_script("""
                for (k in jsApiReporter.results()) {
                    var result = jsApiReporter.results()[k];
                    var messages = result.messages;

                    for (var i = 0; i < messages.length; i++) {
                        if (result.result === 'failed') {
                            messages[i].stack = messages[i].trace.stack;
                        }
                    }
                }
            """)

            results = browser.evaluate_script("window.jsApiReporter.results()")
            suites = browser.evaluate_script("window.jsApiReporter.suites()")

            spec_results = self._process_results(suites, results)

            results = Parser().parse(spec_results)
            formatter = Formatter(results)

            sys.stdout.write(formatter.format())
        finally:
            browser.quit()
            test_server.join()

if __name__ == "__main__":
    CIRunner().run()