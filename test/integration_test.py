# coding=utf-8
import sys
import subprocess
from subprocess import Popen, PIPE
from time import sleep
import requests
from pytest import fail

def get_with_retries(url):
    n = 0
    while True:
        try:
            return requests.get(url)
        except requests.ConnectionError:
            if n < 20:
                n += 1
                sleep(0.1)
            else:
                raise

def test_standalone_serves_html():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/')

        assert req.status_code == 200
        assert '/__jasmine__/jasmine.js' in req.text
        assert '/__src__/main.js' in req.text
        assert '/__src__/main.css' in req.text
        assert '/__spec__/someSpec.js' in req.text
    finally:
        process.terminate()

def test_standalone_supports_query_strings():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/?random=true')

        assert req.status_code == 200
    finally:
        process.terminate()

def test_standalone_serves_jasmine_files():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__jasmine__/jasmine.css')

        assert 'text/css' in req.headers['content-type']
        assert req.status_code == 200
    finally:
        process.terminate()

def test_standalone_serves_jasmine_css_files():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__jasmine__/jasmine.js')

        assert 'application/javascript' in req.headers['content-type']
        assert req.status_code == 200
    finally:
        process.terminate()

def test_standalone_serves_jasmine_favicon():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__jasmine__/jasmine_favicon.png')

        assert 'image/png' in req.headers['content-type']
        assert req.status_code == 200
    finally:
        process.terminate()

def test_standalone_serves_js():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__src__/main.js')

        assert 'application/javascript' in req.headers['content-type']
        assert req.status_code == 200
        assert "thingUnderTest" in req.text
    finally:
        process.terminate()

def test_standalone_serves_css():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__src__/main.css')

        assert 'text/css' in req.headers['content-type']
        assert req.status_code == 200
        assert "CSS" in req.text
    finally:
        process.terminate()

def test_standalone_serves_weird_encodings():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'server', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__src__/weird_encoding.js')

        req.encoding = 'iso8859-1'
        assert req.status_code == 200

        assert u"weirdEncoding = 'ã'" in req.text
    finally:
        process.terminate()

def test_ci():
    if subprocess.call('which geckodriver > /dev/null', shell=True) != 0:
        fail('Geckodriver was not found in $PATH')

    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()', 'ci', '--config', 'test/fixture_files/jasmine.yml'], stdout=PIPE)
    output = process.communicate()[0]
    process.wait()

    assert '2 specs, 0 failed' in str(output)
    assert process.returncode == 0

def test_help_fallback():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import begin; begin()'], stdout=PIPE)
    output = process.communicate()[0]
    process.wait()

    assert 'usage:' in str(output)
    assert 'Jasmine command line' in str(output)
    assert process.returncode != 0
