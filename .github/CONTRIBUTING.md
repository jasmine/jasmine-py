# Contributing

We welcome your contributions! Thanks for helping make Jasmine a better project for everyone. Please review the backlog and discussion lists before starting work.  What you're looking for may already have been done. If it hasn't, the community can help make your contribution better. If you want to contribute but don't know what to work on, [issues tagged ready for work](https://github.com/jasmine/jasmine-py/labels/ready%20for%20work) should have enough detail to get started.

## Links

- [Jasmine Google Group](http://groups.google.com/group/jasmine-js)
- [Jasmine-dev Google Group](http://groups.google.com/group/jasmine-js-dev)
- [Jasmine on PivotalTracker](https://www.pivotaltracker.com/n/projects/10606)

## Setup

The Jasmine python package tests itself against multiple versions of Python. However, in most cases you can contribute successfully even if you only have one version installed. To get started:

1. Make sure you have Python installed.
1. Get pip: http://www.pip-installer.org/en/latest/installing.html
1. Get virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
1. `source /usr/local/bin/virtualenvwrapper.sh`
1. `git clone` this repo
1. Make an environment: `mkvirtualenv jasminePy`
1. Use that environment: `workon jasminePy`
1. Install dependencies: `pip install -r requirements.txt && pip install -r requirements_dev.txt`
1. Run specs: `py.test`

If you want to run the tests against all supported versions of Python:

1. Install Python 2.6, 2.7, 3.4, 3.5, and pypy.
1. Run specs: `detox -n 1`

## Submitting a Pull Request

Please submit pull requests via feature branches using the semi-standard workflow of:

```bash
git clone git@github.com:yourUserName/jasmine-py.git              # Clone your fork
cd jasmine-py                                                     # Change directory
git remote add upstream https://github.com/jasmine/jasmine-py.git # Assign original repository to a remote named 'upstream'
git fetch upstream                                                # Pull in changes not present in your local repository
git checkout -b my-new-feature                                    # Create your feature branch
git commit -am 'Add some feature'                                 # Commit your changes
git push origin my-new-feature                                    # Push to the branch
```

Once you've pushed a feature branch to your forked repo, you're ready to open a pull request. We favor pull requests with very small, single commits with a single purpose.

Note that we use Travis for Continuous Integration. We only accept green pull requests.

