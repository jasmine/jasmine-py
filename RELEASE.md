# Releasing jasmine-py

1.  Install [twine](https://github.com/pypa/twine)
2. Make sure that all specs are green on CI.
3. Generate release notes in `release_notes` using the Anchorman gem and edit
them.
4. Update the version and jasmine-core version in `setup.py`.
5. Commit the release notes and `package.json` change.
6. Tag the commit.
7. `git push main --tags`
8. Wait for Circle CI to go green.
9. `python setup.py sdist`
10. `twine upload dist/jasmine-<version>.tar.gz` You will need pypi credentials to upload the egg.
