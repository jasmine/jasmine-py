# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import argparse
import socket
import sys

from .standalone import app as App
from jasmine.ci import CIRunner


def standalone():
    parser = argparse.ArgumentParser(description='Jasmine Standalone')
    parser.add_argument('-p', '--port', type=int, default=8888,
                        help='The port of the Jasmine html runner')
    parser.add_argument('-o', '--host', type=str, default='127.0.0.1',
                        help='The host of the Jasmine html runner')
    args = parser.parse_args()

    if _check_for_config():
        try:
            App.run(host=args.host, port=args.port, debug=True)
        except socket.error:
            sys.stdout.write('Socket unavailable')


def continuous_integration():
    parser = argparse.ArgumentParser(description='Jasmine-CI')
    parser.add_argument('-b', '--browser', type=str,
                        help='The selenium driver to utilize')
    parser.add_argument('-l', '--logs', action='store_true',
                        help='Displays browser logs')
    args = parser.parse_args()

    if _check_for_config():
        CIRunner().run(browser=args.browser, logs=args.logs)


def _check_for_config():
    project_path = os.path.realpath(os.path.dirname(__name__))
    config_file = os.path.join(
        project_path,
        "spec/javascripts/support/jasmine.yml"
    )

    config_exists = os.path.exists(config_file)
    if not config_exists:
        print("Could not find your config file at {0}".format(config_file))
    return config_exists


def _query(question):

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
    from jasmine.console import Formatter

    spec_dir = os.path.join(os.getcwd(), 'spec/javascripts/')

    print(Formatter.JASMINE_HEADER)

    print('Spec directory')

    msg = "About to create {0}... is this okay?".format(spec_dir)
    if _query(msg):
        print('making spec/javascripts')
        mkdir_p(spec_dir)

    yaml_dir = os.path.join(spec_dir, 'support')
    yaml_file_path = os.path.join(yaml_dir, 'jasmine.yml')

    print(("*" * 80) + '\n\nConfig yaml')

    if os.path.exists(yaml_file_path):
        print('found existing {0}, not overwriting'.format(yaml_file_path))
    else:
        msg = "About to create {0}... is this okay?".format(yaml_file_path)
        if _query(msg):
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
# Return an array of filepaths relative to src_dir
# to include before jasmine specs.
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
# Return an array of stylesheet filepaths relative
# to src_dir to include before jasmine specs.
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
# Return an array of filepaths relative to spec_dir
# to include before jasmine specs.
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
# Source directory path. Your src_files must be returned
# relative to this path. Will use root if left blank.
# Default: project root
#
# EXAMPLE:
#
# src_dir: public
#
src_dir:

# spec_dir
#
# Spec directory path. Your spec_files must be returned
# relative to this path.
# Default: spec/javascripts
#
# EXAMPLE:
#
# spec_dir: spec/javascripts
#
spec_dir: spec/javascripts
"""
