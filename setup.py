import re
from setuptools import setup, find_packages

requirements = []
non_pypi_requirements = []

with open("requirements.txt", 'r') as f:
    for requirement in f:
        requirement = requirement.strip()

        if requirement.startswith("#") or not requirement:
            continue
        elif requirement.startswith("http"):
            non_pypi_requirements.append(requirement)
            requirements.append(
                re.match(r'.*#egg=(?P<egg>.*)', requirement).group('egg')
            )
        else:
            requirements.append(requirement)

setup(
    name="jasmine",
    version="2.3.0",
    url="http://pivotal.github.io/jasmine/",
    author="Pivotal Labs",
    author_email="jasmine-js@googlegroups.com",
    description=('Jasmine is a Behavior Driven Development'
                 ' testing framework for JavaScript.'
                 ' It does not rely on browsers, DOM,'
                 ' or any JavaScript framework.'
                 ' Thus it\'s suited for websites, '
                 'Node.js (http://nodejs.org) projects,'
                 ' or anywhere that JavaScript can run.'),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ],

    packages=find_packages(),
    package_data={'jasmine.django.templates': ['*.html']},
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'jasmine = jasmine.entry_points:standalone',
            'jasmine-ci = jasmine.entry_points:continuous_integration',
            'jasmine-install = jasmine.entry_points:install'
        ]
    },

    install_requires=requirements,

    dependency_links=non_pypi_requirements
)
