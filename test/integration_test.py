# coding=utf-8
import sys
from subprocess import Popen, PIPE
from time import sleep
import requests

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
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import standalone; standalone()', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/')

        assert req.status_code == 200
        assert '/__jasmine__/jasmine.js' in req.text
        assert '/__src__/main.js' in req.text
        assert '/__src__/main.css' in req.text
        assert '/__spec__/someSpec.js' in req.text
    finally:
        process.terminate()

def test_standalone_serves_jasmine_files():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import standalone; standalone()', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__jasmine__/jasmine.js')

        assert req.status_code == 200
    finally:
        process.terminate()

def test_standalone_serves_jasmine_favicon():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import standalone; standalone()', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__jasmine__/jasmine_favicon.png')

        assert req.status_code == 200
    finally:
        process.terminate()

def test_standalone_serves_js():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import standalone; standalone()', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__src__/main.js')

        assert req.status_code == 200
        assert "thingUnderTest" in req.text
    finally:
        process.terminate()

def test_standalone_serves_css():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import standalone; standalone()', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__src__/main.css')

        assert req.status_code == 200
        assert "CSS" in req.text
    finally:
        process.terminate()

def test_standalone_serves_weird_encodings():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import standalone; standalone()', '--config', 'test/fixture_files/jasmine.yml'])
    try:
        req = get_with_retries('http://localhost:8888/__src__/weird_encoding.js')

        req.encoding = 'iso8859-1'
        assert req.status_code == 200

        assert u"weirdEncoding = 'ã'" in req.text
    finally:
        process.terminate()

def test_ci():
    process = Popen([sys.executable, '-c', 'from jasmine.entry_points import continuous_integration; continuous_integration()', '--config', 'test/fixture_files/jasmine.yml'], stdout=PIPE)
    output = process.communicate()[0]
    process.wait()

    assert '2 specs, 0 failed' in str(output)
    assert process.returncode == 0
