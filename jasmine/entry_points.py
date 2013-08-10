# -*- coding: utf-8 -*-
from __future__ import print_function
from .standalone import app as App


def standalone():
    import sys
    import getopt
    import socket

    port_arg = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:", ["port="])
    except getopt.GetoptError:
        sys.stdout.write('jasmine.py -p <port>')
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

        try:
            choice = raw_input().lower()
        except NameError:
            choice = input().lower()

        if choice == '':
            return True
        elif choice in valid:
            return valid[choice]


def install():
    import os
    from jasmine.console import Formatter

    spec_dir = os.path.join(os.getcwd(), 'spec/javascripts/')

    print(Formatter.JASMINE_HEADER)

    print('Spec directory')

    if _query("About to create {0}... is this okay?".format(spec_dir)):
        print('making spec/javascripts')
        mkdir_p(spec_dir)

    yaml_dir = os.path.join(spec_dir, 'support')
    yaml_file_path = os.path.join(yaml_dir, 'jasmine.yml')

    print(("*" * 80) + '\n\nConfig yaml')

    if os.path.exists(yaml_file_path):
        print('found existing {0}, not overwriting'.format(yaml_file_path))
    else:
        if _query("About to create {0}... is this okay?".format(yaml_file_path)):
            print('making {0}'.format(yaml_dir))

            mkdir_p(yaml_dir)

            print('making {0}'.format(yaml_file_path))
            try:
                with open(yaml_file_path, 'w') as f:
                    f.write(YAML_TEMPLATE)
                    f.flush()
            except IOError:
                pass


def mkdir_p(path):
    import os
    import errno

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


YAML_TEMPLATE = """
# src_files
#
# Return an array of filepaths relative to src_dir to include before jasmine specs.
# Default: []
#
# EXAMPLE:
#
# src_files:
#   - lib/source1.js
#   - lib/source2.js
#   - dist/**/*.js
#
src_files:

# stylesheets
#
# Return an array of stylesheet filepaths relative to src_dir to include before jasmine specs.
# Default: []
#
# EXAMPLE:
#
# stylesheets:
#   - css/style.css
#   - stylesheets/*.css
#
stylesheets:

# helpers
#
# Return an array of filepaths relative to spec_dir to include before jasmine specs.
# Default: ["helpers/**/*.js"]
#
# EXAMPLE:
#
# helpers:
#   - helpers/**/*.js
#
helpers:
  - "helpers/**/*.js"

# spec_files
#
# Return an array of filepaths relative to spec_dir to include.
# Default: ["**/*[sS]pec.js"]
#
# EXAMPLE:
#
# spec_files:
#   - **/*[sS]pec.js
#
spec_files:
  - "**/*[Ss]pec.js"


# src_dir
#
# Source directory path. Your src_files must be returned relative to this path. Will use root if left blank.
# Default: project root
#
# EXAMPLE:
#
# src_dir: public
#
src_dir:

# spec_dir
#
# Spec directory path. Your spec_files must be returned relative to this path.
# Default: spec/javascripts
#
# EXAMPLE:
#
# spec_dir: spec/javascripts
#
spec_dir: spec/javascripts
"""