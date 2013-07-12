# -*- coding: utf-8 -*-

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
    import argparse

    parser = argparse.ArgumentParser(description='Jasmine-CI')
    parser.add_argument('--browser', type=str,
                        help='the selenium driver to utilize')

    args = parser.parse_args()

    CIRunner().run(browser=args.browser)


def _query(question):
    import sys

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    prompt = " [Y/n] "

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice == '':
            return True
        elif choice in valid:
            return valid[choice]


def install():
    import os

    basepath = os.getcwd()

    spec_dir = os.path.join(basepath, 'spec/javascripts/')

    print """
 ▬▬ι═══════ﺤ -═══════ι▬▬
      Jasmine Setup
 ▬▬ι═══════ﺤ -═══════ι▬▬
"""

    print 'Spec directory'
    if _query("About to create {0}... is this okay?".format(spec_dir)):
        print 'making spec/javascripts'
        # os.mkdir(spec_dir)

    yaml_dir = os.path.join(spec_dir, 'support')
    yaml_file_path = os.path.join(yaml_dir, 'jasmine.yml')

    print '\n▬▬ι═══════ﺤ\nConfig yaml'
    if _query("About to create {0}... is this okay?".format(yaml_file_path)):
        print 'making spec/javascripts/support'
        # os.mkdir(yaml_dir)
        print 'making spec/javascripts/support/jasmine.yml'
        # try:
        #     open(yaml_file_path, 'w')
        # except IOError:
        #     pass

