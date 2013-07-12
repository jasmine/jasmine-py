from .config import Config
from .standalone import app as App


def standalone():
    import sys
    import getopt
    import socket

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


def continuous_integration():
    from jasmine.ci import CIRunner

    CIRunner().run()


def install():
    # create spec_dir
    # drop a jasmine.yml template with defaults
    pass