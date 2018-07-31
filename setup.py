from setuptools import setup, find_packages

setup(
    name="jasmine",
    version="3.1.2",
    url="http://jasmine.github.io",
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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
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
    package_data={'jasmine.templates': ['*.html']},
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'jasmine = jasmine.entry_points:begin'
        ]
    },

    install_requires=[
        'PyYAML==3.10',
        'Jinja2>=2.0, <3.0',
        'jasmine-core==3.1.0',
        'CherryPy>=11',
        'selenium>=3.0',
    ],
)
