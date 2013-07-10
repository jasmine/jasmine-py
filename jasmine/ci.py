import threading
import sys

from gevent.wsgi import WSGIServer, socket
from selenium.webdriver.support.wait import WebDriverWait
from splinter import Browser
from gevent import monkey

from jasmine import App
from jasmine.console import Parser, Formatter


class CIRunner(object):
    class TestServerThread(threading.Thread):
        def run(self):
            ports = self.possible_ports("localhost:80,8889-9999")

            for index, port in enumerate(ports):
                try:
                    self.server = WSGIServer(('localhost', port), application=App, log=None)
                    self.port = port
                    self.server.serve_forever()
                except socket.error:
                    continue

        def join(self):
            self.server.kill()

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

    def run(self):
        try:
            monkey.patch_all()

            test_server = self.TestServerThread()
            test_server.start()

            browser = Browser('phantomjs')
            browser.visit("http://localhost:{}/".format(test_server.port))

            WebDriverWait(browser.driver, 100).until(
                lambda driver: driver.execute_script("return window.jsApiReporter.finished;")
            )

            spec_results = []
            index = 0
            batch_size = 50

            while True:
                results = browser.evaluate_script("window.jsApiReporter.specResults({0}, {1})".format(index, batch_size))
                spec_results.extend(results)
                index = len(results)

                if not index == batch_size:
                    break

            results = Parser().parse(spec_results)
            formatter = Formatter(results)

            sys.stdout.write(formatter.format())
        finally:
            browser.quit()
            test_server.join()

if __name__ == "__main__":
    CIRunner().run()