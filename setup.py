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
            requirements.append(re.match(r'.*#egg=(?P<egg>.*)', requirement).group('egg'))
        else:
            requirements.append(requirement)

setup(
    name="jasmine-py",
    version="2.0",

    packages=find_packages(),

    install_requires=requirements,

    dependency_links=non_pypi_requirements
)
