# Jasmine... For Python!
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjasmine%2Fjasmine-py.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fjasmine%2Fjasmine-py?ref=badge_shield)


[![Build Status](https://circleci.com/gh/jasmine/jasmine-py.svg?style=shield)](https://circleci.com/gh/jasmine/jasmine-py)

The [Jasmine](http://github.com/jasmine/jasmine) Python package contains helper code for developing Jasmine projects for Python-based web projects (Django, Flask, etc.) or for JavaScript projects where Python is a welcome partner. It serves up a project's Jasmine suite in a browser so you can focus on your code instead of manually editing script tags in the Jasmine runner HTML file.

For documentation on writing Jasmine tests, check out the [Jasmine Documentation site](http://jasmine.github.io/).

## Contributing

Please read the [contributor's guide](https://github.com/jasmine/jasmine-py/blob/main/.github/CONTRIBUTING.md).


## Contents
This package contains:

* A small server that builds and executes a Jasmine suite for a project
* A command line script to run your tests (handy for continuous integration)

You can get all of this by: `pip install jasmine` or by adding `jasmine` to your `requirements.txt`.

## \__init__ A Project

To initialize a project for Jasmine:

	$ jasmine init

This will create a spec directory and configuration yaml template for you.

## Configuration

Customize `spec/javascripts/support/jasmine.yml` to enumerate the source files, stylesheets, and spec files you would like the Jasmine runner to include.
You may use dir glob strings.

## Usage

#### Standalone Server
Start the Jasmine server:

	$ jasmine server

Point your browser to `localhost:8888`. The suite will run every time this page is re-loaded.

Start Jasmine on a different port:

	$ jasmine server -p 1337

Point your browser to `localhost:1337`.

For a full list of commands, type `jasmine -h`

#### Continuous Integration

For Continuous Integration environments, add this task to the project build steps:

	$ jasmine ci

The browser used by selenium can be changed by exporting `JASMINE_BROWSER`

    $ export JASMINE_BROWSER=phantomjs
    $ jasmine ci

or adding `--browser` to `jasmine-ci`

	$ jasmine ci --browser phantomjs

For a full list of commands, type `jasmine ci -h`

## Support

Documentation: [jasmine.github.io](https://jasmine.github.io)
Jasmine Mailing list: [jasmine-js@googlegroups.com](mailto:jasmine-js@googlegroups.com)
Twitter: [@jasminebdd](http://twitter.com/jasminebdd)

Please file issues here at Github

Copyright (c) 2008-2017 Pivotal Labs. This software is licensed under the MIT License.


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjasmine%2Fjasmine-py.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fjasmine%2Fjasmine-py?ref=badge_large)
