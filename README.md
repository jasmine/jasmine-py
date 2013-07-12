# Jasmine... For Python!

<a title="Build at Travis CI" href="https://travis-ci.org/pivotal/jasmine-py"><img src="https://api.travis-ci.org/pivotal/jasmine-py.png" /></a>

The [Jasmine](http://github.com/pivotal/jasmine) Python package contains helper code for developing Jasmine projects for Python-based web projects (Django, Flask, etc.) or for JavaScript projects where Python is a welcome partner. It serves up a project's Jasmine suite in a browser so you can focus on your code instead of manually editing script tags in the Jasmine runner HTML file.

## Contents
This package contains:

* A small server that builds and executes a Jasmine suite for a project
* A Django view to display test results
* A command line script to run your tests (handy for CI)
* And more...?

You can get all of this by: `pip install jasmine-py` or by adding `jasmine-py` to your `requirements.txt`.

## \__init__ A Project

To initialize a project for Jasmine, it depends on your web framework

For Django support,

* Add 'jasmine.django' to INSTALLED_APPS in your setting.py
* To display test results within your application, add a route to your urls.py: `url(r'^jasmine/', include('jasmine.django.urls', namespace='jasmine'))`. Test results are now visible at your.django.app/jasmine 
    * You may wish to protect this URL so it does not appear in the production deploy of your app

For any other project (Pylons, Flask, etc)

* Drop a `jasmine.yml` into `spec/javascripts/support/jasmine.yml`. Run `jasmine` and visit `http://localhost:8888`

## Configuration

Customize `spec/javascripts/support/jasmine.yml` to enumerate the source files, stylesheets, and spec files you would like the Jasmine runner to include.
You may use dir glob strings.


## Usage

Start the Jasmine server:

`jasmine`

Point your browser to `localhost:8888`. The suite will run every time this page is re-loaded.

Start Jasmine on a different port:

`jasmine -p 1337`

Point your browser to `localhost:1337`.

For Continuous Integration environments, add this task to the project build steps:

`jasmine-ci`

if you are using Django, you can also run:

`./manage.py run_jasmine`


The browser used by selenium can be changed by exporting `JASMINE_BROWSER` 

    $ export JASMINE_BROWSER=chrome
    $ jasmine-ci

or adding `--browser=` to `jasmine-ci`

    $ jasmine-ci --browser=firefox


## Support

Jasmine Mailing list: [jasmine-js@googlegroups.com](mailto:jasmine-js@googlegroups.com)
Twitter: [@jasminebdd](http://twitter.com/jasminebdd)

Please file issues here at Github

Copyright (c) 2008-2013 Pivotal Labs. This software is licensed under the MIT License.
