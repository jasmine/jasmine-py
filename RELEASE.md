# Releasing jasmine-py

1. Special step for 3.99: After merging to main, remove the jasmine-core
dependency from requirements_dev.txt.

1.  Install [twine](https://github.com/pypa/twine)
2. Make sure that all specs are green on CI.
3. Generate release notes in `release_notes` using the Anchorman gem and edit
them.
4. Update the version and jasmine-core version in `setup.py`.
5. Commit the release notes and `setup.py` change.
6. Tag the commit.
7. `git push`
8. `git push --tags`
9. Wait for Circle CI to go green.
10. `python setup.py sdist`
11. `twine upload dist/jasmine-<version>.tar.gz` You will need pypi credentials to upload the egg.
12. Edit the tag on Github and add a reference to the release notes.
