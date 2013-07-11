from __future__ import absolute_import
import os

import sys
import getopt
import socket

if __name__ == "__main__":
    __package__ = "jasmine.bin"

    sys.path = [os.path.join(os.path.dirname(__file__), '../..')] + sys.path

    from jasmine import App

    port_arg = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:", ["port="])
    except getopt.GetoptError:
        sys.stdout.write('python jasmine/standalone.py -p <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-p', '--port']:
            try:
                port_arg = int(arg)
            except ValueError:
                pass
    port = port_arg if port_arg and 0 <= port_arg <= 65535 else 8888
    try:
        App.run(port=port, debug=True)
    except socket.error:
        sys.stdout.write('Socket unavailable')
