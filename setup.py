from setuptools import setup, find_packages
setup(
    name="jasmine-py",
    version="2.0",

    packages=find_packages(),

    install_requires=['jasmine==2.0', 'PyYAML==3.10']
)
