# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import argparse
import socket
import sys
from jasmine.config import Config

from jasmine.standalone import JasmineApp
from jasmine.ci import CIRunner


def standalone():
    parser = argparse.ArgumentParser(description='Jasmine Standalone')
    parser.add_argument('-p', '--port', type=int, default=8888,
                        help='The port of the Jasmine html runner')
    parser.add_argument('-o', '--host', type=str, default='127.0.0.1',
                        help='The host of the Jasmine html runner')
    args = parser.parse_args()

    if _check_for_config():
        jasmine_config = _load_config()
        try:
            jasmine_app = JasmineApp(jasmine_config=jasmine_config)
            jasmine_app.app.run(host=args.host, port=args.port, debug=True)
        except socket.error:
            sys.stdout.write('Socket unavailable')


def continuous_integration():
    parser = argparse.ArgumentParser(description='Jasmine-CI')
    parser.add_argument('-b', '--browser', type=str,
                        help='The selenium driver to utilize')
    parser.add_argument('-l', '--logs', action='store_true',
                        help='Displays browser logs')
    parser.add_argument('-s', '--seed', type=str,
                        help='Seed for random spec order')
    args = parser.parse_args()

    if _check_for_config():
        jasmine_config = _load_config()
        jasmine_app = JasmineApp(jasmine_config=jasmine_config)
        CIRunner(jasmine_config=jasmine_config).run(
            browser=args.browser,
            show_logs=args.logs,
            seed=args.seed,
            app=jasmine_app.app,
        )


def _config_paths():
    project_path = os.path.realpath(os.path.dirname(__name__))
    config_file = os.path.join(
        project_path,
        "spec/javascripts/support/jasmine.yml"
    )
    return config_file, project_path


def _check_for_config():
    config_file, _ = _config_paths()

    config_exists = os.path.exists(config_file)
    if not config_exists:
        print("Could not find your config file at {0}".format(config_file))
    return config_exists


def _load_config():
    config_file, project_path = _config_paths()
    return Config(config_file, project_path=project_path)


def query(question):
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
    from jasmine.console_formatter import ConsoleFormatter

    spec_dir = os.path.join(os.getcwd(), 'spec/javascripts/')

    print(ConsoleFormatter.JASMINE_HEADER)

    print('Spec directory')

    msg = "About to create {0}... is this okay?".format(spec_dir)
    if query(msg):
        print('making spec/javascripts')
        mkdir_p(spec_dir)

    yaml_dir = os.path.join(spec_dir, 'support')
    yaml_file_path = os.path.join(yaml_dir, 'jasmine.yml')

    print(("*" * 80) + '\n\nConfig yaml')

    if os.path.exists(yaml_file_path):
        print('found existing {0}, not overwriting'.format(yaml_file_path))
    else:
        msg = "About to create {0}... is this okay?".format(yaml_file_path)
        if query(msg):
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

# stop_spec_on_expectation_failure
#
# Stop executing each spec on the first expectation failure.
# Default: false
#
# EXAMPLE:
#
# stop_spec_on_expectation_failure: true
#
stop_spec_on_expectation_failure:

# random
#
# Run specs in semi-random order.
# Default: false
#
# EXAMPLE:
#
# random: true
#
random:
"""
