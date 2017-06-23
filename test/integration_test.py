#import pytest
from subprocess import Popen
from time import sleep
import os
import requests

running_indicator = ' * Running on http://127.0.0.1:8888/ (Press CTRL+C to quit)'

def get_with_retries(url):
    n = 0
    while True:
        try:
            return requests.get(url)
        except requests.ConnectionError as e:
            if n < 5:
                n += 1
                sleep(0.1)
            else:
                raise

def test_standalone_serves_html():
    config_path = os.path.join(os.getcwd(), 'test/fixture_files/jasmine.yml')
    env = { 'JASMINE_CONFIG_PATH': config_path }
    process = Popen(['python', '-c', 'from jasmine.entry_points import standalone; standalone()'], env=env)
    try:
        req = get_with_retries('http://localhost:8888/')
        # w00t
    finally:
        process.terminate()
    raise BaseException
    #using IntegrationTestServerThread(config_somehow) as server_thread:
        # http request to server at /
        # check the html for some stuff
